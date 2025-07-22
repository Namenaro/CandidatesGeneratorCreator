import json


def extract_and_save_json(input_filename, name_key, output_filename=None):
    """
    Извлекает объект по ключу из JSON файла и сохраняет его в отдельный файл

    :param input_filename: Имя входного JSON файла
    :param name_key: Ключ, по которому нужно извлечь данные
    :param output_filename: Имя выходного файла (если None, будет использовано name_key + '.json')
    """
    # Загружаем исходный JSON
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Проверяем, существует ли указанный ключ
    if name_key not in data:
        raise KeyError(f"Ключ '{name_key}' не найден в JSON файле {input_filename}")

    # Получаем данные по ключу
    extracted_data = data[name_key]

    # Определяем имя выходного файла
    if output_filename is None:
        output_filename = f"{name_key}.json"

    # Сохраняем извлеченные данные в новый JSON файл
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Данные успешно сохранены в файл {output_filename}")

# Пример использования:
# extract_and_save_json('input.json', 'name_i')