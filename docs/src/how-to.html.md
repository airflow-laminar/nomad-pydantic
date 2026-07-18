# How-to guides

These guides provide focused recipes for loading and operating Nomad jobs.
Consult the [API reference](api.md) for the complete model surface.

## How to load a job from Hydra YAML

Create `config/jobs/report.yaml`:

```yaml
job:
  id: report
  type: batch
  namespace: analytics
  task_groups:
    - name: report
      tasks:
        - name: report
          driver: exec
          config:
            command: /opt/reports/build
          resources:
            cpu: 500
            memory_mb: 256
```

Compose and validate it:

```python
from nomad_pydantic import NomadConfiguration

config = NomadConfiguration.load("config/jobs", "report")
config.write("build/report.json")
```

Pass Hydra overrides when values vary between deployments:

```python
config = NomadConfiguration.load(
    "config/jobs",
    "report",
    overrides=["job.namespace=staging", "job.task_groups.0.count=2"],
)
```

## How to schedule a periodic job

Add `PeriodicConfig` to a `batch` or `sysbatch` job:

```python
from nomad_pydantic import Job, PeriodicConfig, Task, TaskGroup

job = Job(
    id="daily-report",
    type="batch",
    periodic=PeriodicConfig(
        crons=["0 6 * * *"],
        time_zone="America/New_York",
        prohibit_overlap=True,
    ),
    task_groups=[
        TaskGroup(
            name="report",
            tasks=[Task(name="report", driver="exec", config={"command": "/opt/reports/build"})],
        )
    ],
)
```

The model renders `crons` as Nomad’s JSON `Specs` field and includes
`SpecType: cron`.

## How to register and manage a job

The lifecycle methods invoke the installed `nomad` executable. Nomad CLI
environment variables and configuration continue to control cluster address and
authentication.

```python
from nomad_pydantic import NomadConfiguration

config = NomadConfiguration.from_file("build/report.json")

config.register()
status = config.status()

if status.running:
    config.restart()

config.stop()
```

Use `config.stop(purge=True)` to remove job history. Use
`config.force_periodic()` to launch a periodic job immediately.

## How to test lifecycle code without Nomad

Provide an object implementing `CommandRunner`:

```python
from nomad_pydantic import CommandResult, NomadClient


class FakeRunner:
    def run(self, command, timeout=None):
        return CommandResult(0, '{"ID":"report","Status":"running"}', "")


client = NomadClient(config, runner=FakeRunner())
assert client.status().running
```
