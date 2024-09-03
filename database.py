import csv
class Database:
    def __init__(self, path):
        self.path = path
        self.dataDict = self.read_csv()

    def read_csv(self):
        from csv import DictReader
        dataDict = {}
        with open(self.path, mode='r', encoding='utf-8-sig') as file:
            csvReader = DictReader(file)
            lineCount = 0
            for row in csvReader:
                key = f"film_{lineCount}"  # Her satır için bir anahtar oluştur
                dataDict[key] = row
                lineCount += 1
        return dataDict