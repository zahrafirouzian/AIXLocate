export default function ScoreCard({
  score,
}: {
  score: number;
}) {
  const numericScore = Number(score ?? 0);

  const level =
    numericScore >= 80
      ? "Strong"
      : numericScore >= 60
      ? "Moderate"
      : "Low";

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

      <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
        AI Data Center Suitability
      </p>

      <p className="mt-3 text-5xl font-bold text-gray-900">
        {numericScore.toFixed(2)}
        <span className="text-2xl text-gray-400">
          /100
        </span>
      </p>

      <p className="mt-3 text-sm text-gray-500">
        Overall climate and environmental suitability
      </p>

      <div className="mt-5 flex items-center gap-2">

        <div
          className={`h-2.5 w-2.5 rounded-full ${
            level === "Strong"
              ? "bg-green-500"
              : level === "Moderate"
              ? "bg-yellow-500"
              : "bg-red-500"
          }`}
        />

        <p className="text-sm font-semibold text-gray-800">
          Status: {level}
        </p>

      </div>

    </div>
  );
}