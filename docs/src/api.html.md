# API reference

The public API is re-exported from `nomad_pydantic`.

## Job models

| [`Job`](_build/nomad_pydantic.Job.html.md#nomad_pydantic.Job)                                        |    |
|------------------------------------------------------------------------------------------------------|----|
| [`TaskGroup`](_build/nomad_pydantic.TaskGroup.html.md#nomad_pydantic.TaskGroup)                      |    |
| [`Task`](_build/nomad_pydantic.Task.html.md#nomad_pydantic.Task)                                     |    |
| [`PeriodicConfig`](_build/nomad_pydantic.PeriodicConfig.html.md#nomad_pydantic.PeriodicConfig)       |    |
| [`Resources`](_build/nomad_pydantic.Resources.html.md#nomad_pydantic.Resources)                      |    |
| [`NetworkResource`](_build/nomad_pydantic.NetworkResource.html.md#nomad_pydantic.NetworkResource)    |    |
| [`NetworkPort`](_build/nomad_pydantic.NetworkPort.html.md#nomad_pydantic.NetworkPort)                |    |
| [`RestartPolicy`](_build/nomad_pydantic.RestartPolicy.html.md#nomad_pydantic.RestartPolicy)          |    |
| [`ReschedulePolicy`](_build/nomad_pydantic.ReschedulePolicy.html.md#nomad_pydantic.ReschedulePolicy) |    |
| [`UpdateStrategy`](_build/nomad_pydantic.UpdateStrategy.html.md#nomad_pydantic.UpdateStrategy)       |    |
| [`Service`](_build/nomad_pydantic.Service.html.md#nomad_pydantic.Service)                            |    |
| [`ServiceCheck`](_build/nomad_pydantic.ServiceCheck.html.md#nomad_pydantic.ServiceCheck)             |    |
| [`CheckRestart`](_build/nomad_pydantic.CheckRestart.html.md#nomad_pydantic.CheckRestart)             |    |
| [`Lifecycle`](_build/nomad_pydantic.Lifecycle.html.md#nomad_pydantic.Lifecycle)                      |    |
| [`LogConfig`](_build/nomad_pydantic.LogConfig.html.md#nomad_pydantic.LogConfig)                      |    |
| [`Template`](_build/nomad_pydantic.Template.html.md#nomad_pydantic.Template)                         |    |
| [`Artifact`](_build/nomad_pydantic.Artifact.html.md#nomad_pydantic.Artifact)                         |    |
| [`Volume`](_build/nomad_pydantic.Volume.html.md#nomad_pydantic.Volume)                               |    |
| [`VolumeMount`](_build/nomad_pydantic.VolumeMount.html.md#nomad_pydantic.VolumeMount)                |    |

## Configuration and lifecycle

| [`NomadConfiguration`](_build/nomad_pydantic.NomadConfiguration.html.md#nomad_pydantic.NomadConfiguration)                  | A Nomad job together with its local JSON artifact and CLI settings.   |
|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| [`NomadClient`](_build/nomad_pydantic.NomadClient.html.md#nomad_pydantic.NomadClient)(configuration, \*[, runner, ...])     | Manage a configuration through the installed Nomad CLI.               |
| [`JobStatus`](_build/nomad_pydantic.JobStatus.html.md#nomad_pydantic.JobStatus)                                             | Status bundle emitted by `nomad job status -json` for one job.        |
| [`JobSummary`](_build/nomad_pydantic.JobSummary.html.md#nomad_pydantic.JobSummary)                                          |                                                                       |
| [`TaskGroupStatus`](_build/nomad_pydantic.TaskGroupStatus.html.md#nomad_pydantic.TaskGroupStatus)                           |                                                                       |
| [`AllocationStatus`](_build/nomad_pydantic.AllocationStatus.html.md#nomad_pydantic.AllocationStatus)                        |                                                                       |
| [`DeploymentStatus`](_build/nomad_pydantic.DeploymentStatus.html.md#nomad_pydantic.DeploymentStatus)                        |                                                                       |
| [`EvaluationStatus`](_build/nomad_pydantic.EvaluationStatus.html.md#nomad_pydantic.EvaluationStatus)                        |                                                                       |
| [`CommandResult`](_build/nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)(returncode, stdout, stderr)     |                                                                       |
| [`CommandRunner`](_build/nomad_pydantic.CommandRunner.html.md#nomad_pydantic.CommandRunner)(\*args, \*\*kwargs)             |                                                                       |
| [`SubprocessCommandRunner`](_build/nomad_pydantic.SubprocessCommandRunner.html.md#nomad_pydantic.SubprocessCommandRunner)() |                                                                       |
| [`NomadCommandError`](_build/nomad_pydantic.NomadCommandError.html.md#nomad_pydantic.NomadCommandError)(command, result)    |                                                                       |
