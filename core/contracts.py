from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from datetime import datetime
import json

@dataclass
class TestResult:
    name: str
    status: str 
    started_at: datetime
    duration_sec: float
    details: Dict[str, Any]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['started_at'] = self.started_at.isoformat()
        return result

@dataclass
class TestCase:
    name: str
    adapter: str
    parameters: Dict[str, Any]