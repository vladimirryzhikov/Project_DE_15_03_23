from faker import Faker
from datetime import datetime
from faker.providers import BaseProvider

fake = Faker()


def capitalize(str):
    return str.capitalize()


words = fake.words()
capitalized_words = list(map(capitalize, words))
stock_name = " ".join(capitalized_words)
print(stock_name)

date = datetime.strftime(fake.date_time_this_decade(), "%B %d, %Y")
print(date)


class StockNameProvider(BaseProvider):
    def stock_name(self):
        return random.choice(["UAA", "COIN", "MSFT", "ZIM", "TLT", "RIG"])

    # add new provider to faker instance
    fake.add_provider(StockNameProvider)

    stock = fake.stock_name()
    print(stock)
