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

students_to_generate = 1000

for i in range(students_to_generate):
    profile = fake.profile()

    name = profile["name"]

    # preferred_name username with only letters
    preferred_name = "".join(
        [c for c in profile["username"] if c.isalpha()]
    )

    name_with_dots = name.replace(" ", ".")

    username_discriminator = 0
    while name_with_dots+str(username_discriminator).rjust(2, "0") in students:
        username_discriminator += 1
        print(name_with_dots, "is duplicated")

    username = (name_with_dots+"." +
                str(username_discriminator).rjust(2, "0")).lower()

    if profile["sex"] == "M":
        gender = "male"
    else:
        gender = "female"

    students[username] = {
        "house": fake.house(),
        "name": name,
        "preferred_name": preferred_name,
        "ystart": fake.ystart(),
        "gender": gender
    }

# benjamin.jefferson.00:
    # house: Green
    # name: Benjamin Jefferson
    # preferred_name: Ben
    # ystart: 2013
    # gender: male

students_db_text = yaml.dump(
    {
        "students": students,
        "houses": [
            "Red",
            "Yellow",
            "Blue",
            "Green"
        ]
    }
)

with open("student_db.yaml", "w") as f:
    f.write(students_db_text)


# students_split_by_ystart = {}

# for username, student in students.items():
#     if student["year"] in students_split_by_ystart:
