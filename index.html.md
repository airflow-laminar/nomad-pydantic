# nomad-pydantic

Typed Python models for building, validating, rendering, and managing
[Nomad](https://developer.hashicorp.com/nomad) jobs.

[![Build Status](https://github.com/airflow-laminar/nomad-pydantic/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/airflow-laminar/nomad-pydantic/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/airflow-laminar/nomad-pydantic/branch/main/graph/badge.svg)](https://codecov.io/gh/airflow-laminar/nomad-pydantic)
[![License](https://img.shields.io/github/license/airflow-laminar/nomad-pydantic)](https://github.com/airflow-laminar/nomad-pydantic)
[![PyPI](https://img.shields.io/pypi/v/nomad-pydantic.svg)](https://pypi.python.org/pypi/nomad-pydantic)

`nomad-pydantic` represents jobs, task groups, tasks, resources, services,
volumes, and periodic schedules as Pydantic models. It renders the JSON envelope
accepted by `nomad job run -json` and provides a mockable client for common
Nomad CLI lifecycle operations.

```python
from nomad_pydantic import Job, NomadConfiguration, Task, TaskGroup

config = NomadConfiguration(
    job=Job(
        id="hello",
        type="batch",
        task_groups=[
            TaskGroup(
                name="hello",
                tasks=[
                    Task(
                        name="hello",
                        driver="docker",
                        config={"image": "alpine:3", "args": ["echo", "hello"]},
                    )
                ],
            )
        ],
    )
)

config.write()
```

## Documentation

- [Tutorial](docs/src/tutorial.md) builds and renders a first job.
- [How-to guides](docs/src/how-to.md) cover Hydra, periodic jobs, and lifecycle
  operations.
- [Concepts](docs/src/explanation.md) explains the model hierarchy and JSON
  boundary.
- [API reference](docs/src/api.md) documents every public model and client.

## Ecosystem

`nomad-pydantic` follows the same configuration pattern as
[supervisor-pydantic](https://github.com/airflow-laminar/supervisor-pydantic),
[systemd-pydantic](https://github.com/airflow-laminar/systemd-pydantic), and
[cron-pydantic](https://github.com/airflow-laminar/cron-pydantic). The broader
declarative Airflow stack is built from
[airflow-pydantic](https://github.com/airflow-laminar/airflow-pydantic) and
[airflow-config](https://github.com/airflow-laminar/airflow-config), with runtime
integrations provided by
[airflow-nomad](https://github.com/airflow-laminar/airflow-nomad),
[airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor),
[airflow-systemd](https://github.com/airflow-laminar/airflow-systemd), and
[airflow-cron](https://github.com/airflow-laminar/airflow-cron).

## Installation

```bash
pip install nomad-pydantic
```
