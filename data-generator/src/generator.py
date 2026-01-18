from faker import Faker

fake = Faker(locale="ru_RU")

print(fake.time(pattern="%H:%M"))

user_types = ["Владелец"]
