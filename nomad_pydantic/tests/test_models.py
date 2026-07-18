import json

import pytest
from pydantic import ValidationError

from nomad_pydantic import Job, PeriodicConfig, Resources, Task, TaskGroup


def test_job_renders_nomad_json() -> None:
    job = Job(
        id="example",
        type="service",
        datacenters=["dc1"],
        task_groups=[
            TaskGroup(
                name="web",
                tasks=[Task(name="server", driver="docker", config={"image": "nginx:alpine"})],
            )
        ],
    )

    rendered = json.loads(job.to_json())

    assert rendered == {
        "Job": {
            "ID": "example",
            "Name": "example",
            "Type": "service",
            "Datacenters": ["dc1"],
            "TaskGroups": [
                {
                    "Name": "web",
                    "Count": 1,
                    "Tasks": [
                        {
                            "Name": "server",
                            "Driver": "docker",
                            "Config": {"image": "nginx:alpine"},
                        }
                    ],
                }
            ],
        }
    }
    assert Job.from_json(job.to_json()) == job


def test_periodic_job_validation() -> None:
    job = Job(
        id="report",
        type="batch",
        periodic=PeriodicConfig(crons=["0 6 * * *"], time_zone="America/New_York"),
        task_groups=[TaskGroup(name="report", tasks=[Task(name="report", driver="exec")])],
    )

    assert job.model_dump(by_alias=True, exclude_none=True)["Periodic"]["Specs"] == ["0 6 * * *"]

    with pytest.raises(ValidationError, match="batch or sysbatch"):
        Job(
            id="invalid",
            type="service",
            periodic=PeriodicConfig(crons=["@daily"]),
            task_groups=[TaskGroup(name="task", tasks=[Task(name="task", driver="exec")])],
        )


def test_resources_reject_cpu_and_cores() -> None:
    with pytest.raises(ValidationError, match="cpu and cores"):
        Resources(cpu=500, cores=1)


def test_nomad_durations_render_as_nanoseconds() -> None:
    task = Task(name="worker", driver="exec", kill_timeout="1m30s")

    assert task.model_dump(by_alias=True)["KillTimeout"] == 90_000_000_000

    assert Task(name="worker", driver="exec", kill_timeout=42).kill_timeout == 42
    with pytest.raises(ValidationError, match="invalid Nomad duration"):
        Task(name="worker", driver="exec", kill_timeout="1s-bad")
    with pytest.raises(ValidationError, match="invalid Nomad duration"):
        Task(name="worker", driver="exec", kill_timeout="1sx2s")
    with pytest.raises(ValidationError, match="invalid Nomad duration"):
        Task(name="worker", driver="exec", kill_timeout="")


def test_job_rejects_duplicate_names() -> None:
    with pytest.raises(ValidationError, match="task names must be unique"):
        TaskGroup(name="workers", tasks=[Task(name="worker", driver="exec"), Task(name="worker", driver="exec")])

    with pytest.raises(ValidationError, match="at least one task"):
        TaskGroup(name="empty", tasks=[])

    group = TaskGroup(name="worker", tasks=[Task(name="worker", driver="exec")])
    with pytest.raises(ValidationError, match="at least one task group"):
        Job(id="empty", task_groups=[])
    with pytest.raises(ValidationError, match="task group names must be unique"):
        Job(id="duplicate", task_groups=[group, group])


def test_job_loads_bare_json() -> None:
    job = Job.from_json('{"ID":"example","TaskGroups":[{"Name":"group","Tasks":[{"Name":"task","Driver":"exec"}]}]}')

    assert job.id == "example"
