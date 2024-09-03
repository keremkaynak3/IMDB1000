from sampleGui import UI
from database import Database
from movieFunctions import Functions

if __name__ == "__main__":
    path = r"C:\Users\MR. CAPH\PycharmProjects\IMDB1000\imdb_top_1000.csv"

    # Database sınıfı kullanılarak CSV dosyası okunur
    db = Database(path)

    # Fonksiyon sınıfı ile veritabanı işlevleri yönetilir
    funcs = Functions()

    # Menü seçenekleri
    menu_choices = ["Film Ara", "Yönetmen Ara", "IMDB Puan", "Türler", "Başrol Ara", "Çıkış"]

    # UI sınıfı kullanılarak menü arayüzü oluşturulur
    ui = UI(menu_choices)

    while True:
        ui.menu()
        try:
            secim = int(input("Lütfen seçiminizi giriniz: "))
            if secim == 1:
                funcs.query(["Series_Title", input("Lütfen film içerisinde geçen bir kelime giriniz: ").lower()],
                            {"Filmin Adı": 'Series_Title', "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 2:
                funcs.query(['Director', input("Lütfen yönetmen içerisinde geçen bir kelime giriniz: ").lower()],
                            {"Filmin Adı": 'Series_Title', "Yönetmen": "Director", "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 3:
                funcs.list_imdb_rating([input("Büyük sayıyı giriniz: "), input("Küçük sayıyı giriniz: ")])
            elif secim == 4:
                funcs.query(['Genre', input("Lütfen tür içerisinde geçen bir kelime giriniz: ").lower()],
                            {"Filmin Adı": 'Series_Title', "Yönetmen": "Director", "Tür": "Genre",
                             "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 5:
                funcs.find_star(input("Lütfen başrol isminin içerisinde geçen bir kelime giriniz: ").lower())
            elif secim == 6:
                print("Programdan çıkılıyor.")
                break
            else:
                print("Yanlış seçim. Lütfen tekrar deneyin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

