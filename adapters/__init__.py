from .net_time_adapter import NetTimeAdapter
from .cpu_load_adapter import CpuLoadAdapter
from core.registry import registry

registry.register("net_time", NetTimeAdapter)
registry.register("cpu_load", CpuLoadAdapter)