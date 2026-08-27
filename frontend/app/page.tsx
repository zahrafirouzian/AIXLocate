"use client";

import { useState } from "react";
import dynamic from "next/dynamic";

import { analyzeLocation } from "@/services/api";

import ScoreCard from "@/components/ScoreCard";
import LocationCard from "@/components/LocationCard";
import ReportCard from "@/components/ReportCard";
import RankingBar from "@/components/RankingBar";

const ClimateMap = dynamic(
  () => import("@/components/map/ClimateMap"),
  {
    ssr: false,
    loading: () => (
      <div className="mt-8 rounded-xl bg-gray-100 p-10 text-center">
        Loading map...
      </div>
    ),
  }
);

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const [city, setCity] = useState("Phoenix");
  const [capacity, setCapacity] = useState("100");

  async function runAnalysis() {
    try {
      setLoading(true);

      const data = {
        city,
        capacity,

        query: `Find the best location for a ${capacity}MW AI data center in ${city}`,
      };

      const response = await analyzeLocation(data);

      setResult(response);
    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-10">
      <h1 className="text-4xl font-bold">AIXLocate</h1>

      <p className="mt-2 text-gray-600">
        AI Climate Intelligence for Data Centers
      </p>

      <div className="mt-8 grid gap-4 md:grid-cols-2">
        <div>
          <label className="mb-2 block font-medium">
            City
          </label>

          <input
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full rounded-lg border bg-white p-3"
            placeholder="Phoenix"
          />
        </div>

        <div>
          <label className="mb-2 block font-medium">
            Capacity (MW)
          </label>

          <input
            value={capacity}
            onChange={(e) => setCapacity(e.target.value)}
            className="w-full rounded-lg border bg-white p-3"
            placeholder="100"
          />
        </div>
      </div>

      <button
        onClick={runAnalysis}
        disabled={loading}
        className="mt-6 rounded bg-black px-5 py-3 text-white disabled:opacity-50"
      >
        {loading
          ? "Analyzing Climate..."
          : "Analyze Location"}
      </button>

      {loading && (
        <div className="mt-6 rounded-xl bg-blue-50 p-5">
          <p>🌎 Querying climate data...</p>
          <p>☀ Analyzing solar conditions...</p>
          <p>🤖 Generating AI recommendation...</p>
        </div>
      )}

      {result && (
        <div className="mt-10 space-y-8">
          <div className="rounded-xl bg-white p-6 shadow">
            <h2 className="text-3xl font-bold">
              🏆 Recommended Location:{" "}
              {result.best_location.name}
            </h2>

            <p className="mt-2 text-gray-600">
              Best AI data center deployment candidate
            </p>
          </div>

          <ScoreCard
            score={result.best_location.score}
          />

          <RankingBar
            locations={result.locations}
          />

          <div className="grid gap-6 md:grid-cols-2">
            {result.locations.map((location: any) => (
              <LocationCard
                key={location.name}
                location={location}
              />
            ))}
          </div>

          <ClimateMap
            locations={result.locations}
          />

          <ReportCard
            report={result.analysis.report}
          />
        </div>
      )}
    </main>
  );
}