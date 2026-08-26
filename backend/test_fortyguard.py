from app.tools.fortyguard_environment import get_environmental_data



locations = [

    {
        "name":"North Phoenix",
        "lat":33.7,
        "lon":-112.1,
        "temperature":38
    },


    {
        "name":"Downtown Phoenix",
        "lat":33.44,
        "lon":-112.07,
        "temperature":44
    }

]



for loc in locations:


    print(
        "\nTesting:",
        loc["name"]
    )


    data = get_environmental_data(

        loc["lat"],

        loc["lon"],

        loc["temperature"]

    )


    print(
        "DONE:",
        loc["name"]
    )