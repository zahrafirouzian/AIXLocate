from app.tools.fortyguard_environment import get_environmental_data
from app.services.climate_normalizer import normalize_climate_data



def climate_node(state):


    locations = state["locations"]


    climate_results = []



    for location in locations:


        print(
            "Requesting FortyGuard:",
            location["name"]
        )


        data = get_environmental_data(
            lat=location["lat"],
            lon=location["lon"],
            temperature=location.get("temperature", 25)
        )

        print(
            "FortyGuard completed:",
            location["name"]
        )



        result = data["result"]["locations"][0]



        normalized = normalize_climate_data(

            {

                "name": location["name"],

                "lat": location["lat"],

                "lon": location["lon"],

                "temperature": result["temperature"],

                "solar_ghi": result["solar_irradiance"]["clear_sky"]["ghi"],

                "solar_dni": result["solar_irradiance"]["clear_sky"]["dni"],

            }

        )


        climate_results.append(
            normalized
        )



    return {

        "locations": climate_results

    }