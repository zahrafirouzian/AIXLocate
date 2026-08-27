from app.services.city_boundary import get_city_boundary
from app.services.heatmap_aoi import create_heatmap_aoi


city = "Phoenix, Arizona, USA"

boundary = get_city_boundary(city)

aoi = create_heatmap_aoi(
    boundary,
    size_km=5
)

geometry = aoi["features"][0]["geometry"]

print("City:", city)
print("AOI geometry:", geometry["type"])
print("Coordinates:", len(geometry["coordinates"][0]))
