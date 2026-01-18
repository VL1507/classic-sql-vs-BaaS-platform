from faker import Faker

from db_conn import Session

fake = Faker(locale="ru_RU")

print(fake.time(pattern="%H:%M"))

user_types = ["Владелец"]
