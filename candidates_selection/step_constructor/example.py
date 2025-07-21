from candidates_selection.step_constructor import StepsLibrary
from settings import TYPES_OF_STEP


def examples_steps():
    # Инициализация
    library = StepsLibrary()

    # Получение информации из библиотеки шагов:
    print("Какие типы шагов описаны в библиотеке:", library.get_class_names())
    print("Типы шагов по отбору кандидатов:", library.get_class_names_by_type(TYPES_OF_STEP.candidates))
    print("Для заданного типа шага получить умолчательный json под редактирование",
          library.get_class_parameters("TestStepSignal"))

    # Пример создания и выполнения шага
    params = '{"threshold": 0.7}'
    obj = library.create_instance('TestStepSignal', params)
    print("результат выполнения шага ", obj.run([0, 1, 2, 3, 4, 5, 3, 2], 2 / 500, 5 / 500))
    print("тип шага ", obj.type_of_step)

if __name__ == "__main__":
    examples_steps()
