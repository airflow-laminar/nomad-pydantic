import json
from urllib.parse import parse_qs, urlsplit

import pytest

from nomad_pydantic import AllocationStatus, CommandResult, Job, NomadClient, NomadConfiguration, Task, TaskGroup


class LogRunner:
    def __init__(self) -> None:
        self.files = {"worker.stdout.0": b"hello\n", "worker.stdout.1": "world €\n".encode(), "worker.stderr.0": b"error\n"}
        self.commands: list[list[str]] = []

    def run(self, command: list[str], timeout: float | None = None) -> CommandResult:
        self.commands.append(command)
        url = urlsplit(command[-1])
        query = parse_qs(url.query)
        assert query["namespace"] == ["analytics"]
        if "/ls/" in url.path:
            return CommandResult(0, json.dumps([{"Name": name, "Size": len(data)} for name, data in self.files.items()]), "")
        data = self.files[query["path"][0].rsplit("/", 1)[-1]]
        start, limit = int(query["offset"][0]), int(query["limit"][0])
        return CommandResult(0, data[start : start + limit].decode("utf-8", errors="surrogateescape"), "")


def test_incremental_logs_preserve_bytes_and_rotation() -> None:
    runner = LogRunner()
    client = NomadClient(
        NomadConfiguration(
            job=Job(id="job", namespace="analytics", task_groups=[TaskGroup(name="group", tasks=[Task(name="worker", driver="raw_exec")])])
        ),
        runner=runner,
    )
    offsets: dict[str, int] = {}
    data = b""
    for _ in range(7):
        chunks = client.read_logs("allocation", "worker", "stdout", offsets=offsets, limit=3)
        assert sum(len(chunk.data) for chunk in chunks) <= 3
        for chunk in chunks:
            data += chunk.data
            offsets[chunk.file] = chunk.offset + len(chunk.data)
    assert data == b"hello\n" + "world €\n".encode()
    assert client.read_logs("allocation", "worker", "stdout", offsets=offsets) == []
    del runner.files["worker.stdout.0"]
    runner.files["worker.stdout.2"] = b"rotated\n"
    chunks = client.read_logs("allocation", "worker", "stdout", offsets=offsets)
    assert [chunk.data for chunk in chunks] == [b"rotated\n"]
    assert client.read_logs("allocation", "worker", "stderr")[0].data == b"error\n"


def test_truncated_logs_reset_offset() -> None:
    runner = LogRunner()
    client = NomadClient(
        NomadConfiguration(
            job=Job(id="job", namespace="analytics", task_groups=[TaskGroup(name="group", tasks=[Task(name="worker", driver="raw_exec")])])
        ),
        runner=runner,
    )
    chunks = client.read_logs("allocation", "worker", "stdout", offsets={"worker.stdout.0": 100})
    assert chunks[0].truncated
    assert chunks[0].offset == 0
    assert chunks[0].data == b"hello\n"


@pytest.mark.parametrize("kwargs", [{"limit": 0}, {"limit": -1}, {"stream": "invalid"}])
def test_log_arguments_are_validated(kwargs: dict) -> None:
    client = NomadClient(NomadConfiguration(job=Job(id="job", task_groups=[TaskGroup(name="group", tasks=[Task(name="worker", driver="raw_exec")])])))
    with pytest.raises(ValueError):
        client.read_logs("allocation", "worker", **{"stream": "stdout", **kwargs})  # ty: ignore[invalid-argument-type]


def test_allocation_preserves_failure_events() -> None:
    status = AllocationStatus.model_validate(
        {
            "ID": "allocation",
            "TaskGroup": "group",
            "DesiredStatus": "run",
            "ClientStatus": "failed",
            "TaskStates": {
                "worker": {
                    "State": "dead",
                    "Failed": True,
                    "Events": [{"Type": "Terminated", "ExitCode": 7, "Signal": 0, "DisplayMessage": "Exit Code: 7"}],
                }
            },
        }
    )
    assert status.task_states["worker"].events[-1].exit_code == 7


def test_allocation_pending_task_states_can_be_null() -> None:
    allocation = AllocationStatus.model_validate(
        {"ID": "allocation", "TaskGroup": "group", "DesiredStatus": "run", "ClientStatus": "pending", "TaskStates": None}
    )
    assert allocation.task_states == {}


def test_subprocess_runner_preserves_log_bytes():
    import sys

    from nomad_pydantic import SubprocessCommandRunner

    result = SubprocessCommandRunner().run([sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'line\\r\\n\\xff')"])
    assert result.stdout.encode("utf-8", errors="surrogateescape") == b"line\r\n\xff"
