import json
import inspect
import importlib
from typing import Dict, Type, List, Any, Optional
import pkgutil
from .step import Step


class StepsLibrary:
    def __init__(self):
        """Автоматически загружает все шаги из steps_model.steps"""
        self._classes: Dict[str, Type[Step]] = {}
        self._type_index: Dict[str, List[str]] = {}
        self._load_classes()

    def _load_classes(self) -> None:
        """Загружает все классы шагов из модулей в пакете steps"""
        try:
            steps_pkg = importlib.import_module('steps_model.steps')

            # Получаем все подмодули в пакете steps
            for module_info in pkgutil.iter_modules(steps_pkg.__path__):
                module = importlib.import_module(f'steps_model.steps.{module_info.name}')

                # Находим все классы-наследники Step
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Step) :
                        self._classes[name] = obj
                        if hasattr(obj, 'type_of_step'):
                            self._add_to_type_index(obj, name)

        except ImportError as e:
            raise ImportError(f"Failed to load steps package: {e}")

    def _add_to_type_index(self, cls: Type[Step], class_name: str) -> None:
        """Добавляет класс в индекс по его типу"""
        type_name = cls.type_of_step
        self._type_index.setdefault(type_name, []).append(class_name)

    def get_class_names(self) -> List[str]:
        """Возвращает список всех загруженных классов шагов"""
        return list(self._classes.keys())

    def get_class_names_by_type(self, type_of_step: str) -> List[str]:
        """Возвращает классы указанного типа"""
        return self._type_index.get(type_of_step, [])

    def get_class_comment(self, class_name: str) -> Optional[str]:
        """Возвращает комментарий класса, если есть"""
        if class_name not in self._classes:
            raise ValueError(f"Class '{class_name}' not found")
        return getattr(self._classes[class_name], 'comment', None)

    def get_class_parameters(self, class_name: str) -> str:
        """Возвращает параметры конструктора в формате JSON"""
        if class_name not in self._classes:
            raise ValueError(f"Class '{class_name}' not found")

        signature = inspect.signature(self._classes[class_name].__init__)
        parameters = {}

        for name, param in signature.parameters.items():
            # Пропускаем служебные параметры
            if name in ['self', 'args', 'kwargs']:
                continue

            # Добавляем только параметры с умолчательными значениями
            if param.default is not inspect.Parameter.empty:
                parameters[name] = param.default

        return parameters

    def create_instance(self, class_name: str, parameters_json: str = '{}') -> Step:
        """Создает экземпляр класса с заданными параметрами"""
        if class_name not in self._classes:
            raise ValueError(f"Class '{class_name}' not found")

        try:
            params = json.loads(parameters_json)
            return self._classes[class_name](**params)
        except Exception as e:
            raise ValueError(f"Failed to create instance: {e}")

    def run_step(self, class_name: str, signal: Any, parameters_json: str = '{}') -> Any:
        """Создает и выполняет шаг"""
        instance = self.create_instance(class_name, parameters_json)
        return instance.run(signal)