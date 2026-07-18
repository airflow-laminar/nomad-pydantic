# Tutorial: render a first Nomad job

In this tutorial, we will model a small batch job, render its Nomad JSON, and
inspect the result without connecting to a Nomad cluster.

## Install the package

```bash
pip install nomad-pydantic
```

## Create the job

Create `hello.py`:

```python
from nomad_pydantic import Job, NomadConfiguration, Resources, Task, TaskGroup

config = NomadConfiguration(
    job=Job(
        id="hello",
        type="batch",
        datacenters=["dc1"],
        task_groups=[
            TaskGroup(
                name="hello",
                tasks=[
                    Task(
                        name="hello",
                        driver="docker",
                        config={"image": "alpine:3", "args": ["echo", "hello"]},
                        resources=Resources(cpu=100, memory_mb=64),
                    )
                ],
            )
        ],
    ),
    path="build/hello.json",
)

print(config.write())
```

Run it:

```bash
python hello.py
```

The output is the generated file:

```text
build/hello.json
```

## Inspect the jobspec

Open `build/hello.json`. It contains a `Job` envelope with `TaskGroups`, `Tasks`,
and `Resources` using Nomad's JSON API field names.

Validate the file if the Nomad CLI is installed:

```bash
nomad job validate -json build/hello.json
```

The command reports that the job validation succeeded. You have now produced a
typed Nomad jobspec without writing HCL or contacting a cluster.
