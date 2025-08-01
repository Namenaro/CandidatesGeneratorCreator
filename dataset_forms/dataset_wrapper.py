from settings import PADDING, FREQUENCY
from dataset_forms.LUDB_utils import get_LUDB_data, get_signal_by_id_and_lead_mV

from typing import List, Optional, Dict, Any
import json
from tkinter import filedialog
from types import SimpleNamespace

POINTS_DATASET_JSON_KEYS = SimpleNamespace(
    id = "id", # имя записи в LUDB
    lead = "lead",
    points = "points"
)


class DatasetWrapper:
    def __init__(self, path_to_dataset):
        self.path = path_to_dataset

        self.entries_list = self.load_forms_dataset() # это составленный нами датасет (см. README)
        self.LUDB_data = get_LUDB_data() # из него будем брать сигнал ЭКГ


    def __len__(self):
        return len(self.entries_list)

    def get_ith_entry(self, i)->Dict:
        return self.entries_list[i]

    def del_ith_entry(self, i):
        del self.entries_list[i]
        # перезаписываем json с датасетом
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.entries_list, f, ensure_ascii=False, indent=4)
            print("Удалена запись")


    def get_signal_for_ith_entry(self, i):
        entry = self.entries_list[i]
        # получаем полный сигнал отведения
        lead = entry["lead"]
        id_in_LUDB = entry["id"]
        signal = get_signal_by_id_and_lead_mV(lead_name=lead, patient_id=id_in_LUDB, LUDB_data=self.LUDB_data)

        # вырезаем из него фрагмент
        points_coords = entry["points"].values()
        left_t = min(points_coords) - PADDING
        right_t = max(points_coords) + PADDING

        if left_t < 0:
            left_t = 0

        left_i = int(left_t* FREQUENCY)
        right_i = int(right_t * FREQUENCY)
        right_i = min(right_i, len(signal) - 1)

        signal_fragment = signal[left_i:right_i]
        time = [i/FREQUENCY for i in range(left_i, right_i)]
        return signal_fragment, time

    def get_info_about_patient(self, id_in_LUDB):
        pass

    def load_forms_dataset(self):
        try:
            with open(self.path, 'r') as f:
                data_list = json.load(f)
                return data_list
        except FileNotFoundError:
            return []


if __name__ == "__main__":
    file_path = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(("Все файлы", "*.*"), ("Текстовые файлы", "*.txt"))
    )

    if file_path:
        dataset = DatasetWrapper(file_path)

        index = 0

        entry = dataset.get_ith_entry(index)

        points_dict = entry[POINTS_DATASET_JSON_KEYS.points]
        print(f"точки {points_dict}")

        signal, time = dataset.get_signal_for_ith_entry(index)
        print(f" сигнал mV {signal}")
        print(f" время в секундах {time}")








