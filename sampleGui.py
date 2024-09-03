class UI ():
    def __init__(self, choices):
        self.choices = choices

    def menu(self):
        print('''
             |--------------------------------|
             |******       Menü        *******|  
             |--------------------------------|''')
        i = 1
        for i in range(0,len(self.choices)):
            print(f'''             | {i+1}...{self.choices[i]} |  ''')
            i+=1
        print("             ----------------------------------")






