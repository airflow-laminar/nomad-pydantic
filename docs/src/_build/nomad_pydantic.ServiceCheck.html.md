# nomad_pydantic.ServiceCheck

### *pydantic model* nomad_pydantic.ServiceCheck

Bases: `NomadModel`

#### *field* name *: str | None* *= None* *(alias 'Name')*

#### *field* type *: Literal['grpc', 'http', 'script', 'tcp']* *[Required]* *(alias 'Type')*

#### *field* command *: str | None* *= None* *(alias 'Command')*

#### *field* args *: list[str]* *[Optional]* *(alias 'Args')*

#### *field* path *: str | None* *= None* *(alias 'Path')*

#### *field* protocol *: str | None* *= None* *(alias 'Protocol')*

#### *field* port_label *: str | None* *= None* *(alias 'PortLabel')*

#### *field* interval *: Duration | None* *= None* *(alias 'Interval')*

#### *field* timeout *: Duration | None* *= None* *(alias 'Timeout')*

#### *field* method *: str | None* *= None* *(alias 'Method')*

#### *field* header *: dict[str, list[str]]* *[Optional]* *(alias 'Header')*

#### *field* body *: str | None* *= None* *(alias 'Body')*

#### *field* tls_skip_verify *: bool | None* *= None* *(alias 'TLSSkipVerify')*

#### *field* grpc_service *: str | None* *= None* *(alias 'GRPCService')*

#### *field* grpc_use_tls *: bool | None* *= None* *(alias 'GRPCUseTLS')*

#### *field* address_mode *: str | None* *= None* *(alias 'AddressMode')*

#### *field* on_update *: str | None* *= None* *(alias 'OnUpdate')*

#### *field* check_restart *: [CheckRestart](nomad_pydantic.CheckRestart.md#nomad_pydantic.CheckRestart) | None* *= None* *(alias 'CheckRestart')*
