import argparse
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.test_runner import TestRunner
import adapters

def main():
    parser = argparse.ArgumentParser(description='Tornado Test Framework')
    parser.add_argument('--tests', '-t', default='tests/test_scenarios.yaml',
                       help='Путь к YAML файлу с тестами (по умолчанию: tests/test_scenarios.yaml)')
    parser.add_argument('--log-level', '-l', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Уровень логирования')
    parser.add_argument('--report-format', '-r', default='json',
                       choices=['json'],
                       help='Формат отчета')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.tests):
        print(f"Ошибка: файл с тестами '{args.tests}' не найден")
        sys.exit(1)
    
    try:
        runner = TestRunner(log_level=args.log_level)
        test_cases = runner.load_test_cases(args.tests)
        print(f"Загружено {len(test_cases)} тест-кейсов")
        results = runner.run_tests(test_cases)
        
        # Генерирую и сохраняю отчет
        report = runner.generate_report()
        report_file = runner.save_report(report, format=args.report_format)
        summary = report['summary']
        print(f"\n=== СВОДКА ===")
        print(f"Всего тестов: {summary['total']}")
        print(f"Пройдено: {summary['passed']}")
        print(f"Не пройдено: {summary['failed']}")
        print(f"Ошибок: {summary['errors']}")
        print(f"Успешность: {summary['success_rate']}%")
        print(f"Отчет: {report_file}")
        
        if summary['failed'] > 0 or summary['errors'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()