class MovieFunctions:
    def __init__(self, db):
        self.db = db
        self.results = []


    def query(self, search_keyword, printing_keywords):
        self.results.clear()
        for key, film in self.db.items():
            # film[search_keyword[0]] verisini alıp, search_keyword[1] içinde arama yapıyoruz
            # lower().find() yerine 'in' ile kontrolü daha basit yapalım
            if search_keyword[1].lower() in film[search_keyword[0]].lower():
                result = "-" * 10 + "\n"
                for pkey, printing_keyword in printing_keywords.items():
                    result += f"{pkey} ----> {film[printing_keyword]}\n"
                result += "-" * 10 + "\n"
                self.results.append(result)

    def list_imdb_rating(self, keyword):
        self.results.clear()
        try:
            upper_limit, lower_limit = keyword[0], keyword[1]
            for key, film in self.db.items():
                if upper_limit >= float(film['IMDB_Rating']) >= lower_limit:
                    self.results.append(f"Film'in adı '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")
        except ValueError:
            self.results.append("Geçersiz puan aralığı.")

    def find_star(self, keyword):
        self.results.clear()
        for key, film in self.db.items():
            stars = [film['Star1'], film['Star2'], film['Star3'], film['Star4']]
            if any(star.lower().find(keyword.lower()) != -1 for star in stars):
                self.results.append(f"*  {', '.join(stars)} film'i '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")
