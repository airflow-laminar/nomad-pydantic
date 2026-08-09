# nomad_pydantic.NomadConfiguration

### *pydantic model* nomad_pydantic.NomadConfiguration[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration)

Bases: `BaseModel`

A Nomad job together with its local JSON artifact and CLI settings.

#### *field* job *: [Job](nomad_pydantic.Job.html.md#nomad_pydantic.Job)* *[Required]*

#### *field* path *: Path | None* *= None*

#### *field* working_dir *: Path | None* *= None*

#### *field* command_timeout *: float | None* *= 60*

#### to_cfg() → str[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.to_cfg)

#### write(path: str | Path | None = None) → Path[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.write)

#### *classmethod* from_file(path: str | Path, \*\*values: Any) → [NomadConfiguration](#nomad_pydantic.NomadConfiguration)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.from_file)

#### *classmethod* load(config_dir: str | Path, config_name: str, , overrides: list[str] | None = None, \*\*values: Any) → [NomadConfiguration](#nomad_pydantic.NomadConfiguration)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.load)

Compose a Hydra YAML configuration and validate it.

#### client(\*\*values: Any) → [NomadClient](nomad_pydantic.NomadClient.html.md#nomad_pydantic.NomadClient)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.client)

#### register(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.register)

#### status(\*\*values: Any) → [JobStatus](nomad_pydantic.JobStatus.html.md#nomad_pydantic.JobStatus)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.status)

#### start(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.start)

#### restart(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.restart)

#### force_periodic(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.force_periodic)

#### stop(, purge: bool = False, \*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.html.md#nomad_pydantic.CommandResult)[[source]](../../../_modules/nomad_pydantic/config.html.md#NomadConfiguration.stop)
