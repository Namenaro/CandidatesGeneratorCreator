from steps_model import StepsLibrary
if __name__ == "__main__":
    # Инициализация
    library = StepsLibrary()

    # Получение информации
    print("Available steps:", library.get_class_names())
    print("Filter steps:", library.get_class_names_by_type("filter"))
    print(library.get_class_parameters("Step1"))


    # Создание и выполнение шага
    params = '{"threshold": 0.7}'
    obj = library.create_instance('Step1', params)
    print(obj.run([1,2,3, 4, 5,3,2],2/500, 5/500))
    print(obj.type_of_step)
