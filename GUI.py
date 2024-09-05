import tkinter as tk
from tkinter import ttk, messagebox

class GUI(tk.Tk):
    def __init__(self, db, funcs):
        super().__init__()
        self.title("IMDB 1000 Filmleri")
        self.geometry("600x400")
        self.db = db
        self.funcs = funcs
        self.create_widgets()

    def create_widgets(self):
        # Başlık
        self.label = tk.Label(self, text="IMDB 1000 Filmleri Arama", font=("Arial", 16))
        self.label.pack(pady=10)

        # Menü seçenekleri
        self.menu_var = tk.StringVar(value="Film Ara")
        self.menu_options = ["Film Ara", "Yönetmen Ara", "IMDB Puanı", "Türler", "Başrol Ara"]
        self.dropdown = ttk.Combobox(self, textvariable=self.menu_var, values=self.menu_options)
        self.dropdown.pack(pady=10)

        # Arama terimi girişi
        self.entry_label = tk.Label(self, text="Arama terimi giriniz:")
        self.entry_label.pack()
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.pack(pady=10)

        # Ara butonu
        self.search_button = tk.Button(self, text="Ara", command=self.search)
        self.search_button.pack(pady=10)

        # Sonuçlar için bir text kutusu
        self.results_text = tk.Text(self, height=15, width=80)
        self.results_text.pack(pady=10)

    def search(self):
        choice = self.menu_var.get()
        keyword = self.search_entry.get().strip()

        self.results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle

        if choice == "Film Ara":
            self.funcs.query(["Series_Title", keyword],
                             {"Filmin Adı": 'Series_Title', "IMDB Puanı": 'IMDB_Rating'})
        elif choice == "Yönetmen Ara":
            self.funcs.query(['Director', keyword],
                             {"Filmin Adı": 'Series_Title', "Yönetmen": 'Director', "IMDB Puanı": 'IMDB_Rating'})
        elif choice == "IMDB Puanı":
            try:
                limits = keyword.split(',')
                if len(limits) != 2:
                    raise ValueError("Puan aralığı eksik.")
                upper_limit, lower_limit = float(limits[0]), float(limits[1])
                self.funcs.list_imdb_rating([upper_limit, lower_limit])
            except ValueError as e:
                self.results_text.insert(tk.END, f"Geçersiz puan aralığı: {e}\n")
        elif choice == "Türler":
            self.funcs.query(['Genre', keyword],
                             {"Filmin Adı": 'Series_Title', "Tür": 'Genre', "IMDB Puanı": 'IMDB_Rating'})
        elif choice == "Başrol Ara":
            self.funcs.find_star(keyword)
        else:
            messagebox.showerror("Hata", "Geçersiz seçim!")

        # Sonuçları GUI'de göster
        for result in self.funcs.results:
            self.results_text.insert(tk.END, result + "\n")
