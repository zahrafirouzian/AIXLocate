"use client";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  GeoJSON,
  useMap,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import L from "leaflet";
import { useEffect, useMemo } from "react";

delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",

  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",

  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});


function MapUpdater({
  locations,
}: {
  locations: any[];
}) {

  const map = useMap();

  useEffect(() => {

    if (!locations?.length) {
      return;
    }

    const bounds = L.latLngBounds(
      locations.map(
        (location) => [
          location.lat,
          location.lon,
        ]
      )
    );

    map.fitBounds(
      bounds,
      {
        padding: [50, 50],
        maxZoom: 12,
      }
    );

  }, [locations, map]);

  return null;
}


export default function ClimateMap({
  locations,
  heatmap,
}: {
  locations: any[];
  heatmap?: any;
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

  const center: [number, number] =
    validLocations.length > 0
      ? [
          validLocations[0].lat,
          validLocations[0].lon,
        ]
      : [33.4484, -112.0740];

  return (
    <div className="mt-8 h-[600px] overflow-hidden rounded-xl">

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

        {heatmap && (
          <GeoJSON
            data={heatmap}
            style={(feature: any) => {

              const temp =
                feature?.properties?.average_temperature ?? 0;

              let color = "#00ff00";

              if (temp > 39.3) {
                color = "#ff0000";
              }
              else if (temp > 39.15) {
                color = "#ff8800";
              }
              else if (temp > 39.05) {
                color = "#ffff00";
              }

              return {
                color,
                weight: 1,
                fillOpacity: 0.45,
              };
            }}
          />
        )}

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
                    {location.suitability_score}
                  </p>

                  <p>
                    <strong>Temperature:</strong>{" "}
                    {location.temperature} °C
                  </p>

                  <p>
                    <strong>Solar GHI:</strong>{" "}
                    {location.solar_ghi}
                  </p>

                  <p>
                    <strong>Solar DNI:</strong>{" "}
                    {location.solar_dni}
                  </p>

                </div>

              </Popup>

            </Marker>
          )
        )}

      </MapContainer>

    </div>
  );
}