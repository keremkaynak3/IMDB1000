import tkinter as tk
from tkinter import ttk, messagebox


class GUI(tk.Tk):
    def __init__(self, db, funcs):
        super().__init__()
        self.title("IMDB 1000 Filmleri")
        self.geometry("700x500")
        self.db = db
        self.funcs = funcs
        self.configure(bg="#e0e0e0")
        self.create_widgets()

    def create_widgets(self):
        # Başlık
        self.label = tk.Label(self, text="IMDB 1000 Filmleri Arama", font=("Arial", 18, "bold"), bg="#e0e0e0",
                              fg="#333")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Menü seçenekleri
        self.menu_var = tk.StringVar(value="Film Ara")
        self.menu_options = ["Film Ara", "Yönetmen Ara", "IMDB Puanı", "Türler", "Başrol Ara"]
        self.dropdown = ttk.Combobox(self, textvariable=self.menu_var, values=self.menu_options, state="readonly")
        self.dropdown.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.dropdown.bind("<<ComboboxSelected>>", self.toggle_imdb_search_fields)

        # Arama terimi girişi
        self.entry_label = tk.Label(self, text="Arama terimi giriniz:", bg="#e0e0e0", font=("Arial", 12))
        self.entry_label.grid(row=2, column=0, padx=10, sticky="w")

        # Placeholder ekleyelim
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.search_entry.insert(0, "Arama terimi yazın...")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)

        # IMDB Puanı arama alanları (başlangıçta gizli)
        self.imdb_frame = tk.Frame(self, bg="#e0e0e0")
        self.imdb_frame.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="ew")
        self.imdb_frame.grid_remove()

        self.upper_label = tk.Label(self.imdb_frame, text="Üst Puan Limiti:", bg="#e0e0e0", font=("Arial", 12))
        self.upper_label.grid(row=0, column=0, padx=5)
        self.upper_limit_entry = tk.Entry(self.imdb_frame, width=10)
        self.upper_limit_entry.grid(row=0, column=1, padx=5)

        self.lower_label = tk.Label(self.imdb_frame, text="Alt Puan Limiti:", bg="#e0e0e0", font=("Arial", 12))
        self.lower_label.grid(row=0, column=2, padx=5)
        self.lower_limit_entry = tk.Entry(self.imdb_frame, width=10)
        self.lower_limit_entry.grid(row=0, column=3, padx=5)

        # Ara butonu
        self.search_button = tk.Button(self, text="Ara", command=self.search, bg="#4CAF50", fg="white",
                                       font=("Arial", 12, "bold"), relief="raised")
        self.search_button.grid(row=5, column=1, padx=10, pady=5)
        self.search_button.bind("<Enter>", self.on_hover)
        self.search_button.bind("<Leave>", self.on_leave)

        # Sonuçlar başlığı
        self.result_label = tk.Label(self, text="Sonuçlar:", font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#555")
        self.result_label.grid(row=6, column=0, padx=10, pady=(20, 0), sticky="w")

        # Sonuçlar için bir text kutusu ve kaydırma çubuğu
        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.results_text = tk.Text(self.results_frame, wrap="word", bg="#ffffff", relief="solid", borderwidth=1)
        self.results_text.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Grid ayarları
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
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
        self.search_button.config(bg="#45a049")

    def on_leave(self, event):
        self.search_button.config(bg="#4CAF50")

    def toggle_imdb_search_fields(self, event):
        # IMDB Puanı araması seçildiğinde giriş alanlarını göster, diğer durumlarda gizle
        if self.menu_var.get() == "IMDB Puanı":
            self.imdb_frame.grid()
            self.entry_label.grid_remove()
            self.search_entry.grid_remove()
        else:
            self.imdb_frame.grid_remove()
            self.entry_label.grid()
            self.search_entry.grid()

    def search(self):
        choice = self.menu_var.get()

        if choice == "IMDB Puanı":
            # IMDB Puanı seçildiğinde iki ayrı girişi alalım
            try:
                lower_limit = float(self.lower_limit_entry.get())
                upper_limit = float(self.upper_limit_entry.get())
                self.funcs.list_imdb_rating([upper_limit, lower_limit])
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli puan limitleri girin!")
                return
        elif choice == "Türler":
            keyword = self.search_entry.get().strip()
            if keyword == "Arama terimi yazın..." or keyword == "":
                messagebox.showerror("Hata", "Lütfen bir tür girin!")
                return
            self.funcs.query(['Genre', keyword],
                             {"Filmin Adı": 'Series_Title', "Tür": 'Genre'})
        else:
            keyword = self.search_entry.get().strip()
            if keyword == "Arama terimi yazın..." or keyword == "":
                messagebox.showerror("Hata", "Lütfen bir arama terimi girin!")
                return

            self.results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle
            if choice == "Film Ara":
                self.funcs.query(["Series_Title", keyword],
                                 {"Filmin Adı": 'Series_Title'})
            elif choice == "Yönetmen Ara":
                self.funcs.query(['Director', keyword],
                                 {"Filmin Adı": 'Series_Title', "Yönetmen": 'Director'})
            elif choice == "Başrol Ara":
                self.funcs.find_star(keyword)
            else:
                self.results_text.insert(tk.END, "Bilinmeyen bir seçenek seçildi.")

        # Sonuçları göster
        self.results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle
        for result in self.funcs.results:
            self.results_text.insert(tk.END, result + "\n\n")
