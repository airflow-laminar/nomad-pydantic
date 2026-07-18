from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

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


class JobStatus(NomadModel):
    model_config = {**NomadModel.model_config, "extra": "ignore"}

    id: str = Field(alias="ID")
    name: str | None = None
    namespace: str | None = None
    type: str | None = None
    status: str
    status_description: str | None = None
    stop: bool = False

    @property
    def running(self) -> bool:
        return self.status == "running" and not self.stop

    @property
    def stopped(self) -> bool:
        return self.stop or self.status == "dead"


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
        return JobStatus.model_validate(json.loads(result.stdout))

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
