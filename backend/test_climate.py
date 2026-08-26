from app.agents.climate import climate_node


state = {

    "locations":[

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

}


result = climate_node(state)


print(result)
