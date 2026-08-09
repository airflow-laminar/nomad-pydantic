# nomad_pydantic.ReschedulePolicy

### *pydantic model* nomad_pydantic.ReschedulePolicy[[source]](../../../_modules/nomad_pydantic/models.html.md#ReschedulePolicy)

Bases: `NomadModel`

#### *field* attempts *: int | None* *= None* *(alias 'Attempts')*

#### *field* interval *: Duration | None* *= None* *(alias 'Interval')*

#### *field* delay *: Duration | None* *= None* *(alias 'Delay')*

#### *field* delay_function *: Literal['constant', 'exponential', 'fibonacci'] | None* *= None* *(alias 'DelayFunction')*

#### *field* max_delay *: Duration | None* *= None* *(alias 'MaxDelay')*

#### *field* unlimited *: bool | None* *= None* *(alias 'Unlimited')*
