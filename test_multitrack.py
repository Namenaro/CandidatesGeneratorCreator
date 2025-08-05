class TestMultitrack:
    def __init__(self, multitrack, dataset, left_name:str, right_name:str, target_name:str):
        self.errs_list = []
        self.num_candidates = []
        self.multitrack = multitrack
        self.dataset = dataset


    def run(self):
        # вернуть среднюю ошибку лучшего кандидата, среднее количество кандидатов
        return 1, 2