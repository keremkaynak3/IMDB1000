class Functions():
    def Query(searchKeyword, printingKeywords):
        for key,film in database.items():
            if film[searchKeyword[0]].lower().find(searchKeyword[1])!=-1:
                print("-"*10)
                for pkey,printingKeyword in printingKeywords.items():print(f"{pkey}---->{film[printingKeyword]}")
                print("-"*10,"\n")

    def ListIMDBRating(keyword):
        for key,film in database.items():
            if float(keyword[0])>=float(film['IMDB_Rating'])>=float(keyword[1]):print(f"Film'in adı '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")

    def FindStar(keyword):
        for key,film in database.items():
            if film['Star1'].lower().find(keyword)!=-1 or film['Star2'].lower().find(keyword)!=-1 or film['Star3'].lower().find(keyword)!=-1 or film['Star4'].lower().find(keyword)!=-1:
                print(f"*  {film['Star1']},{film['Star2']},{film['Star3']},{film['Star4']} film'i '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")

        
"""    
def SearchFilm(keyword):
    for key,film in database.items():
        if film["Series_Title"].lower().find(keyword)!=-1:
            print(f"Film'in adı '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")


def FindDirector(keyword):
    for key,film in database.items():
        if film['Director'].lower().find(keyword)!=-1:
            print(f"Yönetmen '{film['Director']}' film'i '{film['Series_Title']}' IMDB puanı ----> {film['IMDB_Rating']}")
"""
