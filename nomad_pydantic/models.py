from __future__ import annotations

import json
import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator


def _pascal_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


class NomadModel(BaseModel):
    """Base model using the field names from Nomad's JSON API as aliases."""

    model_config = ConfigDict(alias_generator=_pascal_case, populate_by_name=True, extra="forbid", validate_assignment=True)


_DURATION_PART = re.compile(r"(\d+(?:\.\d+)?)(ns|us|µs|ms|s|m|h)")
_DURATION_FACTORS = {"ns": 1, "us": 1_000, "µs": 1_000, "ms": 1_000_000, "s": 1_000_000_000, "m": 60_000_000_000, "h": 3_600_000_000_000}


def _parse_duration(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    position = 0
    nanoseconds = 0.0
    for match in _DURATION_PART.finditer(value):
        if match.start() != position:
            raise ValueError(f"invalid Nomad duration: {value}")
        nanoseconds += float(match.group(1)) * _DURATION_FACTORS[match.group(2)]
        position = match.end()
    if position != len(value) or not value:
        raise ValueError(f"invalid Nomad duration: {value}")
    return int(nanoseconds)


Duration = Annotated[int, BeforeValidator(_parse_duration)]


def _without_empty_collections(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: cleaned for key, item in value.items() if (cleaned := _without_empty_collections(item)) not in ({}, [])}
    if isinstance(value, list):
        return [cleaned for item in value if (cleaned := _without_empty_collections(item)) not in ({}, [])]
    return value


class NetworkPort(NomadModel):
    label: str
    value: int | None = None
    to: int | None = None
    host_network: str | None = None
    ignore_collision: bool | None = None


class NetworkResource(NomadModel):
    mode: str | None = None
    mbits: int | None = Field(default=None, alias="MBits")
    hostname: str | None = None
    dynamic_ports: list[NetworkPort] = Field(default_factory=list)
    reserved_ports: list[NetworkPort] = Field(default_factory=list)
    dns: dict[str, Any] | None = Field(default=None, alias="DNS")


class Resources(NomadModel):
    cpu: int | None = Field(default=None, alias="CPU")
    cores: int | None = None
    memory_mb: int | None = Field(default=None, alias="MemoryMB")
    memory_max_mb: int | None = Field(default=None, alias="MemoryMaxMB")
    disk_mb: int | None = Field(default=None, alias="DiskMB")
    networks: list[NetworkResource] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_compute(self) -> Resources:
        if self.cpu is not None and self.cores is not None:
            raise ValueError("cpu and cores are mutually exclusive")
        return self


class RestartPolicy(NomadModel):
    attempts: int | None = None
    interval: Duration | None = None
    delay: Duration | None = None
    mode: Literal["delay", "fail"] | None = None
    render_templates: bool | None = None


class ReschedulePolicy(NomadModel):
    attempts: int | None = None
    interval: Duration | None = None
    delay: Duration | None = None
    delay_function: Literal["constant", "exponential", "fibonacci"] | None = None
    max_delay: Duration | None = None
    unlimited: bool | None = None


class UpdateStrategy(NomadModel):
    max_parallel: int | None = None
    health_check: Literal["checks", "task_states", "manual"] | None = None
    min_healthy_time: Duration | None = None
    healthy_deadline: Duration | None = None
    progress_deadline: Duration | None = None
    auto_revert: bool | None = None
    auto_promote: bool | None = None
    canary: int | None = None
    stagger: Duration | None = None


class PeriodicConfig(NomadModel):
    crons: list[str] = Field(alias="Specs")
    spec_type: Literal["cron"] = "cron"
    prohibit_overlap: bool = False
    time_zone: str = "UTC"
    enabled: bool = True


class CheckRestart(NomadModel):
    limit: int | None = None
    grace: Duration | None = None
    ignore_warnings: bool | None = None


class ServiceCheck(NomadModel):
    name: str | None = None
    type: Literal["grpc", "http", "script", "tcp"]
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    path: str | None = None
    protocol: str | None = None
    port_label: str | None = None
    interval: Duration | None = None
    timeout: Duration | None = None
    method: str | None = None
    header: dict[str, list[str]] = Field(default_factory=dict)
    body: str | None = None
    tls_skip_verify: bool | None = Field(default=None, alias="TLSSkipVerify")
    grpc_service: str | None = Field(default=None, alias="GRPCService")
    grpc_use_tls: bool | None = Field(default=None, alias="GRPCUseTLS")
    address_mode: str | None = None
    on_update: str | None = None
    check_restart: CheckRestart | None = None


class Service(NomadModel):
    name: str | None = None
    provider: Literal["consul", "nomad"] | None = None
    port_label: str | None = None
    address_mode: str | None = None
    tags: list[str] = Field(default_factory=list)
    canary_tags: list[str] = Field(default_factory=list)
    meta: dict[str, str] = Field(default_factory=dict)
    checks: list[ServiceCheck] = Field(default_factory=list)


class Lifecycle(NomadModel):
    hook: Literal["prestart", "poststart", "poststop"]
    sidecar: bool = False


class LogConfig(NomadModel):
    max_files: int | None = None
    max_file_size_mb: int | None = Field(default=None, alias="MaxFileSizeMB")
    disabled: bool | None = None


class Template(NomadModel):
    source_path: str | None = None
    destination: str
    embedded_tmpl: str | None = None
    change_mode: Literal["noop", "restart", "signal", "script"] | None = None
    change_signal: str | None = None
    perms: str | None = None
    envvars: bool | None = None


class Artifact(NomadModel):
    getter_source: str
    relative_dest: str | None = None
    getter_mode: str | None = None
    getter_options: dict[str, str] = Field(default_factory=dict)
    getter_headers: dict[str, str] = Field(default_factory=dict)


class VolumeMount(NomadModel):
    volume: str
    destination: str
    read_only: bool = False
    propagation_mode: str | None = None
    selinux_label: str | None = Field(default=None, alias="SELinuxLabel")


class Volume(NomadModel):
    type: Literal["csi", "host"]
    source: str
    read_only: bool = False
    access_mode: str | None = None
    attachment_mode: str | None = None
    per_alloc: bool | None = None
    sticky: bool | None = None


class Task(NomadModel):
    name: str
    driver: str
    user: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    env: dict[str, str] = Field(default_factory=dict)
    services: list[Service] = Field(default_factory=list)
    resources: Resources = Field(default_factory=Resources)
    restart_policy: RestartPolicy | None = None
    lifecycle: Lifecycle | None = None
    meta: dict[str, str] = Field(default_factory=dict)
    kill_timeout: Duration | None = None
    shutdown_delay: Duration | None = None
    kill_signal: str | None = None
    log_config: LogConfig | None = None
    templates: list[Template] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    volume_mounts: list[VolumeMount] = Field(default_factory=list)


class TaskGroup(NomadModel):
    name: str
    count: int = 1
    tasks: list[Task]
    restart_policy: RestartPolicy | None = None
    reschedule_policy: ReschedulePolicy | None = None
    update: UpdateStrategy | None = None
    networks: list[NetworkResource] = Field(default_factory=list)
    services: list[Service] = Field(default_factory=list)
    meta: dict[str, str] = Field(default_factory=dict)
    volumes: dict[str, Volume] = Field(default_factory=dict)
    shutdown_delay: Duration | None = None
    max_client_disconnect: Duration | None = None
    max_run_duration: Duration | None = None

    @model_validator(mode="after")
    def validate_tasks(self) -> TaskGroup:
        names = [task.name for task in self.tasks]
        if not names:
            raise ValueError("a task group must contain at least one task")
        if len(names) != len(set(names)):
            raise ValueError("task names must be unique within a task group")
        return self


class Job(NomadModel):
    id: str = Field(alias="ID")
    name: str | None = None
    type: Literal["service", "batch", "system", "sysbatch"] = "service"
    region: str | None = None
    namespace: str | None = None
    node_pool: str | None = None
    priority: int | None = Field(default=None, ge=1, le=100)
    all_at_once: bool | None = None
    datacenters: list[str] = Field(default_factory=list)
    meta: dict[str, str] = Field(default_factory=dict)
    task_groups: list[TaskGroup]
    periodic: PeriodicConfig | None = None
    stop: bool | None = None

    @model_validator(mode="after")
    def validate_job(self) -> Job:
        if self.name is None:
            self.name = self.id
        if not self.task_groups:
            raise ValueError("a job must contain at least one task group")
        names = [group.name for group in self.task_groups]
        if len(names) != len(set(names)):
            raise ValueError("task group names must be unique within a job")
        if self.periodic is not None and self.type not in {"batch", "sysbatch"}:
            raise ValueError("periodic jobs must use type batch or sysbatch")
        return self

    def to_json(self, *, indent: int | None = 2) -> str:
        """Render the JSON envelope accepted by ``nomad job run -json``."""

        data = _without_empty_collections(self.model_dump(by_alias=True, exclude_none=True))
        return json.dumps({"Job": data}, indent=indent)

    @classmethod
    def from_json(cls, value: str | bytes) -> Job:
        """Load either a Nomad JSON job envelope or a bare job object."""

        data = json.loads(value)
        return cls.model_validate(data.get("Job", data))
