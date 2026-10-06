from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Protocol
from urllib.parse import quote, urlencode

from pydantic import ConfigDict, Field, field_validator

from nomad_pydantic.models import NomadModel

if TYPE_CHECKING:
    from nomad_pydantic.config import NomadConfiguration


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class CommandRunner(Protocol):
    def run(self, command: list[str], timeout: float | None = None) -> CommandResult: ...


class SubprocessCommandRunner:
    def run(self, command: list[str], timeout: float | None = None) -> CommandResult:
        result = subprocess.run(command, capture_output=True, check=False, timeout=timeout)
        return CommandResult(
            result.returncode, result.stdout.decode("utf-8", errors="surrogateescape"), result.stderr.decode("utf-8", errors="surrogateescape")
        )


class NomadCommandError(RuntimeError):
    def __init__(self, command: list[str], result: CommandResult) -> None:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit status {result.returncode}"
        super().__init__(f"{' '.join(command)} failed: {detail}")
        self.command = command
        self.result = result


class StatusModel(NomadModel):
    model_config: ClassVar[ConfigDict] = {**NomadModel.model_config, "extra": "ignore"}


class TaskGroupStatus(StatusModel):
    queued: int = 0
    complete: int = 0
    failed: int = 0
    running: int = 0
    starting: int = 0
    lost: int = 0
    unknown: int = 0


class JobSummary(StatusModel):
    job_id: str = Field(alias="JobID")
    namespace: str = "default"
    summary: dict[str, TaskGroupStatus]


class AllocationStatus(StatusModel):
    id: str = Field(alias="ID")
    job_version: int = 0
    task_group: str
    desired_status: str
    client_status: str
    task_states: dict[str, TaskState] = Field(default_factory=dict)

    @field_validator("task_states", mode="before")
    @classmethod
    def empty_task_states(cls, value: Any) -> Any:
        return value or {}


class TaskEvent(StatusModel):
    type: str
    display_message: str = ""
    exit_code: int = 0
    signal: int = 0


class TaskState(StatusModel):
    state: str
    failed: bool = False
    events: list[TaskEvent] = Field(default_factory=list)


@dataclass(frozen=True)
class LogChunk:
    file: str
    offset: int
    data: bytes
    truncated: bool = False


class DeploymentStatus(StatusModel):
    id: str = Field(alias="ID")
    status: str
    status_description: str | None = None


class EvaluationStatus(StatusModel):
    id: str = Field(alias="ID")
    status: str
    failed_task_group_allocations: dict[str, Any] | None = Field(default=None, alias="FailedTGAllocs")


class JobStatus(StatusModel):
    """Status bundle emitted by ``nomad job status -json`` for one job."""

    summary: JobSummary
    allocations: list[AllocationStatus]
    latest_deployment: DeploymentStatus | None = None
    evaluations: list[EvaluationStatus]

    @classmethod
    def from_cli(cls, value: str | bytes) -> JobStatus:
        data = json.loads(value)
        if not isinstance(data, list) or len(data) != 1:
            raise ValueError("Nomad job status must contain exactly one job")
        return cls.model_validate(data[0])

    @property
    def id(self) -> str:
        return self.summary.job_id

    @property
    def namespace(self) -> str:
        return self.summary.namespace

    @property
    def current_allocations(self) -> list[AllocationStatus]:
        if not self.allocations:
            return []
        version = max(allocation.job_version for allocation in self.allocations)
        return [allocation for allocation in self.allocations if allocation.job_version == version and allocation.desired_status == "run"]

    @property
    def running(self) -> bool:
        return any(group.queued or group.starting or group.running for group in self.summary.summary.values())

    @property
    def complete(self) -> bool:
        current = self.current_allocations
        return bool(current) and not self.running and all(allocation.client_status == "complete" for allocation in current)

    @property
    def failed(self) -> bool:
        current = self.current_allocations
        return bool(current) and not self.running and any(allocation.client_status in {"failed", "lost"} for allocation in current)

    @property
    def stopped(self) -> bool:
        return bool(self.allocations) and all(allocation.desired_status == "stop" for allocation in self.allocations)


class NomadClient:
    """Manage a configuration through the installed Nomad CLI."""

    def __init__(
        self,
        configuration: NomadConfiguration,
        *,
        runner: CommandRunner | None = None,
        executable: str = "nomad",
    ) -> None:
        self.configuration = configuration
        self.runner = runner or SubprocessCommandRunner()
        self.executable = executable

    def _run(self, command: list[str]) -> CommandResult:
        result = self.runner.run([self.executable, *command], timeout=self.configuration.command_timeout)
        if result.returncode:
            raise NomadCommandError([self.executable, *command], result)
        return result

    def _identity(self) -> list[str]:
        namespace = self.configuration.job.namespace
        return ([f"-namespace={namespace}"] if namespace else []) + [self.configuration.job.id]

    def register(self) -> CommandResult:
        path = self.configuration.write()
        return self._run(["job", "run", "-json", "-detach", str(path)])

    def validate(self) -> CommandResult:
        path = self.configuration.write()
        return self._run(["job", "validate", "-json", str(path)])

    def status(self) -> JobStatus:
        result = self._run(["job", "status", "-json", *self._identity()])
        return JobStatus.from_cli(result.stdout)

    def read_logs(
        self,
        allocation_id: str,
        task: str,
        stream: Literal["stdout", "stderr"],
        *,
        offsets: dict[str, int] | None = None,
        limit: int = 65536,
    ) -> list[LogChunk]:
        """Read at most ``limit`` bytes across retained log files, oldest first.

        Pass each returned file's offset plus data length on the next call.
        Nomad's ``read-fs`` namespace capability is required.
        """
        if limit <= 0:
            raise ValueError("limit must be positive")
        if stream not in {"stdout", "stderr"}:
            raise ValueError("stream must be stdout or stderr")
        query = {"namespace": self.configuration.job.namespace or "default", "path": "alloc/logs"}
        allocation = quote(allocation_id, safe="")
        listing = self._run(["operator", "api", f"/v1/client/fs/ls/{allocation}?{urlencode(query)}"])
        prefix = f"{task}.{stream}."
        files = [entry for entry in json.loads(listing.stdout) if entry["Name"].startswith(prefix) and entry["Name"][len(prefix) :].isdigit()]
        chunks = []
        for entry in sorted(files, key=lambda entry: int(entry["Name"][len(prefix) :])):
            name = entry["Name"]
            offset = (offsets or {}).get(name, 0)
            truncated = offset > entry["Size"]
            if truncated:
                offset = 0
            size = min(entry["Size"] - offset, limit)
            if size <= 0:
                continue
            params = {**query, "path": f"alloc/logs/{name}", "offset": offset, "limit": size}
            result = self._run(["operator", "api", f"/v1/client/fs/readat/{allocation}?{urlencode(params)}"])
            data = result.stdout.encode("utf-8", errors="surrogateescape")
            chunks.append(LogChunk(name, offset, data, truncated))
            limit -= len(data)
            if limit <= 0:
                break
        return chunks

    def start(self) -> CommandResult:
        return self._run(["job", "start", "-detach", *self._identity()])

    def restart(self) -> CommandResult:
        return self._run(["job", "restart", "-yes", "-all-tasks", *self._identity()])

    def force_periodic(self) -> CommandResult:
        return self._run(["job", "periodic", "force", *self._identity()])

    def stop(self, *, purge: bool = False) -> CommandResult:
        options = ["job", "stop", "-yes", "-detach"]
        if purge:
            options.append("-purge")
        return self._run([*options, *self._identity()])
