import json
import subprocess
from pathlib import Path

import pytest

import nomad_pydantic.config as config_module
from nomad_pydantic import CommandResult, Job, NomadClient, NomadCommandError, NomadConfiguration, SubprocessCommandRunner, Task, TaskGroup


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

    alternate = NomadConfiguration(job=configuration.job, working_dir=path.parent / "alternate")
    assert alternate.path == path.parent / "alternate" / "example.json"


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


def test_configuration_rejects_non_mapping_hydra_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "job.yaml").write_text("job: {}\n")
    monkeypatch.setattr(config_module.OmegaConf, "to_container", lambda *args, **kwargs: [])

    with pytest.raises(ValueError, match="must be a mapping"):
        NomadConfiguration.load(tmp_path, "job")


def test_client_registers_and_manages_job(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner()
    client = NomadClient(configuration, runner=runner)

    client.register()
    client.validate()
    client.start()
    client.restart()
    client.force_periodic()
    client.stop(purge=True)

    path = str(configuration.path)
    assert runner.commands == [
        ["nomad", "job", "run", "-json", "-detach", path],
        ["nomad", "job", "validate", "-json", path],
        ["nomad", "job", "start", "-detach", "-namespace=analytics", "example"],
        ["nomad", "job", "restart", "-yes", "-all-tasks", "-namespace=analytics", "example"],
        ["nomad", "job", "periodic", "force", "-namespace=analytics", "example"],
        ["nomad", "job", "stop", "-yes", "-detach", "-purge", "-namespace=analytics", "example"],
    ]


def test_configuration_lifecycle_shortcuts(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner([CommandResult(0, '{"ID":"example","Status":"dead","Stop":true}', "")])

    assert configuration.client(runner=runner).configuration is configuration
    assert configuration.status(runner=runner).stopped
    configuration.register(runner=runner)
    configuration.start(runner=runner)
    configuration.restart(runner=runner)
    configuration.force_periodic(runner=runner)
    configuration.stop(runner=runner)


def test_client_without_namespace(tmp_path: Path) -> None:
    configuration = NomadConfiguration(
        job=Job(id="example", task_groups=[TaskGroup(name="job", tasks=[Task(name="job", driver="exec")])]),
        path=tmp_path / "example.json",
    )
    runner = RecordingRunner([CommandResult(0, '{"ID":"example","Status":"dead"}', "")])

    status = NomadClient(configuration, runner=runner).status()
    NomadClient(configuration, runner=runner).stop()

    assert status.stopped
    assert runner.commands[0] == ["nomad", "job", "status", "-json", "example"]
    assert runner.commands[1] == ["nomad", "job", "stop", "-yes", "-detach", "example"]


def test_client_reads_status(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner([CommandResult(0, '{"ID":"example","Status":"running","Type":"batch"}', "")])

    status = NomadClient(configuration, runner=runner).status()

    assert status.id == "example"
    assert status.running


def test_client_raises_useful_error(configuration: NomadConfiguration) -> None:
    runner = RecordingRunner([CommandResult(1, "", "permission denied")])

    with pytest.raises(NomadCommandError, match="permission denied"):
        NomadClient(configuration, runner=runner).status()

    with pytest.raises(NomadCommandError, match="standard output"):
        NomadClient(configuration, runner=RecordingRunner([CommandResult(1, "standard output", "")])).status()
    with pytest.raises(NomadCommandError, match="exit status 2"):
        NomadClient(configuration, runner=RecordingRunner([CommandResult(2, "", "")])).status()


def test_subprocess_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    def run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(["nomad", "version"], 0, "Nomad v1", "")

    monkeypatch.setattr(subprocess, "run", run)

    assert SubprocessCommandRunner().run(["nomad", "version"]).stdout == "Nomad v1"
