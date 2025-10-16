import json
import time
from datetime import datetime
from typing import Any, Dict
import requests
import pytz
from core.base_adapter import BaseAdapter
from core.contracts import TestResult

class NetTimeAdapter(BaseAdapter):
    def execute(self, name: str, parameters: Dict[str, Any]) -> TestResult:
        started_at = datetime.now()
        start_time = time.perf_counter()
        
        try:
            url = parameters["url"]
            tz = parameters.get("tz", "Asia/Novosibirsk")
            tolerance_sec = parameters.get("tolerance_sec", 5)
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'formatted' in data:
                # Формат: "16/10/2025 12:35:13"
                server_time_str = data['formatted']
                server_dt = datetime.strptime(server_time_str, "%d/%m/%Y %H:%M:%S")
            elif 'now' in data:
                # Альтернативный формат, если есть поле 'now'
                server_time_str = data['now']
                server_dt = datetime.strptime(server_time_str, "%d/%m/%Y %H:%M:%S")
            else:
                raise ValueError("Неизвестный формат ответа API")
            try:
                tz_obj = pytz.timezone(tz)
            except pytz.UnknownTimeZoneError:
                # Если зона не найдена, используем UTC+7
                tz_obj = pytz.timezone('Asia/Krasnoyarsk') 
            
            server_dt = tz_obj.localize(server_dt)
            local_dt = datetime.now(tz_obj)
            
            time_diff = abs((server_dt - local_dt).total_seconds())
            
            # Проверяю условие
            if time_diff <= tolerance_sec:
                status = "pass"
            else:
                status = "fail"
                
            return TestResult(
                name=name,
                status=status,
                started_at=started_at,
                duration_sec=round(time.perf_counter() - start_time, 3),
                details={
                    "time_diff_seconds": time_diff,
                    "tolerance_seconds": tolerance_sec,
                    "server_time": server_dt.isoformat(),
                    "local_time": local_dt.isoformat(),
                    "timezone": tz,
                    "url": url
                }
            )
            
        except Exception as e:
            return TestResult(
                name=name,
                status="error",
                started_at=started_at,
                duration_sec=round(time.perf_counter() - start_time, 3),
                details={"url": parameters.get("url")},
                error=str(e)
            )