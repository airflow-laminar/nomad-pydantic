# nomad_pydantic.Job

### *pydantic model* nomad_pydantic.Job[[source]](../../../_modules/nomad_pydantic/models.html.md#Job)

Bases: `NomadModel`

#### *field* id *: str* *[Required]* *(alias 'ID')*

#### *field* name *: str | None* *= None* *(alias 'Name')*

#### *field* type *: Literal['service', 'batch', 'system', 'sysbatch']* *= 'service'* *(alias 'Type')*

#### *field* region *: str | None* *= None* *(alias 'Region')*

#### *field* namespace *: str | None* *= None* *(alias 'Namespace')*

#### *field* node_pool *: str | None* *= None* *(alias 'NodePool')*

#### *field* priority *: int | None* *= None* *(alias 'Priority')*

#### *field* all_at_once *: bool | None* *= None* *(alias 'AllAtOnce')*

#### *field* datacenters *: list[str]* *[Optional]* *(alias 'Datacenters')*

#### *field* meta *: dict[str, str]* *[Optional]* *(alias 'Meta')*

#### *field* task_groups *: list[[TaskGroup](nomad_pydantic.TaskGroup.html.md#nomad_pydantic.TaskGroup)]* *[Required]* *(alias 'TaskGroups')*

#### *field* periodic *: [PeriodicConfig](nomad_pydantic.PeriodicConfig.html.md#nomad_pydantic.PeriodicConfig) | None* *= None* *(alias 'Periodic')*

#### *field* stop *: bool | None* *= None* *(alias 'Stop')*

#### to_json(, indent: int | None = 2) → str[[source]](../../../_modules/nomad_pydantic/models.html.md#Job.to_json)

Render the JSON envelope accepted by `nomad job run -json`.

#### *classmethod* from_json(value: str | bytes) → [Job](#nomad_pydantic.Job)[[source]](../../../_modules/nomad_pydantic/models.html.md#Job.from_json)

Load either a Nomad JSON job envelope or a bare job object.
