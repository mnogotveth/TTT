import time
import psutil
from datetime import datetime
from typing import Any, Dict  
from core.base_adapter import BaseAdapter
from core.contracts import TestResult

class CpuLoadAdapter(BaseAdapter):
    def execute(self, name: str, parameters: Dict[str, Any]) -> TestResult:
        started_at = datetime.now()
        start_time = time.perf_counter()
        
        try:
            duration = parameters.get("duration", 30)
            max_cpu_load = parameters.get("max_cpu_load", 50.0)
            
            psutil.cpu_percent(interval=0.1)
            
            # Собираю показания CPU в течение указанного времени
            samples = []
            end_time = time.time() + duration
            
            while time.time() < end_time:
                cpu_percent = psutil.cpu_percent(interval=1.0)
                samples.append(cpu_percent)
                
                if time.time() >= end_time:
                    break
            
            # Вычисляю среднюю загрузку
            if samples:
                avg_cpu_load = sum(samples) / len(samples)
            else:
                avg_cpu_load = 0.0
            
            # Проверяю условие
            if avg_cpu_load <= max_cpu_load:
                status = "pass"
            else:
                status = "fail"
                
            return TestResult(
                name=name,
                status=status,
                started_at=started_at,
                duration_sec=round(time.perf_counter() - start_time, 3),
                details={
                    "average_cpu_load": round(avg_cpu_load, 2),
                    "max_allowed_load": max_cpu_load,
                    "monitoring_duration": duration,
                    "samples_collected": len(samples),
                    "min_load": round(min(samples), 2) if samples else 0,
                    "max_load": round(max(samples), 2) if samples else 0
                }
            )
            
        except Exception as e:
            return TestResult(
                name=name,
                status="error",
                started_at=started_at,
                duration_sec=round(time.perf_counter() - start_time, 3),
                details={},
                error=str(e)
            )