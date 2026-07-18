# nomad_pydantic.NomadClient

### *class* nomad_pydantic.NomadClient(configuration: [NomadConfiguration](nomad_pydantic.NomadConfiguration.md#nomad_pydantic.NomadConfiguration), , runner: [CommandRunner](nomad_pydantic.CommandRunner.md#nomad_pydantic.CommandRunner) | None = None, executable: str = 'nomad')

Bases: `object`

Manage a configuration through the installed Nomad CLI.

#### \_\_init_\_(configuration: [NomadConfiguration](nomad_pydantic.NomadConfiguration.md#nomad_pydantic.NomadConfiguration), , runner: [CommandRunner](nomad_pydantic.CommandRunner.md#nomad_pydantic.CommandRunner) | None = None, executable: str = 'nomad') → None

### Methods

| [`__init__`](#nomad_pydantic.NomadClient.__init__)(configuration, \*[, runner, executable])   |    |
|-----------------------------------------------------------------------------------------------|----|
| `force_periodic`()                                                                            |    |
| `register`()                                                                                  |    |
| `restart`()                                                                                   |    |
| `start`()                                                                                     |    |
| `status`()                                                                                    |    |
| `stop`(\*[, purge])                                                                           |    |
| `validate`()                                                                                  |    |
