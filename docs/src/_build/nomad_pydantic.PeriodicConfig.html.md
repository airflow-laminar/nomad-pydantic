# nomad_pydantic.PeriodicConfig

### *pydantic model* nomad_pydantic.PeriodicConfig

Bases: `NomadModel`

#### *field* crons *: list[str]* *[Required]* *(alias 'Specs')*

#### *field* spec_type *: Literal['cron']* *= 'cron'* *(alias 'SpecType')*

#### *field* prohibit_overlap *: bool* *= False* *(alias 'ProhibitOverlap')*

#### *field* time_zone *: str* *= 'UTC'* *(alias 'TimeZone')*

#### *field* enabled *: bool* *= True* *(alias 'Enabled')*
