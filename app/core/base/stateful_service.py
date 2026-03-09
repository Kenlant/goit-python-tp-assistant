import pickle


class StatefullService:
    def save_data(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_data(filename, cls):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            return cls()
