# nomad_pydantic.JobStatus

### *pydantic model* nomad_pydantic.JobStatus[[source]](../../../_modules/nomad_pydantic/client.html.md#JobStatus)

Bases: `StatusModel`

Status bundle emitted by `nomad job status -json` for one job.

#### *field* summary *: [JobSummary](nomad_pydantic.JobSummary.html.md#nomad_pydantic.JobSummary)* *[Required]* *(alias 'Summary')*

#### *field* allocations *: list[[AllocationStatus](nomad_pydantic.AllocationStatus.html.md#nomad_pydantic.AllocationStatus)]* *[Required]* *(alias 'Allocations')*

#### *field* latest_deployment *: [DeploymentStatus](nomad_pydantic.DeploymentStatus.html.md#nomad_pydantic.DeploymentStatus) | None* *= None* *(alias 'LatestDeployment')*

#### *field* evaluations *: list[[EvaluationStatus](nomad_pydantic.EvaluationStatus.html.md#nomad_pydantic.EvaluationStatus)]* *[Required]* *(alias 'Evaluations')*

#### *classmethod* from_cli(value: str | bytes) → [JobStatus](#nomad_pydantic.JobStatus)[[source]](../../../_modules/nomad_pydantic/client.html.md#JobStatus.from_cli)

#### *property* id *: str*

#### *property* namespace *: str*

#### *property* current_allocations *: list[[AllocationStatus](nomad_pydantic.AllocationStatus.html.md#nomad_pydantic.AllocationStatus)]*

#### *property* running *: bool*

#### *property* complete *: bool*

#### *property* failed *: bool*

#### *property* stopped *: bool*
