from faker import Faker
from faker.providers import BaseProvider
import random
import csv
from datetime import datetime


class GenereProvider(BaseProvider):
    def movie_genre(self):
        return random.choice(
            [
                "Documentary",
                "Thriller",
                "Mystery",
                "Horror",
                "Action",
                "Comedy",
                "Drama",
                "Romance",
            ]
        )


class LanguageProvider(BaseProvider):
    def language(self):
        return random.choice(
            ["English", "Chinese", "Italian", "Spanish", "Hindi", "Japanese"]
        )


fake = Faker()

fake.add_provider(GenereProvider)
fake.add_provider(LanguageProvider)

# Some of this is a bit verbose now, but doing so for the sake of completion


def get_movie_name():
    words = fake.words()
    capitalized_words = list(map(lambda x: x.upper(), words))
    return " ".join(capitalized_words)


def get_movie_date():
    return datetime.strftime(fake.date_time_this_decade(), "%B %d, %Y")


def get_movie_len():
    return random.randrange(50, 150)


def get_movie_rating():
    return round(random.uniform(1.0, 5.0), 1)


def generate_movie():
    return [
        get_movie_name(),
        fake.movie_genre(),
        get_movie_date(),
        get_movie_len(),
        get_movie_rating(),
        fake.language(),
    ]


with open("movie_data.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Genre", "Premiere", "Runtime", "IMDB Score", "Language"])
    for n in range(1, 100):
        writer.writerow(generate_movie())
