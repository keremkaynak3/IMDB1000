import csv

class Database:
    def __init__(self, path):
        self.data = self.read_csv(path)

    def read_csv(self, path):
        """
        CSV dosyasını okur ve veritabanı olarak kullanılacak bir sözlük oluşturur.
        :param path: CSV dosyasının yolu
        :return: Filmler veritabanı
        """
        with open(path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            database = {i: row for i, row in enumerate(reader)}
        return database

    def items(self):
        return self.data.items()
