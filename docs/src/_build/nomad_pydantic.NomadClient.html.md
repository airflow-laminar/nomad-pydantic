# nomad_pydantic.NomadClient

### *class* nomad_pydantic.NomadClient(configuration: [NomadConfiguration](nomad_pydantic.NomadConfiguration.html.md#nomad_pydantic.NomadConfiguration), , runner: [CommandRunner](nomad_pydantic.CommandRunner.html.md#nomad_pydantic.CommandRunner) | None = None, executable: str = 'nomad')[[source]](../../../_modules/nomad_pydantic/client.html.md#NomadClient)

Bases: `object`

Manage a configuration through the installed Nomad CLI.

#### \_\_init_\_(configuration: [NomadConfiguration](nomad_pydantic.NomadConfiguration.html.md#nomad_pydantic.NomadConfiguration), , runner: [CommandRunner](nomad_pydantic.CommandRunner.html.md#nomad_pydantic.CommandRunner) | None = None, executable: str = 'nomad') → None[[source]](../../../_modules/nomad_pydantic/client.html.md#NomadClient.__init__)

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
