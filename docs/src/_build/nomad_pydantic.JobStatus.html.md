# nomad_pydantic.JobStatus

### *pydantic model* nomad_pydantic.JobStatus

Bases: `StatusModel`

Status bundle emitted by `nomad job status -json` for one job.

#### *field* summary *: [JobSummary](nomad_pydantic.JobSummary.md#nomad_pydantic.JobSummary)* *[Required]* *(alias 'Summary')*

#### *field* allocations *: list[[AllocationStatus](nomad_pydantic.AllocationStatus.md#nomad_pydantic.AllocationStatus)]* *[Required]* *(alias 'Allocations')*

#### *field* latest_deployment *: [DeploymentStatus](nomad_pydantic.DeploymentStatus.md#nomad_pydantic.DeploymentStatus) | None* *= None* *(alias 'LatestDeployment')*

#### *field* evaluations *: list[[EvaluationStatus](nomad_pydantic.EvaluationStatus.md#nomad_pydantic.EvaluationStatus)]* *[Required]* *(alias 'Evaluations')*

#### *classmethod* from_cli(value: str | bytes) → [JobStatus](#nomad_pydantic.JobStatus)

#### *property* id *: str*

#### *property* namespace *: str*

#### *property* current_allocations *: list[[AllocationStatus](nomad_pydantic.AllocationStatus.md#nomad_pydantic.AllocationStatus)]*

#### *property* running *: bool*

#### *property* complete *: bool*

#### *property* failed *: bool*

#### *property* stopped *: bool*
