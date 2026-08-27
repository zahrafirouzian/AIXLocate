import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export function exportReport(result: any) {
  const doc = new jsPDF();

  const PRIMARY = [37, 99, 235];
  const SUCCESS = [22, 163, 74];
  const DARK = [17, 24, 39];
  const GRAY = [107, 114, 128];

  const sortedLocations = [...(result.locations ?? [])].sort(
    (a, b) =>
      (b.suitability_score ?? 0) -
      (a.suitability_score ?? 0)
  );

  const best = sortedLocations[0];

  // =====================================================
  // COVER PAGE
  // =====================================================

  doc.setTextColor(...PRIMARY);

  doc.setFontSize(28);
  doc.text("AIXLocate", 105, 40, {
    align: "center",
  });

  doc.setTextColor(...DARK);

  doc.setFontSize(18);
  doc.text(
    "AI Infrastructure Site Intelligence",
    105,
    55,
    { align: "center" }
  );

  doc.setFontSize(22);
  doc.text(
    "Climate Intelligence Report",
    105,
    80,
    { align: "center" }
  );

  doc.setDrawColor(...PRIMARY);

  doc.line(40, 90, 170, 90);

  doc.setFontSize(12);

  doc.setTextColor(...GRAY);

  doc.text(
    `Generated: ${new Date().toLocaleDateString()}`,
    105,
    105,
    { align: "center" }
  );

  doc.roundedRect(
    35,
    130,
    140,
    50,
    4,
    4
  );

  doc.setTextColor(...GRAY);

  doc.setFontSize(12);

  doc.text(
    "BEST LOCATION",
    105,
    145,
    {
      align: "center",
    }
  );

  doc.setTextColor(...DARK);

  doc.setFontSize(20);

  doc.text(
    best?.name ?? "N/A",
    105,
    158,
    {
      align: "center",
    }
  );

  doc.setTextColor(...SUCCESS);

  doc.setFontSize(26);

  doc.text(
    `${best?.suitability_score ?? 0}/100`,
    105,
    172,
    {
      align: "center",
    }
  );

  // =====================================================
  // EXECUTIVE SUMMARY
  // =====================================================

  doc.addPage();

  let y = 25;

  doc.setTextColor(...PRIMARY);

  doc.setFontSize(20);

  doc.text(
    "Executive Summary",
    20,
    y
  );

  y += 15;

  doc.setTextColor(...DARK);

  doc.setFontSize(12);

  const summary =
    `AIXLocate analyzed ${
      sortedLocations.length
    } candidate locations for AI infrastructure deployment.\n\n` +
    `Based on climate suitability, cooling efficiency, thermal stability, and renewable energy potential, ${
      best?.name ?? "N/A"
    } achieved the highest score with ${
      best?.suitability_score ?? 0
    }/100.`;

  const summaryLines =
    doc.splitTextToSize(
      summary,
      170
    );

  doc.text(
    summaryLines,
    20,
    y
  );

  y += 40;

  // Best Location Card

  doc.setDrawColor(...PRIMARY);

  doc.roundedRect(
    15,
    y,
    180,
    35,
    4,
    4
  );

  doc.setFontSize(12);

  doc.setTextColor(...GRAY);

  doc.text(
    "Recommended Location",
    25,
    y + 12
  );

  doc.setFontSize(18);

  doc.setTextColor(...DARK);

  doc.text(
    best?.name ?? "N/A",
    25,
    y + 24
  );

  doc.setTextColor(...SUCCESS);

  doc.setFontSize(22);

  doc.text(
    `${best?.suitability_score ?? 0}`,
    165,
    y + 24
  );

  y += 55;

  // =====================================================
  // RANKING TABLE
  // =====================================================

  doc.setTextColor(...PRIMARY);

  doc.setFontSize(18);

  doc.text(
    "Location Ranking",
    20,
    y
  );

  y += 8;

  autoTable(doc, {
    startY: y,

    head: [
      [
        "Rank",
        "Location",
        "Score",
      ],
    ],

    body: sortedLocations.map(
      (
        location,
        index
      ) => [
        index + 1,
        location.name,
        location.suitability_score ?? 0,
      ]
    ),

    theme: "grid",
  });

  // =====================================================
  // METRICS PAGE
  // =====================================================

  doc.addPage();

  y = 25;

  doc.setTextColor(...PRIMARY);

  doc.setFontSize(20);

  doc.text(
    "Location Metrics",
    20,
    y
  );

  y += 15;

  sortedLocations.forEach(
    (location) => {
      if (y > 230) {
        doc.addPage();
        y = 20;
      }

      doc.setTextColor(...PRIMARY);

      doc.setFontSize(14);

      doc.text(
        location.name,
        20,
        y
      );

      y += 8;

      autoTable(doc, {
        startY: y,

        head: [
          [
            "Metric",
            "Value",
          ],
        ],

        body: [
          [
            "Temperature",
            `${location.temperature ?? "-"} °C`,
          ],
          [
            "Cooling Score",
            location.cooling_score ?? "-",
          ],
          [
            "Thermal Score",
            location.thermal_score ?? "-",
          ],
          [
            "Solar GHI",
            location.solar_ghi ?? "-",
          ],
          [
            "Solar DNI",
            location.solar_dni ?? "-",
          ],
        ],

        theme: "striped",
      });

      y =
        (doc as any)
          .lastAutoTable
          .finalY + 15;
    }
  );

  // =====================================================
  // AI ANALYSIS
  // =====================================================

  doc.addPage();

  y = 25;

  doc.setTextColor(...PRIMARY);

  doc.setFontSize(20);

  doc.text(
    "AI Climate Analysis",
    20,
    y
  );

  y += 15;

  doc.setTextColor(...DARK);

  doc.setFontSize(12);

  const analysis =
    result.analysis?.report ??
    "No analysis available.";

  const paragraphs =
    analysis.split("\n");

  paragraphs.forEach(
    (paragraph) => {
      const lines =
        doc.splitTextToSize(
          paragraph,
          170
        );

      doc.text(
        lines,
        20,
        y
      );

      y +=
        lines.length * 6 +
        6;

      if (y > 260) {
        doc.addPage();
        y = 20;
      }
    }
  );

  // =====================================================
  // FOOTER
  // =====================================================

  const totalPages =
    doc.getNumberOfPages();

  for (
    let i = 1;
    i <= totalPages;
    i++
  ) {
    doc.setPage(i);

    doc.setDrawColor(
      220,
      220,
      220
    );

    doc.line(
      15,
      285,
      195,
      285
    );

    doc.setTextColor(...GRAY);

    doc.setFontSize(9);

    doc.text(
      "AIXLocate | AI Infrastructure Intelligence Platform",
      15,
      291
    );

    doc.text(
      `Page ${i}/${totalPages}`,
      180,
      291
    );
  }

  doc.save(
    "AIXLocate_Climate_Report.pdf"
  );
}