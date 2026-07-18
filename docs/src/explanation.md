# Why model Nomad jobs in Python?

Nomad accepts JSON jobs through its API and CLI, while operators commonly author
jobs in HCL. `nomad-pydantic` uses the JSON representation as its boundary because
it is the native structure exchanged with Nomad and maps directly to nested
Pydantic models.

## Jobs form a typed hierarchy

A Nomad job contains task groups, and each task group contains colocated tasks.
The model hierarchy preserves that structure:

```text
Job
└── TaskGroup
    ├── Task
    │   ├── Resources
    │   ├── Service
    │   └── VolumeMount
    ├── NetworkResource
    └── Volume
```

Validation therefore happens before scheduling. Duplicate task names, invalid
periodic job types, and mutually exclusive CPU settings fail when models are
created rather than after submission to a cluster.

## Python names and Nomad names serve different boundaries

Python callers use `snake_case`, such as `task_groups`, `memory_mb`, and
`kill_timeout`. Rendered jobs use Nomad's API names, such as `TaskGroups`,
`MemoryMB`, and `KillTimeout`.

Nomad's JSON API encodes durations as nanoseconds. Models accept readable values
such as `30s` and `1m30s`, then render their integer nanosecond equivalents. This
keeps YAML and Python configuration readable without changing the wire format.

## Configuration and lifecycle are separate concerns

`Job` describes desired scheduler state. `NomadConfiguration` associates that job
with a local JSON artifact. `NomadClient` performs lifecycle operations through
the Nomad CLI. Separating these layers allows rendering and validation without a
cluster and allows lifecycle tests to replace process execution with a fake
runner.

`nomad job status -json` combines the job summary with allocations, the latest
deployment, and evaluations. `JobStatus` preserves that structure. Its
`running`, `complete`, `failed`, and `stopped` properties derive lifecycle state
from current-version allocations and task-group summary counts rather than from
Nomad's coarse `running`/`dead` job status.

This mirrors the boundary used by
[supervisor-pydantic](https://github.com/airflow-laminar/supervisor-pydantic) and
[systemd-pydantic](https://github.com/airflow-laminar/systemd-pydantic): models
describe workload configuration, while a client handles runtime state.
