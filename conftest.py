# allure_doqa_patch.py
import json
from pathlib import Path
from allure_pytest.listener import AllureListener


def _patched_write(self, data: dict, path: Path):
    """Рекурсивно добавляет пробел после каждого ключа словаря"""

    def add_space_to_keys(obj):
        if isinstance(obj, dict):
            return {f"{k} ": add_space_to_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [add_space_to_keys(item) for item in obj]
        return obj

    # Модифицируем данные только если это словарь
    if isinstance(data, dict):
        data = add_space_to_keys(data)

    # ВАЖНО: Записываем модифицированный JSON вручную,
    # так как мы полностью переопределяем метод
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def pytest_configure(config):
    """Применяем патч при старте pytest"""
    AllureListener._write = _patched_write



pytest_plugins = (
    "fixtures.browsers",
    "fixtures.pages"
)