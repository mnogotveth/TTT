from abc import ABC, abstractmethod
from typing import Dict, Any
from core.contracts import TestResult

class BaseAdapter(ABC):
    @abstractmethod
    def execute(self, name: str, parameters: Dict[str, Any]) -> TestResult:
        pass