# nomad_pydantic.NetworkResource

### *pydantic model* nomad_pydantic.NetworkResource[[source]](../../../_modules/nomad_pydantic/models.html.md#NetworkResource)

Bases: `NomadModel`

#### *field* mode *: str | None* *= None* *(alias 'Mode')*

#### *field* mbits *: int | None* *= None* *(alias 'MBits')*

#### *field* hostname *: str | None* *= None* *(alias 'Hostname')*

#### *field* dynamic_ports *: list[[NetworkPort](nomad_pydantic.NetworkPort.html.md#nomad_pydantic.NetworkPort)]* *[Optional]* *(alias 'DynamicPorts')*

#### *field* reserved_ports *: list[[NetworkPort](nomad_pydantic.NetworkPort.html.md#nomad_pydantic.NetworkPort)]* *[Optional]* *(alias 'ReservedPorts')*

#### *field* dns *: dict[str, Any] | None* *= None* *(alias 'DNS')*
