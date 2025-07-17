from steps_model.steps_library import StepsLibrary

# Инициализация
library = StepsLibrary()

# Получение информации
print("Available steps:", library.get_class_names())
print("Filter steps:", library.get_class_names_by_type("filter"))
print(library.get_class_parameters("Step1"))


# Создание и выполнение шага
params = '{"threshold": 0.7}'
obj = library.create_instance('Step1', params)
print(obj.run([1,2,3]))
print(obj.type_of_step)

result = library.run_step("Step1", [0.1, 0.6, 0.8, 0.4, 0.9], params)
print("Result:", result)