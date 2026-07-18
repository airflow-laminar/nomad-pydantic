# nomad_pydantic.Job

### *pydantic model* nomad_pydantic.Job

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

#### *field* task_groups *: list[[TaskGroup](nomad_pydantic.TaskGroup.md#nomad_pydantic.TaskGroup)]* *[Required]* *(alias 'TaskGroups')*

#### *field* periodic *: [PeriodicConfig](nomad_pydantic.PeriodicConfig.md#nomad_pydantic.PeriodicConfig) | None* *= None* *(alias 'Periodic')*

#### *field* stop *: bool | None* *= None* *(alias 'Stop')*

#### to_json(, indent: int | None = 2) → str

Render the JSON envelope accepted by `nomad job run -json`.

#### *classmethod* from_json(value: str | bytes) → [Job](#nomad_pydantic.Job)

Load either a Nomad JSON job envelope or a bare job object.
