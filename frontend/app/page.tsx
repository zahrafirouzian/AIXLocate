"use client";

import { useState } from "react";
import dynamic from "next/dynamic";

import { analyzeLocation } from "@/services/api";
import { exportReport } from "@/services/pdf";

import ScoreCard from "@/components/ScoreCard";
import LocationCard from "@/components/LocationCard";
import ReportCard from "@/components/ReportCard";
import RankingBar from "@/components/RankingBar";

const ClimateMap = dynamic(
  () => import("@/components/map/ClimateMap"),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-[500px] items-center justify-center rounded-2xl bg-gray-100">
        <p className="text-sm text-gray-500">
          Loading map...
        </p>
      </div>
    ),
  }
);

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [city, setCity] = useState("");

  async function runAnalysis() {
    setError("");
    setResult(null);

    if (!city.trim()) {
      setError("Please enter a city.");
      return;
    }

    try {
      setLoading(true);

      const data = {
        city: city.trim(),
        query: `Find the best location for an AI data center in ${city}`,
      };

      const response = await analyzeLocation(data);

      console.log("AIXLocate API Response:", response);
      console.log("Heatmap:", response.heatmap);

      setResult(response);

    } catch (error) {
      console.error("Analysis error:", error);

      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Something went wrong while analyzing the location.");
      }
    } finally {
      setLoading(false);
    }
  }

  const bestLocation = result?.best_location;
  const locations = result?.locations ?? [];

  return (
    <main className="min-h-screen bg-[#f5f6f8] text-gray-900">

      {/* TOP BAR */}
      <header className="sticky top-0 z-20 border-b border-gray-200 bg-white/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-[1600px] items-center justify-between px-5 sm:px-8 lg:px-10">

          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-black text-xs font-bold text-white">
              AI
            </div>

            <div>
              <h1 className="font-bold tracking-tight">
                AIXLocate
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="hidden text-sm text-gray-500 sm:block">
              AI-powered location analysis
            </span>

            <div className="h-2.5 w-2.5 rounded-full bg-green-500" />
          </div>

        </div>
      </header>


      <div className="mx-auto flex max-w-[1600px]">

        {/* SIDEBAR */}
        <aside className="hidden min-h-[calc(100vh-64px)] w-60 border-r border-gray-200 bg-white p-5 lg:block">

          <div className="mb-8">
            <p className="px-3 text-xs font-semibold uppercase tracking-wider text-gray-400">
              Workspace
            </p>
          </div>

          <nav className="space-y-1">

            <div className="rounded-xl bg-gray-100 px-4 py-3 text-sm font-semibold text-gray-900">
              Dashboard
            </div>

            <div className="rounded-xl px-4 py-3 text-sm text-gray-500 transition hover:bg-gray-50">
              Location Analysis
            </div>

            <div className="rounded-xl px-4 py-3 text-sm text-gray-500 transition hover:bg-gray-50">
              Reports
            </div>

          </nav>

          <div className="mt-10 rounded-2xl bg-gray-50 p-4">
            <p className="text-xs font-semibold text-gray-700">
              AIXLocate
            </p>

            <p className="mt-2 text-xs leading-5 text-gray-500">
              Climate-aware intelligence for AI infrastructure.
            </p>
          </div>

        </aside>


        {/* MAIN CONTENT */}
        <section className="w-full px-5 py-8 sm:px-8 lg:px-10">

          {/* PAGE HEADER */}
          <div className="mb-8">

            <p className="text-sm font-medium text-gray-500">
              Dashboard
            </p>

            <h2 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
              Climate Intelligence
            </h2>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-500">
              Analyze environmental conditions and discover the
              most suitable location for AI data center deployment.
            </p>

          </div>


          {/* ANALYSIS CARD */}
          <section className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm sm:p-8">

            <div className="mb-6">
              <h3 className="text-lg font-semibold">
                Analyze a Location
              </h3>

              <p className="mt-1 text-sm text-gray-500">
                Enter a U.S. city to start the climate analysis.
              </p>
            </div>


            <div className="flex flex-col gap-4 sm:flex-row sm:items-end">

              <div className="flex-1">

                <label className="mb-2 block text-sm font-medium text-gray-700">
                  City
                </label>

                <input
                  value={city}
                  onChange={(e) => {
                    setCity(e.target.value);
                    setError("");
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !loading) {
                      runAnalysis();
                    }
                  }}
                  className="h-12 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 text-sm outline-none transition placeholder:text-gray-400 focus:border-gray-400 focus:bg-white focus:ring-4 focus:ring-gray-100"
                  placeholder="Enter a U.S. city"
                />

              </div>


              <button
                onClick={runAnalysis}
                disabled={loading}
                className="h-12 rounded-xl bg-black px-7 text-sm font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze Location →"}
              </button>

            </div>


            {/* ERROR */}
            {error && (
              <div className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4">
                <p className="text-sm font-semibold text-red-700">
                  ⚠️ Analysis Error
                </p>

                <p className="mt-1 text-sm text-red-600">
                  {error}
                </p>
              </div>
            )}

          </section>


          {/* LOADING */}
          {loading && (
            <section className="mt-6 rounded-2xl border border-blue-100 bg-blue-50 p-6">

              <div className="flex items-center gap-3">
                <div className="h-3 w-3 animate-pulse rounded-full bg-blue-500" />

                <p className="text-sm font-medium text-blue-900">
                  AI is analyzing climate conditions...
                </p>
              </div>

              <div className="mt-4 grid gap-2 text-xs text-blue-700 sm:grid-cols-3">
                <span>
                  🌎 Querying climate data
                </span>

                <span>
                  ☀ Analyzing environmental conditions
                </span>

                <span>
                  🤖 Generating AI recommendation
                </span>
              </div>

            </section>
          )}


          {/* RESULTS */}
          {result && (
            <div className="mt-8 space-y-8">

              {/* KPI CARDS */}
              <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">

                <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                  <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                    Best Score
                  </p>

                  <p className="mt-3 text-3xl font-bold">
                    {bestLocation?.score ?? 0}
                  </p>

                  <p className="mt-1 text-xs text-gray-500">
                    Climate suitability score
                  </p>

                </div>


                <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                  <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                    Candidates
                  </p>

                  <p className="mt-3 text-3xl font-bold">
                    {locations.length}
                  </p>

                  <p className="mt-1 text-xs text-gray-500">
                    Locations analyzed
                  </p>

                </div>


                <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">

                  <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                    Analysis Status
                  </p>

                  <div className="mt-3 flex items-center gap-2">

                    <div className="h-2.5 w-2.5 rounded-full bg-green-500" />

                    <p className="text-xl font-bold">
                      Complete
                    </p>

                  </div>

                  <p className="mt-1 text-xs text-gray-500">
                    AI recommendation generated
                  </p>

                </div>

              </div>


              {/* RECOMMENDED LOCATION */}
              <section className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">

                <div className="border-b border-gray-100 px-6 py-4">
                  <p className="text-xs font-semibold uppercase tracking-wider text-gray-400">
                    Recommended Location
                  </p>
                </div>


                <div className="flex flex-col justify-between gap-5 p-6 sm:flex-row sm:items-center">

                  <div className="flex items-center gap-4">

                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gray-100 text-xl">
                      🏆
                    </div>

                    <div>

                      <h3 className="text-2xl font-bold">
                        {bestLocation?.name}
                      </h3>

                      <p className="mt-1 text-sm text-gray-500">
                        Best AI data center deployment candidate
                      </p>

                    </div>

                  </div>


                  <div className="sm:text-right">

                    <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                      Score
                    </p>

                    <p className="mt-1 text-4xl font-bold">
                      {bestLocation?.score ?? 0}
                    </p>

                  </div>

                </div>

              </section>


              {/* SCORE */}
              <section>
                <ScoreCard
                  score={bestLocation?.score ?? 0}
                />
              </section>


              {/* MAP + RANKING */}
              <section>

                <div className="mb-4">

                  <h3 className="text-lg font-bold">
                    Climate Intelligence
                  </h3>

                  <p className="mt-1 text-sm text-gray-500">
                    Geographic climate suitability analysis
                  </p>

                </div>


                <div className="grid gap-6 xl:grid-cols-[1.7fr_1fr]">

                  {/* MAP */}
                  <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white p-3 shadow-sm">

                    <ClimateMap
                      locations={locations}
                      heatmap={result.heatmap}
                    />

                  </div>


                  {/* RANKING */}
                  <div className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">

                    <div className="mb-5">

                      <h3 className="font-semibold">
                        Location Ranking
                      </h3>

                      <p className="mt-1 text-xs text-gray-500">
                        Climate suitability comparison
                      </p>

                    </div>

                    <RankingBar
                      locations={locations}
                    />

                  </div>

                </div>

              </section>


              {/* CANDIDATE LOCATIONS */}
              <section>

                <div className="mb-5">

                  <h3 className="text-lg font-bold">
                    Candidate Locations
                  </h3>

                  <p className="mt-1 text-sm text-gray-500">
                    Detailed analysis of all evaluated locations
                  </p>

                </div>


                <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">

                  {locations.map(
                    (location: any) => (
                      <LocationCard
                        key={location.name}
                        location={location}
                      />
                    )
                  )}

                </div>

              </section>


              {/* AI REPORT */}
              <section>

                <div className="mb-5">

                  <h3 className="text-lg font-bold">
                    AI Analysis
                  </h3>

                  <p className="mt-1 text-sm text-gray-500">
                    AI-generated climate intelligence report
                  </p>

                </div>


                <ReportCard
                  report={
                    result.analysis?.report ??
                    "No report available"
                  }
                />

              </section>


              {/* EXPORT */}
              <section className="flex justify-end border-t border-gray-200 pt-6">

                <button
                  onClick={() => exportReport(result)}
                  className="rounded-xl bg-black px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-gray-800"
                >
                  📄 Export PDF Report
                </button>

              </section>

            </div>
          )}

        </section>

      </div>

    </main>
  );
}
