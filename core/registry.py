from typing import Dict, Type
from core.base_adapter import BaseAdapter

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, Type[BaseAdapter]] = {}
    
    def register(self, name: str, adapter_class: Type[BaseAdapter]):
        self._adapters[name] = adapter_class
    
    def get_adapter(self, name: str) -> BaseAdapter:
        if name not in self._adapters:
            raise ValueError(f"Adapter '{name}' not found")
        return self._adapters[name]()
    
    def list_adapters(self) -> list:
        return list(self._adapters.keys())

registry = AdapterRegistry()