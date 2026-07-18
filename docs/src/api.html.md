# API reference

The public API is re-exported from `nomad_pydantic`.

## Job models

| [`Job`](_build/nomad_pydantic.Job.md#nomad_pydantic.Job)                                        |    |
|-------------------------------------------------------------------------------------------------|----|
| [`TaskGroup`](_build/nomad_pydantic.TaskGroup.md#nomad_pydantic.TaskGroup)                      |    |
| [`Task`](_build/nomad_pydantic.Task.md#nomad_pydantic.Task)                                     |    |
| [`PeriodicConfig`](_build/nomad_pydantic.PeriodicConfig.md#nomad_pydantic.PeriodicConfig)       |    |
| [`Resources`](_build/nomad_pydantic.Resources.md#nomad_pydantic.Resources)                      |    |
| [`NetworkResource`](_build/nomad_pydantic.NetworkResource.md#nomad_pydantic.NetworkResource)    |    |
| [`NetworkPort`](_build/nomad_pydantic.NetworkPort.md#nomad_pydantic.NetworkPort)                |    |
| [`RestartPolicy`](_build/nomad_pydantic.RestartPolicy.md#nomad_pydantic.RestartPolicy)          |    |
| [`ReschedulePolicy`](_build/nomad_pydantic.ReschedulePolicy.md#nomad_pydantic.ReschedulePolicy) |    |
| [`UpdateStrategy`](_build/nomad_pydantic.UpdateStrategy.md#nomad_pydantic.UpdateStrategy)       |    |
| [`Service`](_build/nomad_pydantic.Service.md#nomad_pydantic.Service)                            |    |
| [`ServiceCheck`](_build/nomad_pydantic.ServiceCheck.md#nomad_pydantic.ServiceCheck)             |    |
| [`CheckRestart`](_build/nomad_pydantic.CheckRestart.md#nomad_pydantic.CheckRestart)             |    |
| [`Lifecycle`](_build/nomad_pydantic.Lifecycle.md#nomad_pydantic.Lifecycle)                      |    |
| [`LogConfig`](_build/nomad_pydantic.LogConfig.md#nomad_pydantic.LogConfig)                      |    |
| [`Template`](_build/nomad_pydantic.Template.md#nomad_pydantic.Template)                         |    |
| [`Artifact`](_build/nomad_pydantic.Artifact.md#nomad_pydantic.Artifact)                         |    |
| [`Volume`](_build/nomad_pydantic.Volume.md#nomad_pydantic.Volume)                               |    |
| [`VolumeMount`](_build/nomad_pydantic.VolumeMount.md#nomad_pydantic.VolumeMount)                |    |

## Configuration and lifecycle

| [`NomadConfiguration`](_build/nomad_pydantic.NomadConfiguration.md#nomad_pydantic.NomadConfiguration)                  | A Nomad job together with its local JSON artifact and CLI settings.   |
|------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`NomadClient`](_build/nomad_pydantic.NomadClient.md#nomad_pydantic.NomadClient)(configuration, \*[, runner, ...])     | Manage a configuration through the installed Nomad CLI.               |
| [`JobStatus`](_build/nomad_pydantic.JobStatus.md#nomad_pydantic.JobStatus)                                             |                                                                       |
| [`CommandResult`](_build/nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)(returncode, stdout, stderr)     |                                                                       |
| [`CommandRunner`](_build/nomad_pydantic.CommandRunner.md#nomad_pydantic.CommandRunner)(\*args, \*\*kwargs)             |                                                                       |
| [`SubprocessCommandRunner`](_build/nomad_pydantic.SubprocessCommandRunner.md#nomad_pydantic.SubprocessCommandRunner)() |                                                                       |
| [`NomadCommandError`](_build/nomad_pydantic.NomadCommandError.md#nomad_pydantic.NomadCommandError)(command, result)    |                                                                       |
