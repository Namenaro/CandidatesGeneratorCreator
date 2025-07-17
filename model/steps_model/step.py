from typing import Any

class Step:
    """Базовый класс для всех шагов обработки"""
    def run(self, signal: Any) -> Any:
        """Основной метод обработки сигнала"""
        raise NotImplementedError("Each step must implement run() method")