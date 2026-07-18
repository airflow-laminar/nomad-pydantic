# nomad_pydantic.TaskGroup

### *pydantic model* nomad_pydantic.TaskGroup

Bases: `NomadModel`

#### *field* name *: str* *[Required]* *(alias 'Name')*

#### *field* count *: int* *= 1* *(alias 'Count')*

#### *field* tasks *: list[[Task](nomad_pydantic.Task.md#nomad_pydantic.Task)]* *[Required]* *(alias 'Tasks')*

#### *field* restart_policy *: [RestartPolicy](nomad_pydantic.RestartPolicy.md#nomad_pydantic.RestartPolicy) | None* *= None* *(alias 'RestartPolicy')*

#### *field* reschedule_policy *: [ReschedulePolicy](nomad_pydantic.ReschedulePolicy.md#nomad_pydantic.ReschedulePolicy) | None* *= None* *(alias 'ReschedulePolicy')*

#### *field* update *: [UpdateStrategy](nomad_pydantic.UpdateStrategy.md#nomad_pydantic.UpdateStrategy) | None* *= None* *(alias 'Update')*

#### *field* networks *: list[[NetworkResource](nomad_pydantic.NetworkResource.md#nomad_pydantic.NetworkResource)]* *[Optional]* *(alias 'Networks')*

#### *field* services *: list[[Service](nomad_pydantic.Service.md#nomad_pydantic.Service)]* *[Optional]* *(alias 'Services')*

#### *field* meta *: dict[str, str]* *[Optional]* *(alias 'Meta')*

#### *field* volumes *: dict[str, [Volume](nomad_pydantic.Volume.md#nomad_pydantic.Volume)]* *[Optional]* *(alias 'Volumes')*

#### *field* shutdown_delay *: Duration | None* *= None* *(alias 'ShutdownDelay')*

#### *field* max_client_disconnect *: Duration | None* *= None* *(alias 'MaxClientDisconnect')*

#### *field* max_run_duration *: Duration | None* *= None* *(alias 'MaxRunDuration')*
