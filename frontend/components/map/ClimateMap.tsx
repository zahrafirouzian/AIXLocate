"use client";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import L from "leaflet";
import { useEffect, useMemo } from "react";

// Fix Leaflet icons
delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});


// Move map when locations change
function MapUpdater({
  locations,
}: {
  locations: any[];
}) {
  const map = useMap();

  useEffect(() => {
    if (!locations || locations.length === 0) {
      return;
    }

    const validLocations = locations.filter(
      (location) =>
        typeof location.lat === "number" &&
        typeof location.lon === "number"
    );

    if (validLocations.length === 0) {
      return;
    }

    const bounds = L.latLngBounds(
      validLocations.map((location) => [
        location.lat,
        location.lon,
      ])
    );

    map.fitBounds(bounds, {
      padding: [50, 50],
      maxZoom: 12,
    });
  }, [locations, map]);

  return null;
}


export default function ClimateMap({
  locations,
}: {
  locations: any[];
}) {

  const validLocations = useMemo(
    () =>
      (locations || []).filter(
        (location) =>
          typeof location.lat === "number" &&
          typeof location.lon === "number"
      ),
    [locations]
  );


  // Default center
  const center: [number, number] =
    validLocations.length > 0
      ? [
          validLocations[0].lat,
          validLocations[0].lon,
        ]
      : [33.4484, -112.0740];


  return (
    <div className="mt-8 h-[500px] overflow-hidden rounded-xl">

      <MapContainer
        center={center}
        zoom={11}
        style={{
          height: "100%",
          width: "100%",
        }}
      >

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />


        <MapUpdater
          locations={validLocations}
        />


        {validLocations.map(
          (location) => (
            <Marker
              key={location.name}
              position={[
                location.lat,
                location.lon,
              ]}
            >

              <Popup>

                <div className="min-w-[180px]">

                  <h3 className="font-bold text-lg">
                    {location.name}
                  </h3>


                  <p className="mt-2">
                    <strong>Score:</strong>{" "}
                    {location.suitability_score ?? "N/A"}
                  </p>


                  <p>
                    <strong>Temperature:</strong>{" "}
                    {location.temperature ?? "N/A"} °C
                  </p>


                  {location.solar_ghi !== undefined && (
                    <p>
                      <strong>Solar GHI:</strong>{" "}
                      {location.solar_ghi}
                    </p>
                  )}


                  {location.solar_dni !== undefined && (
                    <p>
                      <strong>Solar DNI:</strong>{" "}
                      {location.solar_dni}
                    </p>
                  )}

                </div>

              </Popup>

            </Marker>
          )
        )}

      </MapContainer>

    </div>
  );
}