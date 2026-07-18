# nomad_pydantic.Task

### *pydantic model* nomad_pydantic.Task

Bases: `NomadModel`

#### *field* name *: str* *[Required]* *(alias 'Name')*

#### *field* driver *: str* *[Required]* *(alias 'Driver')*

#### *field* user *: str | None* *= None* *(alias 'User')*

#### *field* config *: dict[str, Any]* *[Optional]* *(alias 'Config')*

#### *field* env *: dict[str, str]* *[Optional]* *(alias 'Env')*

#### *field* services *: list[[Service](nomad_pydantic.Service.md#nomad_pydantic.Service)]* *[Optional]* *(alias 'Services')*

#### *field* resources *: [Resources](nomad_pydantic.Resources.md#nomad_pydantic.Resources)* *[Optional]* *(alias 'Resources')*

#### *field* restart_policy *: [RestartPolicy](nomad_pydantic.RestartPolicy.md#nomad_pydantic.RestartPolicy) | None* *= None* *(alias 'RestartPolicy')*

#### *field* lifecycle *: [Lifecycle](nomad_pydantic.Lifecycle.md#nomad_pydantic.Lifecycle) | None* *= None* *(alias 'Lifecycle')*

#### *field* meta *: dict[str, str]* *[Optional]* *(alias 'Meta')*

#### *field* kill_timeout *: Duration | None* *= None* *(alias 'KillTimeout')*

#### *field* shutdown_delay *: Duration | None* *= None* *(alias 'ShutdownDelay')*

#### *field* kill_signal *: str | None* *= None* *(alias 'KillSignal')*

#### *field* log_config *: [LogConfig](nomad_pydantic.LogConfig.md#nomad_pydantic.LogConfig) | None* *= None* *(alias 'LogConfig')*

#### *field* templates *: list[[Template](nomad_pydantic.Template.md#nomad_pydantic.Template)]* *[Optional]* *(alias 'Templates')*

#### *field* artifacts *: list[[Artifact](nomad_pydantic.Artifact.md#nomad_pydantic.Artifact)]* *[Optional]* *(alias 'Artifacts')*

#### *field* volume_mounts *: list[[VolumeMount](nomad_pydantic.VolumeMount.md#nomad_pydantic.VolumeMount)]* *[Optional]* *(alias 'VolumeMounts')*
