import tkinter as tk
from tkinter import ttk, messagebox

class GUI(tk.Tk):
    def __init__(self, db, funcs):
        super().__init__()
        self.title("IMDB 1000 Filmleri")
        self.geometry("700x500")
        self.db = db
        self.funcs = funcs
        self.configure(bg="#e0e0e0")  # Arka plan rengini daha açık gri yapalım
        self.create_widgets()

    def create_widgets(self):
        # Başlık
        self.label = tk.Label(self, text="IMDB 1000 Filmleri Arama", font=("Arial", 18, "bold"), bg="#e0e0e0", fg="#333")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Menü seçenekleri
        self.menu_var = tk.StringVar(value="Film Ara")
        self.menu_options = ["Film Ara", "Yönetmen Ara", "IMDB Puanı", "Türler", "Başrol Ara"]
        self.dropdown = ttk.Combobox(self, textvariable=self.menu_var, values=self.menu_options, state="readonly")
        self.dropdown.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        # Arama terimi girişi
        self.entry_label = tk.Label(self, text="Arama terimi giriniz:", bg="#e0e0e0", font=("Arial", 12))
        self.entry_label.grid(row=2, column=0, padx=10, sticky="w")

        # Placeholder ekleyelim
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.search_entry.insert(0, "Arama terimi yazın...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)  # Placeholder kaldır
        self.search_entry.bind("<FocusOut>", self.add_placeholder)   # Placeholder geri getir

        # Ara butonu
        self.search_button = tk.Button(self, text="Ara", command=self.search, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="raised")
        self.search_button.grid(row=3, column=1, padx=10, pady=5)
        self.search_button.bind("<Enter>", self.on_hover)
        self.search_button.bind("<Leave>", self.on_leave)

        # Sonuçlar başlığı
        self.result_label = tk.Label(self, text="Sonuçlar:", font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#555")
        self.result_label.grid(row=4, column=0, padx=10, pady=(20, 0), sticky="w")

        # Sonuçlar için bir text kutusu ve kaydırma çubuğu
        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.results_text = tk.Text(self.results_frame, height=15, width=80, wrap="word", bg="#ffffff", relief="solid", borderwidth=1)
        self.results_text.grid(row=0, column=0, sticky="nsew")

        # Kaydırma çubuğu
        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Arama çerçevesinin genişleyebilmesi için
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def clear_placeholder(self, event):
        if self.search_entry.get() == "Arama terimi yazın...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Arama terimi yazın...")
            self.search_entry.config(fg="gray")

    def on_hover(self, event):
        self.search_button.config(bg="#45a049")  # Hover'da renk değişikliği

    def on_leave(self, event):
        self.search_button.config(bg="#4CAF50")  # Normal renge dön

    def search(self):
        choice = self.menu_var.get()
        keyword = self.search_entry.get().strip()

        if keyword == "Arama terimi yazın...":
            messagebox.showerror("Hata", "Lütfen bir arama terimi girin!")
            return

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
