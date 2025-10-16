import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.registry import registry
try:
    import adapters
    print("Адаптеры импортированы")
except Exception as e:
    print(f"Ошибка импорта адаптеров: {e}")

print("Зарегистрированные адаптеры:", registry.list_adapters())