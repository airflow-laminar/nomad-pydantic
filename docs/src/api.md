# API reference

The public API is re-exported from `nomad_pydantic`.

## Job models

```{eval-rst}
.. currentmodule:: nomad_pydantic

.. autosummary::
   :toctree: _build

   Job
   TaskGroup
   Task
   PeriodicConfig
   Resources
   NetworkResource
   NetworkPort
   RestartPolicy
   ReschedulePolicy
   UpdateStrategy
   Service
   ServiceCheck
   CheckRestart
   Lifecycle
   LogConfig
   Template
   Artifact
   Volume
   VolumeMount
```

## Configuration and lifecycle

```{eval-rst}
.. currentmodule:: nomad_pydantic

.. autosummary::
   :toctree: _build

   NomadConfiguration
   NomadClient
   JobStatus
   JobSummary
   TaskGroupStatus
   AllocationStatus
   DeploymentStatus
   EvaluationStatus
   CommandResult
   CommandRunner
   SubprocessCommandRunner
   NomadCommandError
```
