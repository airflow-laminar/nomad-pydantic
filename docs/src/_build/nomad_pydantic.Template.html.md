# nomad_pydantic.Template

### *pydantic model* nomad_pydantic.Template[[source]](../../../_modules/nomad_pydantic/models.html.md#Template)

Bases: `NomadModel`

#### *field* source_path *: str | None* *= None* *(alias 'SourcePath')*

#### *field* destination *: str* *[Required]* *(alias 'Destination')*

#### *field* embedded_tmpl *: str | None* *= None* *(alias 'EmbeddedTmpl')*

#### *field* change_mode *: Literal['noop', 'restart', 'signal', 'script'] | None* *= None* *(alias 'ChangeMode')*

#### *field* change_signal *: str | None* *= None* *(alias 'ChangeSignal')*

#### *field* perms *: str | None* *= None* *(alias 'Perms')*

#### *field* envvars *: bool | None* *= None* *(alias 'Envvars')*
