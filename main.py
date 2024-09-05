import sampleUI
import database
import movieFunctions

if __name__ == "__main__":
    path = r"C:\Users\MR. CAPH\PycharmProjects\IMDB1000\imdb_top_1000.csv"

    # Veritabanı sınıfı kullanılarak CSV dosyası okunur
    db = database.Database(path)  # Sınıf adları büyük harfle başlatılır

    # Fonksiyon sınıfı ile veritabanı işlevleri yönetilir
    funcs = movieFunctions.MovieFunctions(db)  # MovieFunctions sınıfı oluşturuldu ve database'i aldı

    # Menü seçenekleri
    menu_choices = ["Film Ara", "Yönetmen Ara", "IMDB Puanı", "Türler", "Başrol Ara", "Çıkış"]

    # UI sınıfı kullanılarak menü arayüzü oluşturulur
    ui = sampleUI.UI(menu_choices)

    while True:
        ui.menu()  # Menü görüntülenir
        try:
            secim = int(input("Lütfen seçiminizi giriniz: "))
            if secim == 1:
                # Film Ara
                search_term = input("Lütfen film içerisinde geçen bir kelime giriniz: ").lower()
                funcs.query(["Series_Title", search_term],
                            {"Filmin Adı": 'Series_Title', "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 2:
                # Yönetmen Ara
                search_term = input("Lütfen yönetmen içerisinde geçen bir kelime giriniz: ").lower()
                funcs.query(['Director', search_term],
                            {"Filmin Adı": 'Series_Title', "Yönetmen": "Director", "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 3:
                # IMDB Puanı Ara
                upper_limit = input("Büyük sayıyı giriniz: ")
                lower_limit = input("Küçük sayıyı giriniz: ")
                funcs.list_imdb_rating([upper_limit, lower_limit])
            elif secim == 4:
                # Türler Ara
                genre = input("Lütfen tür içerisinde geçen bir kelime giriniz: ").lower()
                funcs.query(['Genre', genre],
                            {"Filmin Adı": 'Series_Title', "Yönetmen": "Director", "Tür": "Genre",
                             "IMDB Puanı": 'IMDB_Rating'})
            elif secim == 5:
                # Başrol Ara
                star_name = input("Lütfen başrol isminin içerisinde geçen bir kelime giriniz: ").lower()
                funcs.find_star(star_name)
            elif secim == 6:
                print("Programdan çıkılıyor.")
                break
            else:
                print("Yanlış seçim. Lütfen tekrar deneyin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
