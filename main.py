from GUI import GUI
import database
import movieFunctions


if __name__ == "__main__":
    path = r"C:\Users\MR. CAPH\PycharmProjects\IMDB1000\imdb_top_1000.csv"

    # Veritabanı ve fonksiyon sınıflarını başlat
    db = database.Database(path)
    funcs = movieFunctions.MovieFunctions(db)

    # GUI başlat
    app = GUI(db, funcs)
    app.mainloop()
