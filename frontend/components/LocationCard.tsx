export default function LocationCard({
  location,
  recommended,
}: {
  location: any;
  recommended: boolean;
}) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4">
        <h2 className="text-xl font-bold">
          {location.name}
        </h2>

        {recommended && (
          <span className="whitespace-nowrap rounded-lg bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
            🏆 Recommended
          </span>
        )}
      </div>

      <div className="mt-5 space-y-2 text-sm text-gray-700">
        <p>
          🌡 Temperature: {location.temperature}°C
        </p>

        <p>
          ☀ Solar GHI: {location.solar_ghi}
        </p>

        <p>
          🔆 Solar DNI: {location.solar_dni}
        </p>

        <p>
          ❄ Cooling: {location.cooling_score}
        </p>

        <p>
          🔥 Thermal: {location.thermal_score}
        </p>

        <p className="pt-2 font-bold text-gray-900">
          ⭐ Suitability: {location.suitability_score}
        </p>
      </div>
    </div>
  );
}