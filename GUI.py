import tkinter as tk
from tkinter import ttk, messagebox


class GUI(tk.Tk):
    def __init__(self, db, funcs):
        super().__init__()
        self.title("Movie Finder")
        self.geometry("1000x700")
        self.db = db
        self.funcs = funcs
        self.configure(bg="#e0e0e0")
        self.create_widgets()

    def create_widgets(self):
        # Başlık
        self.label = tk.Label(self, text="SEARCH MOVIES AS YOU WISH", font=("Arial", 18, "bold"), bg="#e0e0e0",
                              fg="#333")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Menü seçenekleri
        self.menu_var = tk.StringVar(value="...")
        self.menu_options = ["By Movie Name", "By Director", "By IMDB Rating", "By Type", "By Actor"]
        self.dropdown = ttk.Combobox(self, textvariable=self.menu_var, values=self.menu_options, state="readonly")
        self.dropdown.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.dropdown.bind("<<ComboboxSelected>>", self.toggle_imdb_search_fields)

        # Arama terimi girişi
        self.entry_label = tk.Label(self, text="Enter a value:", bg="#e0e0e0", font=("Arial", 12))
        self.entry_label.grid(row=2, column=0, padx=10, sticky="w")

        # Placeholder ekleyelim
        self.search_entry = tk.Entry(self, width=50)
        self.search_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.search_entry.insert(0, "")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_placeholder)

        # IMDB Puanı arama alanları (başlangıçta gizli)
        self.imdb_frame = tk.Frame(self, bg="#e0e0e0")
        self.imdb_frame.grid(row=4, column=0, columnspan=2, pady=5, padx=10, sticky="ew")
        self.imdb_frame.grid_remove()

        self.upper_label = tk.Label(self.imdb_frame, text="Maximum Rating:", bg="#e0e0e0", font=("Arial", 12))
        self.upper_label.grid(row=0, column=0, padx=5)
        self.upper_limit_entry = tk.Entry(self.imdb_frame, width=10)
        self.upper_limit_entry.grid(row=0, column=1, padx=5)

        self.lower_label = tk.Label(self.imdb_frame, text="Minimum Rating:", bg="#e0e0e0", font=("Arial", 12))
        self.lower_label.grid(row=0, column=2, padx=5)
        self.lower_limit_entry = tk.Entry(self.imdb_frame, width=10)
        self.lower_limit_entry.grid(row=0, column=3, padx=5)

        # Ara butonu
        self.search_button = tk.Button(self, text="Search", command=self.search, bg="#4CAF50", fg="white",
                                       font=("Arial", 12, "bold"), relief="raised")
        self.search_button.grid(row=5, column=1, padx=10, pady=5)
        self.search_button.bind("<Enter>", self.on_hover)
        self.search_button.bind("<Leave>", self.on_leave)

        # Sonuçlar başlığı
        self.result_label = tk.Label(self, text="Results:", font=("Arial", 14, "bold"), bg="#e0e0e0", fg="#555")
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
        if self.search_entry.get() == "Type a search term...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="black")

    def add_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Type a search term...")
            self.search_entry.config(fg="gray")

    def on_hover(self, event):
        self.search_button.config(bg="#45a049")

    def on_leave(self, event):
        self.search_button.config(bg="#4CAF50")

    def toggle_imdb_search_fields(self, event):
        # IMDB Puanı araması seçildiğinde giriş alanlarını göster, diğer durumlarda gizle
        if self.menu_var.get() == "By IMDB Rating":
            self.results_text.delete(1.0, tk.END)
            self.imdb_frame.grid()
            self.entry_label.grid_remove()
            self.search_entry.grid_remove()
        else:
            self.imdb_frame.grid_remove()
            self.entry_label.grid()
            self.search_entry.grid()

    def search(self):
        choice = self.menu_var.get()

        if choice == "By IMDB Rating":
            # IMDB Puanı seçildiğinde iki ayrı girişi alalım
            try:
                lower_limit = float(self.lower_limit_entry.get())
                upper_limit = float(self.upper_limit_entry.get())
                self.funcs.list_imdb_rating([upper_limit, lower_limit])
            except ValueError:
                messagebox.showerror("ERROR!", "Please enter a valid numbers!")
                return
        elif choice == "By Type":
            keyword = self.search_entry.get().strip()
            if keyword == "Type a search term..." or keyword == "":
                messagebox.showerror("ERROR!", "Please enter a type!")
                return
            self.funcs.query(['Genre', keyword],
                             {"MOVIE NAME": 'Series_Title', "TYPE": 'Genre'})
        else:
            keyword = self.search_entry.get().strip()
            if keyword == "Type a search term..." or keyword == "":
                messagebox.showerror("ERROR!", "Please enter a search term!")
                return

            self.results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle
            if choice == "By Movie Name":
                self.funcs.query(["Series_Title", keyword],
                                 {"Filmin Adı": 'Series_Title'})
            elif choice == "By Director":
                self.funcs.query(['Director', keyword],
                                 {"MOVIE NAME": 'Series_Title', "DIRECTOR": 'Director'})
            elif choice == "By Actor":
                self.funcs.find_star(keyword)
            else:
                self.results_text.insert(tk.END, "INVALID OPTION!")

        # Sonuçları göster
        self.results_text.delete(1.0, tk.END)  # Önceki sonuçları temizle
        for result in self.funcs.results:
            self.results_text.insert(tk.END, result + "\n\n")
