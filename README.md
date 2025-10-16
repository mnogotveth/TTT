Tornado Test Framework
Простой фреймворк для автоматического тестирования.

Быстрый старт
Установка
bash
# Создай виртуальное окружение
python -m venv venv

# Активируй (Windows)
venv\Scripts\activate

# Активируй (Linux/Mac)
source venv/bin/activate

# Установи зависимости
pip install -r requirements.txt
Запуск
bash
# Запусти все тесты
python main.py

Структура тестов
Тесты описываются в YAML файлах (tests/test_scenarios.yaml):

Результаты
После запуска создаются:

test_framework.log - детальные логи выполнения

test_report_XXXXX.json - отчет с результатами тестов

Фреймворк продолжает работу даже при ошибках в тестах