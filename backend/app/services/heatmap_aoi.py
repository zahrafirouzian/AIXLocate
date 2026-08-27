from shapely.geometry import shape, mapping, Point
from shapely.ops import transform
from pyproj import Transformer


def create_heatmap_aoi(
    boundary,
    size_km=1.5
):
    """
    Create a Polygon AOI around the center of a city.

    size_km:
        Radius of the AOI around the city center.
    """

    feature = boundary["features"][0]

    geom = shape(
        feature["geometry"]
    )

    if geom.is_empty:
        raise ValueError(
            "City boundary geometry is empty"
        )

    # Find city center
    center = geom.centroid

    # WGS84 -> Web Mercator
    to_meters_transformer = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True
    )

    # Web Mercator -> WGS84
    to_wgs84_transformer = Transformer.from_crs(
        "EPSG:3857",
        "EPSG:4326",
        always_xy=True
    )

    # Transform city center to meters
    center_m = transform(
        to_meters_transformer.transform,
        center
    )

    # Create circular AOI
    radius_meters = size_km * 1000

    aoi = Point(
        center_m.x,
        center_m.y
    ).buffer(
        radius_meters
    )

    # Simplify geometry slightly
    aoi = aoi.simplify(
        50
    )

    # Make sure result is Polygon
    if aoi.geom_type != "Polygon":
        aoi = aoi.convex_hull

    # Convert back to WGS84
    aoi_wgs84 = transform(
        to_wgs84_transformer.transform,
        aoi
    )

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": mapping(
                    aoi_wgs84
                )
            }
        ]
    }