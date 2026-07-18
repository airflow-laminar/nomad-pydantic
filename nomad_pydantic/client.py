from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol

from pydantic import Field

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
        result = subprocess.run(command, capture_output=True, check=False, text=True, timeout=timeout)
        return CommandResult(result.returncode, result.stdout, result.stderr)


class NomadCommandError(RuntimeError):
    def __init__(self, command: list[str], result: CommandResult) -> None:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit status {result.returncode}"
        super().__init__(f"{' '.join(command)} failed: {detail}")
        self.command = command
        self.result = result


class StatusModel(NomadModel):
    model_config = {**NomadModel.model_config, "extra": "ignore"}


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
