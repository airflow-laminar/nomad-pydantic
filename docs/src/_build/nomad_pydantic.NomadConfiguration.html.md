# nomad_pydantic.NomadConfiguration

### *pydantic model* nomad_pydantic.NomadConfiguration

Bases: `BaseModel`

A Nomad job together with its local JSON artifact and CLI settings.

#### *field* job *: [Job](nomad_pydantic.Job.md#nomad_pydantic.Job)* *[Required]*

#### *field* path *: Path | None* *= None*

#### *field* working_dir *: Path | None* *= None*

#### *field* command_timeout *: float | None* *= 60*

#### to_cfg() → str

#### write(path: str | Path | None = None) → Path

#### *classmethod* from_file(path: str | Path, \*\*values: Any) → [NomadConfiguration](#nomad_pydantic.NomadConfiguration)

#### *classmethod* load(config_dir: str | Path, config_name: str, , overrides: list[str] | None = None, \*\*values: Any) → [NomadConfiguration](#nomad_pydantic.NomadConfiguration)

Compose a Hydra YAML configuration and validate it.

#### client(\*\*values: Any) → [NomadClient](nomad_pydantic.NomadClient.md#nomad_pydantic.NomadClient)

#### register(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)

#### status(\*\*values: Any) → [JobStatus](nomad_pydantic.JobStatus.md#nomad_pydantic.JobStatus)

#### start(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)

#### restart(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)

#### force_periodic(\*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)

#### stop(, purge: bool = False, \*\*values: Any) → [CommandResult](nomad_pydantic.CommandResult.md#nomad_pydantic.CommandResult)
