"use client";

export default function RankingBar({
  locations,
}: {
  locations: any[];
}) {
  const sortedLocations = [...locations].sort(
    (a, b) =>
      Number(b.suitability_score ?? 0) -
      Number(a.suitability_score ?? 0)
  );

  function getAssessment(score: number) {
    if (score >= 80) {
      return "Strong";
    }

    if (score >= 60) {
      return "Moderate";
    }

    return "Low";
  }

  function getStatusColor(score: number) {
    if (score >= 80) {
      return "bg-green-500";
    }

    if (score >= 60) {
      return "bg-yellow-500";
    }

    return "bg-red-500";
  }

  function getStatusTextColor(score: number) {
    if (score >= 80) {
      return "text-green-700";
    }

    if (score >= 60) {
      return "text-yellow-700";
    }

    return "text-red-700";
  }

  return (
    <div className="mt-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

      <div className="mb-5">

        <h2 className="text-xl font-bold text-gray-900">
          Location Ranking
        </h2>

        <p className="mt-1 text-sm text-gray-500">
          Climate suitability comparison
        </p>

      </div>

      <div className="space-y-5">

        {sortedLocations.map(
          (location, index) => {
            const score = Number(
              location.suitability_score ?? 0
            );

            const assessment =
              getAssessment(score);

            return (
              <div
                key={location.name}
                className="rounded-xl border border-gray-100 p-4"
              >

                {/* LOCATION HEADER */}
                <div className="mb-2 flex items-center justify-between gap-4">

                  <div className="flex items-center gap-3">

                    <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-gray-100 text-xs font-bold text-gray-700">
                      {index + 1}
                    </span>

                    <span className="font-semibold text-gray-900">
                      {location.name}
                    </span>

                  </div>

                  <div className="text-right">

                    <span className="font-bold text-gray-900">
                      {score.toFixed(2)}
                    </span>

                    <span className="text-gray-400">
                      /100
                    </span>

                  </div>

                </div>

                {/* SCORE BAR */}
                <div className="h-3 overflow-hidden rounded-full bg-gray-200">

                  <div
                    className={`h-full rounded-full transition-all ${getStatusColor(
                      score
                    )}`}
                    style={{
                      width: `${Math.max(
                        0,
                        Math.min(score, 100)
                      )}%`,
                    }}
                  />

                </div>

                {/* ASSESSMENT */}
                <div className="mt-2 flex justify-end">

                  <span
                    className={`text-xs font-semibold ${getStatusTextColor(
                      score
                    )}`}
                  >
                    {assessment}
                  </span>

                </div>

              </div>
            );
          }
        )}

      </div>

    </div>
  );
}