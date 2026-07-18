from __future__ import annotations

from pathlib import Path
from typing import Any

from hydra import compose, initialize_config_dir
from omegaconf import OmegaConf
from pydantic import BaseModel, ConfigDict, Field, model_validator

from nomad_pydantic.client import CommandResult, JobStatus, NomadClient
from nomad_pydantic.models import Job


class NomadConfiguration(BaseModel):
    """A Nomad job together with its local JSON artifact and CLI settings."""

    model_config = ConfigDict(validate_assignment=True)

    job: Job
    path: Path | None = None
    working_dir: Path | None = None
    command_timeout: float | None = Field(default=60, gt=0)

    @model_validator(mode="after")
    def default_paths(self) -> NomadConfiguration:
        if self.working_dir is None:
            self.working_dir = Path.cwd() / ".nomad-pydantic" / self.job.id
        if self.path is None:
            self.path = self.working_dir / f"{self.job.id}.json"
        return self

    def to_cfg(self) -> str:
        return self.job.to_json()

    def write(self, path: str | Path | None = None) -> Path:
        destination = Path(path) if path is not None else self.path
        if destination is None:  # pragma: no cover - guarded by model validation
            raise ValueError("configuration path is not set")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(self.to_cfg() + "\n")
        self.path = destination
        return destination

    @classmethod
    def from_file(cls, path: str | Path, **values: Any) -> NomadConfiguration:
        source = Path(path)
        return cls(job=Job.from_json(source.read_text()), path=source, **values)

    @classmethod
    def load(
        cls,
        config_dir: str | Path,
        config_name: str,
        *,
        overrides: list[str] | None = None,
        **values: Any,
    ) -> NomadConfiguration:
        """Compose a Hydra YAML configuration and validate it."""

        with initialize_config_dir(config_dir=str(Path(config_dir).resolve()), version_base=None):
            composed = compose(config_name=config_name, overrides=overrides or [])
        data = OmegaConf.to_container(composed, resolve=True)
        if not isinstance(data, dict):
            raise ValueError("Nomad configuration must be a mapping")
        return cls.model_validate({**data, **values})

    def client(self, **values: Any) -> NomadClient:
        return NomadClient(self, **values)

    def register(self, **values: Any) -> CommandResult:
        return self.client(**values).register()

    def status(self, **values: Any) -> JobStatus:
        return self.client(**values).status()

    def start(self, **values: Any) -> CommandResult:
        return self.client(**values).start()

    def restart(self, **values: Any) -> CommandResult:
        return self.client(**values).restart()

    def force_periodic(self, **values: Any) -> CommandResult:
        return self.client(**values).force_periodic()

    def stop(self, *, purge: bool = False, **values: Any) -> CommandResult:
        return self.client(**values).stop(purge=purge)
