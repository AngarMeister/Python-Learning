human1 = {
    "first_name": "Lebo",
    "last_name": "Tripo",
    "age": 21,
    "city": "Muuga"
}
human2 = {
    "first_name": "Nerko",
    "last_name": "Orks",
    "age": 25,
    "city": "Tallinn"
}
human3 = {
    "first_name": "Svilo",
    "last_name": "Zoks",
    "age": 65,
    "city": "Tartu"
}

people = [human1, human2, human3]
for person in people:
    print(f"Person named {person['first_name']} {person['last_name']} who is {person['age']} years old, also lives in {person['city']}")
