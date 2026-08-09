# nomad_pydantic.Service

### *pydantic model* nomad_pydantic.Service[[source]](../../../_modules/nomad_pydantic/models.html.md#Service)

Bases: `NomadModel`

#### *field* name *: str | None* *= None* *(alias 'Name')*

#### *field* provider *: Literal['consul', 'nomad'] | None* *= None* *(alias 'Provider')*

#### *field* port_label *: str | None* *= None* *(alias 'PortLabel')*

#### *field* address_mode *: str | None* *= None* *(alias 'AddressMode')*

#### *field* tags *: list[str]* *[Optional]* *(alias 'Tags')*

#### *field* canary_tags *: list[str]* *[Optional]* *(alias 'CanaryTags')*

#### *field* meta *: dict[str, str]* *[Optional]* *(alias 'Meta')*

#### *field* checks *: list[[ServiceCheck](nomad_pydantic.ServiceCheck.html.md#nomad_pydantic.ServiceCheck)]* *[Optional]* *(alias 'Checks')*
