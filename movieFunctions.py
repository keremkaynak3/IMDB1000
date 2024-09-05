class MovieFunctions:
    def __init__(self, db):
        self.db = db  # Veritabanı referansını sınıfa alıyoruz

    def query(self, search_keyword, printing_keywords):
        """
        Filmleri belirli bir anahtar kelimeye göre arar ve sonuçları ekrana yazdırır.
        :param search_keyword: Arama yapılacak kolon ve kelime [kolon_adı, kelime]
        :param printing_keywords: Yazdırılacak kolonlar {görünen_ad: kolon_adı}
        """
        for key, film in self.db.items():
            if film[search_keyword[0]].lower().find(search_keyword[1]) != -1:
                print("-" * 10)
                for pkey, printing_keyword in printing_keywords.items():
                    print(f"{pkey} ----> {film[printing_keyword]}")
                print("-" * 10, "\n")

    def list_imdb_rating(self, keyword):
        """
        Belirli IMDB puanı aralığındaki filmleri listeler.
        :param keyword: [upper_limit, lower_limit] IMDB puan aralığı
        """
        upper_limit, lower_limit = float(keyword[0]), float(keyword[1])
        for key, film in self.db.items():
            if upper_limit >= float(film['IMDB_Rating']) >= lower_limit:
                print(f"Film'in adı '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")

    def find_star(self, keyword):
        """
        Belirli bir başrol oyuncusu adına göre filmleri bulur.
        :param keyword: Oyuncu adında arama yapılacak kelime
        """
        for key, film in self.db.items():
            stars = [film['Star1'], film['Star2'], film['Star3'], film['Star4']]
            if any(star.lower().find(keyword) != -1 for star in stars):
                print(f"*  {', '.join(stars)} film'i '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")
