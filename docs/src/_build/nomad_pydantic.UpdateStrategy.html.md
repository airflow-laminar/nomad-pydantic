# nomad_pydantic.UpdateStrategy

### *pydantic model* nomad_pydantic.UpdateStrategy

Bases: `NomadModel`

#### *field* max_parallel *: int | None* *= None* *(alias 'MaxParallel')*

#### *field* health_check *: Literal['checks', 'task_states', 'manual'] | None* *= None* *(alias 'HealthCheck')*

#### *field* min_healthy_time *: Duration | None* *= None* *(alias 'MinHealthyTime')*

#### *field* healthy_deadline *: Duration | None* *= None* *(alias 'HealthyDeadline')*

#### *field* progress_deadline *: Duration | None* *= None* *(alias 'ProgressDeadline')*

#### *field* auto_revert *: bool | None* *= None* *(alias 'AutoRevert')*

#### *field* auto_promote *: bool | None* *= None* *(alias 'AutoPromote')*

#### *field* canary *: int | None* *= None* *(alias 'Canary')*

#### *field* stagger *: Duration | None* *= None* *(alias 'Stagger')*
