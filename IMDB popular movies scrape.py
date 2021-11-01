import requests
from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime

response = requests.get("https://www.imdb.com/chart/moviemeter")
soup = BeautifulSoup(response.text, "html.parser")
movies = soup.select("tbody.lister-list tr")

with open("imdb.csv", "w", newline="") as csv_file:
    csv_writer = writer(csv_file)
    csv_writer.writerow(["rank", "title", "director", "rating", "release_date", "url", str(datetime.now())])

    rank = 1
    for movie in movies:
        title_column = movie.select("td.titleColumn")[0]
        rating_column = movie.select("td.imdbRating")[0]

        title = title_column.find("a").get_text()
        rating = rating_column.find("strong").get_text() if rating_column.find("strong") else "No rating"
        release_date = title_column.find(class_="secondaryInfo").get_text()
        trimmed_date = ''.join([char for char in release_date if char.isalnum()])
        url = f'https://imdb.com/{title_column.find("a")["href"]}'

        people = title_column.find("a")["title"]
        director = ""
        for char in people:
            if char != "(":
                director += char
            else:
                break

        csv_writer.writerow([rank, title, director.strip(), rating, trimmed_date, url])
        rank += 1
