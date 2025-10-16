import yaml
import logging
from typing import List, Dict, Any
from datetime import datetime
import json
import os

from core.contracts import TestCase, TestResult
from core.registry import registry

class TestRunner:
    def __init__(self, log_level: str = "INFO"):
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        self.results: List[TestResult] = []
    
    def setup_logging(self, log_level: str):
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('test_framework.log', encoding='utf-8')
            ]
        )
    
    def load_test_cases(self, file_path: str) -> List[TestCase]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            test_cases = []
            for test_data in data.get('tests', []):
                test_case = TestCase(
                    name=test_data['name'],
                    adapter=test_data['adapter'],
                    parameters=test_data.get('parameters', {})
                )
                test_cases.append(test_case)
            
            return test_cases
            
        except Exception as e:
            self.logger.error(f"Ошибка загрузки тест-кейсов: {e}")
            raise
    
    def run_tests(self, test_cases: List[TestCase]) -> List[TestResult]:
        self.logger.info(f"Запуск {len(test_cases)} тестов")
        
        for test_case in test_cases:
            self.logger.info(f"Выполнение теста: {test_case.name}")
            
            try:
                adapter = registry.get_adapter(test_case.adapter)
                result = adapter.execute(test_case.name, test_case.parameters)
                self.results.append(result)
                
                if result.status == "pass":
                    self.logger.info(f"✓ Тест '{test_case.name}' пройден")
                elif result.status == "fail":
                    self.logger.warning(f"✗ Тест '{test_case.name}' не пройден")
                else:
                    self.logger.error(f"⚠ Тест '{test_case.name}' завершился с ошибкой: {result.error}")
                    
            except Exception as e:
                self.logger.error(f"Критическая ошибка при выполнении теста '{test_case.name}': {e}")
                error_result = TestResult(
                    name=test_case.name,
                    status="error",
                    started_at=datetime.now(),
                    duration_sec=0,
                    details={},
                    error=f"Ошибка инициализации адаптера: {str(e)}"
                )
                self.results.append(error_result)
        
        return self.results
    
    def generate_report(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = len([r for r in self.results if r.status == "pass"])
        failed = len([r for r in self.results if r.status == "fail"])
        errors = len([r for r in self.results if r.status == "error"])
        
        report = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "success_rate": round(passed / total * 100, 2) if total > 0 else 0
            },
            "results": [result.to_dict() for result in self.results],
            "timestamp": datetime.now().isoformat()
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], format: str = "json"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            report_file = f"test_report_{timestamp}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Отчет сохранен в {report_file}")
        
        return report_file