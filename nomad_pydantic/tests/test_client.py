import json
from pathlib import Path

import pytest

from nomad_pydantic import CommandResult, Job, NomadClient, NomadCommandError, NomadConfiguration, Task, TaskGroup


class RecordingRunner:
    def __init__(self, results: list[CommandResult] | None = None) -> None:
        self.commands: list[list[str]] = []
        self.results = results or []

    def run(self, command: list[str], timeout: float | None = None) -> CommandResult:
        self.commands.append(command)
        return self.results.pop(0) if self.results else CommandResult(0, "", "")


@pytest.fixture
def configuration(tmp_path: Path) -> NomadConfiguration:
    return NomadConfiguration(
        job=Job(
            id="example",
            namespace="analytics",
            type="batch",
            task_groups=[TaskGroup(name="job", tasks=[Task(name="job", driver="exec", config={"command": "/bin/true"})])],
        ),
        path=tmp_path / "example.json",
    )


def test_configuration_writes_and_loads_json(configuration: NomadConfiguration) -> None:
    path = configuration.write()

    assert json.loads(path.read_text())["Job"]["ID"] == "example"
    assert NomadConfiguration.from_file(path).job == configuration.job


def test_configuration_loads_hydra_yaml(tmp_path: Path) -> None:
    (tmp_path / "job.yaml").write_text(
        """job:
  id: report
  type: batch
  task_groups:
    - name: report
      tasks:
        - name: report
          driver: exec
"""
    )

    configuration = NomadConfiguration.load(tmp_path, "job", overrides=["+job.namespace=analytics"])

    assert configuration.job.id == "report"
    assert configuration.job.namespace == "analytics"


def test_client_registers_and_manages_job(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner()
    client = NomadClient(configuration, runner=runner)

    client.register()
    client.start()
    client.restart()
    client.force_periodic()
    client.stop(purge=True)

    path = str(configuration.path)
    assert runner.commands == [
        ["nomad", "job", "run", "-json", "-detach", path],
        ["nomad", "job", "start", "-detach", "-namespace=analytics", "example"],
        ["nomad", "job", "restart", "-yes", "-all-tasks", "-namespace=analytics", "example"],
        ["nomad", "job", "periodic", "force", "-namespace=analytics", "example"],
        ["nomad", "job", "stop", "-yes", "-detach", "-purge", "-namespace=analytics", "example"],
    ]


def test_client_reads_status(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner([CommandResult(0, '{"ID":"example","Status":"running","Type":"batch"}', "")])

    status = NomadClient(configuration, runner=runner).status()

    assert status.id == "example"
    assert status.running


def test_client_raises_useful_error(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner([CommandResult(1, "", "permission denied")])

    with pytest.raises(NomadCommandError, match="permission denied"):
        NomadClient(configuration, runner=runner).status()
