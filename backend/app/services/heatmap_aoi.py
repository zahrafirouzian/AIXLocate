from math import pi, sqrt

from shapely.geometry import shape, mapping
from shapely.ops import transform, unary_union
from pyproj import Transformer


# ==================================================
# FortyGuard Basic API limit
# ==================================================

# FortyGuard Basic:
# Maximum = 10 mi² ≈ 25.9 km²
#
# We intentionally stay below the official limit
# to leave a safety margin.
#
# 20 km² ≈ 7.72 mi²

MAX_AOI_AREA_KM2 = 20.0


def create_heatmap_aoi(
    boundary,
    padding_km=0.5,
):
    """
    Create a FortyGuard-compatible GeoJSON Polygon.

    The returned value is the geometry itself:

        {
            "type": "Polygon",
            "coordinates": [...]
        }

    NOT a FeatureCollection.

    FortyGuard Basic supports heatmaps up to
    approximately 10 mi² (~25.9 km²).

    This implementation intentionally keeps the AOI
    below 20 km² (~7.72 mi²).
    """

    # ==================================================
    # Validate boundary
    # ==================================================

    if not boundary:

        raise ValueError(
            "City boundary is empty"
        )

    features = boundary.get(
        "features",
        []
    )

    if not features:

        raise ValueError(
            "City boundary contains no features"
        )

    # ==================================================
    # Build geometry from all features
    # ==================================================

    geometries = []

    for feature in features:

        geometry = feature.get(
            "geometry"
        )

        if not geometry:
            continue

        try:

            geom = shape(
                geometry
            )

        except Exception as exc:

            print(
                "WARNING: Invalid boundary geometry:",
                exc
            )

            continue

        if not geom.is_empty:

            geometries.append(
                geom
            )

    if not geometries:

        raise ValueError(
            "No valid city boundary geometry found"
        )

    # ==================================================
    # Merge boundary geometries
    # ==================================================

    city_geom = unary_union(
        geometries
    )

    if city_geom.is_empty:

        raise ValueError(
            "Merged city boundary is empty"
        )

    # ==================================================
    # WGS84 -> metric projection
    # ==================================================

    to_meters = Transformer.from_crs(
        "EPSG:4326",
        "EPSG:3857",
        always_xy=True,
    )

    to_wgs84 = Transformer.from_crs(
        "EPSG:3857",
        "EPSG:4326",
        always_xy=True,
    )

    # ==================================================
    # Convert city geometry to meters
    # ==================================================

    city_meters = transform(
        to_meters.transform,
        city_geom,
    )

    if city_meters.is_empty:

        raise ValueError(
            "Projected city geometry is empty"
        )

    # ==================================================
    # Optional padding
    # ==================================================

    if padding_km > 0:

        city_meters = city_meters.buffer(
            padding_km * 1000
        )

    # ==================================================
    # Find city center
    # ==================================================

    center = city_meters.centroid

    if center.is_empty:

        raise ValueError(
            "Unable to determine city center"
        )

    # ==================================================
    # Create safe circular AOI
    # ==================================================

    max_area_m2 = (
        MAX_AOI_AREA_KM2
        * 1_000_000
    )

    # Radius corresponding to the maximum
    # configured area.
    radius_m = sqrt(
        max_area_m2 / pi
    )

    # Additional safety margin.
    radius_m *= 0.95

    # 32 segments keeps the polygon reasonably
    # lightweight while still looking smooth.
    aoi_meters = center.buffer(
        radius_m,
        resolution=32,
    )

    # ==================================================
    # Ensure Polygon
    # ==================================================

    if aoi_meters.geom_type != "Polygon":

        aoi_meters = aoi_meters.convex_hull

    if aoi_meters.is_empty:

        raise ValueError(
            "Generated AOI is empty"
        )

    # ==================================================
    # Simplify geometry
    # ==================================================

    aoi_meters = aoi_meters.simplify(
        50,
        preserve_topology=True,
    )

    if aoi_meters.is_empty:

        raise ValueError(
            "Simplified AOI is empty"
        )

    # ==================================================
    # Calculate final area
    # ==================================================

    area_km2 = (
        aoi_meters.area
        / 1_000_000
    )

    area_mi2 = (
        area_km2
        * 0.386102
    )

    # ==================================================
    # Final safety validation
    # ==================================================

    if area_km2 > MAX_AOI_AREA_KM2:

        raise ValueError(
            "Generated Heatmap AOI exceeds "
            f"configured limit: "
            f"{area_km2:.2f} km²"
        )

    if aoi_meters.geom_type != "Polygon":

        raise ValueError(
            "Generated Heatmap AOI must be Polygon"
        )

    # ==================================================
    # Convert back to WGS84
    # ==================================================

    aoi_wgs84 = transform(
        to_wgs84.transform,
        aoi_meters,
    )

    if aoi_wgs84.is_empty:

        raise ValueError(
            "Generated WGS84 AOI is empty"
        )

    if aoi_wgs84.geom_type != "Polygon":

        raise ValueError(
            "Generated WGS84 AOI must be Polygon"
        )

    # ==================================================
    # Validate coordinates
    # ==================================================

    if len(aoi_wgs84.exterior.coords) < 4:

        raise ValueError(
            "Generated Polygon has invalid coordinates"
        )

    # ==================================================
    # Debug
    # ==================================================

    print(
        "\n===== HEATMAP AOI ====="
    )

    print(
        "Geometry:",
        aoi_wgs84.geom_type
    )

    print(
        "Bounds:",
        aoi_wgs84.bounds
    )

    print(
        "Padding:",
        padding_km,
        "km"
    )

    print(
        "Area:",
        round(
            area_km2,
            2
        ),
        "km²"
    )

    print(
        "Area:",
        round(
            area_mi2,
            2
        ),
        "mi²"
    )

    print(
        "Configured limit:",
        f"{MAX_AOI_AREA_KM2} km²"
    )

    print(
        "FortyGuard Basic limit:",
        "10 mi² (~25.9 km²)"
    )

    print(
        "Coordinates:",
        len(
            aoi_wgs84.exterior.coords
        )
    )

    print(
        "=======================\n"
    )

    # ==================================================
    # FortyGuard-compatible GeoJSON Polygon
    # ==================================================

    return mapping(
        aoi_wgs84
    )