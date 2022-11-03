import yaml
import faker
import faker.providers
import random

faker.Faker.seed(0)
random.seed(0)
fake = faker.Faker()

ystart_provider = faker.providers.DynamicProvider(
    provider_name="ystart",
    elements=[2015, 2014, 2013, 2012]
)
fake.add_provider(ystart_provider)

house_provider = faker.providers.DynamicProvider(
    provider_name="house",
    elements=["Red", "Yellow", "Blue", "Green"]
)
fake.add_provider(house_provider)

students = {}

students_to_generate = 20

for i in range(students_to_generate):
    if students_to_generate-i != 1:
        name = fake.name()
    name_with_dots = name.replace(" ", ".")
    username_discriminator = 0
    while name_with_dots+str(username_discriminator).rjust(2, "0") in students:
        username_discriminator += 1
        print(name_with_dots,"is duplicated")
    username = (name_with_dots+"."+str(username_discriminator).rjust(2, "0")).lower()
    students[username] = {
        "name": name,
        "ystart": fake.ystart(),
        "house": fake.house()
    }

print(yaml.dump(students))

# students_split_by_ystart = {}

# for username, student in students.items():
#     if student["year"] in students_split_by_ystart:

