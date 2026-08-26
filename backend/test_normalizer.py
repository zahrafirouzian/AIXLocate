from app.services.climate_normalizer import normalize_climate_data


data = {
    "name":"North Phoenix",
    "temperature":38,
    "solar_ghi":904.13,
    "solar_dni":868.32
}


print(
    normalize_climate_data(data)
)
