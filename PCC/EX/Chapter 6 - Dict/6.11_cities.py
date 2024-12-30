cities = {
    "Tallinn":{
        "Country": "Estonia",
        "Population": 1_300_000,
        "Size": "Small"
    },

    "Helsinki":{
        "Country": "Finland",
        "Population": 2_700_000,
        "Size": "Medium"
    }
}
for city, country in cities.items():
    print(f"City: {city} is capital of {country['Country']}, it's population is {country['Population']} and its size is {country['Size']}")