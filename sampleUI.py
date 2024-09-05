class UI():
    def __init__(self, choices):
        self.choices = choices

    def menu(self):
        print('''
             |--------------------------------|
             |******       Menü        *******|  
             |--------------------------------|''')

        # Maksimum seçenek uzunluğunu bulalım, böylece tüm satırları aynı hizaya getirebiliriz
        max_length = max(len(choice) for choice in self.choices)

        for i in range(len(self.choices)):
            # Her satırı aynı uzunluğa getirmek için boşluk ekleyelim
            print(f'''             |        {i + 1}...{self.choices[i].ljust(max_length)}        |  ''')

        print("             ----------------------------------")

