from steps_model.steps_library import StepsLibrary

# Инициализация
library = StepsLibrary()

# Получение информации
print("Available steps:", library.get_class_names())
print("Filter steps:", library.get_class_names_by_type("filter"))

# Создание и выполнение шага
params = '{"threshold": 0.7}'
result = library.run_step("Step1", [0.1, 0.6, 0.8, 0.4, 0.9], params)
print("Result:", result)