class MovieFunctions:
    def __init__(self, db):
        self.db = db
        self.results = []

    def query(self, search_keyword, printing_keywords):
        self.results.clear()
        for key, film in self.db.items():
            if search_keyword[1].lower() in film[search_keyword[0]].lower():
                result = "-" * 10 + "\n"
                for pkey, printing_keyword in printing_keywords.items():
                    result += f"{pkey} ----> {film[printing_keyword]}\n"
                result += "-" * 10 + "\n"
                self.results.append(result)

        if not self.results:
            self.results.append(f"No results found for '{search_keyword[1]}'.")

    def list_imdb_rating(self, keyword):
        self.results.clear()
        try:
            upper_limit, lower_limit = keyword[0], keyword[1]
            for key, film in self.db.items():
                if upper_limit >= float(film['IMDB_Rating']) >= lower_limit:
                    self.results.append(f"MOVIE NAME: '{film['Series_Title']}' IMDB Rating --> {film['IMDB_Rating']}")

            if upper_limit < lower_limit:
                self.results.append("Maximum rating can not smaller than minimum rating!")

            if not self.results:
                self.results.append(f"No movies found with IMDB rating between {lower_limit} and {upper_limit}.")
        except ValueError:
            self.results.append("INVALID RATING RANGE! Please provide valid numeric values.")

    def find_star(self, keyword):
        self.results.clear()
        for key, film in self.db.items():
            stars = [film['Star1'], film['Star2'], film['Star3'], film['Star4']]
            if any(star.lower().find(keyword.lower()) != -1 for star in stars):
                self.results.append(
                    f"*  {', '.join(stars)} MOVIE: '{film['Series_Title']}' IMDB Rating --> {film['IMDB_Rating']}")

        if not self.results:
            self.results.append(f"No results found for '{keyword}'.")
