Moissei = {
    "Pet's Name": "Moissei",
    "Owner": "Borja Nikolaevich",
    "Age" : 5,
    "Sex" : "male",
    "Weight" : 5
}
Sverspm = {
    "Pet's Name": "Sverspm",
    "Owner": "Borja Nikolaevich",
    "Age" : 5,
    "Sex": "female",
    "Weight" : 215
}
Merki = {
    "Pet's Name": "Merki",
    "Owner": "Borja Nikolaevich",
    "Age" : 5,
    "Sex" : "male",
    "Weight" : 25
}

pets = [Moissei, Sverspm, Merki]
for pet in pets:
    print(f"Pet called {pet["Pet's Name"]}, it's owner is {pet['Owner']}, and age is {pet['Age']}, it's sex is {pet["Sex"]} and it's weight is {pet["Weight"]}")