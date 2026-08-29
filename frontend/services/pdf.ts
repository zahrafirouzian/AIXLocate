import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

export function exportReport(result: any) {
  const doc = new jsPDF();

  // =====================================================
  // DESIGN SYSTEM
  // =====================================================

  const PRIMARY = [37, 99, 235];
  const SUCCESS = [22, 163, 74];
  const DARK = [17, 24, 39];
  const GRAY = [107, 114, 128];
  const LIGHT = [243, 244, 246];
  const BORDER = [229, 231, 235];

  const PAGE_WIDTH = 210;
  const MARGIN = 20;
  const CONTENT_WIDTH = 170;

  // =====================================================
  // TYPOGRAPHY
  // =====================================================

  const FONT = "helvetica";
  const FONT_TITLE = 20;
  const FONT_SUBTITLE = 9;
  const FONT_BODY = 10;
  const FONT_SMALL = 8.5;
  const FONT_TABLE = 9;
  const FONT_HEADER = 8;
  const FONT_SECTION = 12;

  // =====================================================
  // DATA
  // =====================================================

  const sortedLocations = [...(result.locations ?? [])].sort(
    (a, b) =>
      (b.suitability_score ?? 0) -
      (a.suitability_score ?? 0)
  );

  const best = sortedLocations[0];

  const score = Number(
    best?.suitability_score ?? 0
  );

  const scoreText = score.toFixed(2);

  const generatedDate = new Date().toLocaleDateString(
    "en-US",
    {
      year: "numeric",
      month: "long",
      day: "numeric",
    }
  );

  // =====================================================
  // HELPERS
  // =====================================================

  function sectionTitle(
    title: string,
    subtitle?: string
  ) {
    doc.setTextColor(...PRIMARY);
    doc.setFontSize(FONT_TITLE);
    doc.setFont(FONT, "bold");

    doc.text(
      title,
      MARGIN,
      25
    );

    if (subtitle) {
      doc.setTextColor(...GRAY);
      doc.setFontSize(FONT_SUBTITLE);
      doc.setFont(FONT, "normal");

      doc.text(
        subtitle,
        MARGIN,
        32
      );
    }
  }

  function addPageHeader(title: string) {
    doc.setTextColor(...PRIMARY);
    doc.setFontSize(FONT_HEADER);
    doc.setFont(FONT, "bold");

    doc.text(
      "AIXLocate",
      MARGIN,
      12
    );

    doc.setTextColor(...GRAY);
    doc.setFont(FONT, "normal");

    doc.text(
      title,
      PAGE_WIDTH - MARGIN,
      12,
      {
        align: "right",
      }
    );

    doc.setDrawColor(...BORDER);

    doc.line(
      MARGIN,
      15,
      PAGE_WIDTH - MARGIN,
      15
    );
  }

  function addFooter() {
    const totalPages =
      doc.getNumberOfPages();

    for (
      let i = 1;
      i <= totalPages;
      i++
    ) {
      doc.setPage(i);

      doc.setDrawColor(...BORDER);

      doc.line(
        MARGIN,
        285,
        PAGE_WIDTH - MARGIN,
        285
      );

      doc.setTextColor(...GRAY);
      doc.setFontSize(8);
      doc.setFont(FONT, "normal");

      doc.text(
        "AIXLocate | AI Infrastructure Site Intelligence",
        MARGIN,
        291
      );

      doc.text(
        `Page ${i} / ${totalPages}`,
        PAGE_WIDTH - MARGIN,
        291,
        {
          align: "right",
        }
      );
    }
  }

  function metricValue(
    value: any,
    suffix = ""
  ) {
    if (
      value === undefined ||
      value === null ||
      value === ""
    ) {
      return "—";
    }

    return `${value}${suffix}`;
  }

  // =====================================================
  // COVER PAGE
  // =====================================================

  doc.setFillColor(...PRIMARY);

  doc.rect(
    0,
    0,
    PAGE_WIDTH,
    8,
    "F"
  );

  doc.setTextColor(...PRIMARY);
  doc.setFont(FONT, "bold");
  doc.setFontSize(30);

  doc.text(
    "AIXLocate",
    PAGE_WIDTH / 2,
    48,
    {
      align: "center",
    }
  );

  doc.setTextColor(...DARK);
  doc.setFontSize(17);
  doc.setFont(FONT, "bold");

  doc.text(
    "AI Infrastructure Site Intelligence",
    PAGE_WIDTH / 2,
    62,
    {
      align: "center",
    }
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(11);
  doc.setFont(FONT, "normal");

  doc.text(
    "Climate-Based Location Assessment",
    PAGE_WIDTH / 2,
    72,
    {
      align: "center",
    }
  );

  doc.setDrawColor(...PRIMARY);

  doc.line(
    55,
    84,
    155,
    84
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);
  doc.setFont(FONT, "bold");

  doc.text(
    "DECISION REPORT",
    PAGE_WIDTH / 2,
    100,
    {
      align: "center",
    }
  );

  doc.setDrawColor(...BORDER);
  doc.setFillColor(...LIGHT);

  doc.roundedRect(
    30,
    115,
    150,
    75,
    5,
    5,
    "FD"
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);
  doc.setFont(FONT, "bold");

  doc.text(
    "RECOMMENDED LOCATION",
    PAGE_WIDTH / 2,
    130,
    {
      align: "center",
    }
  );

  doc.setTextColor(...DARK);
  doc.setFontSize(21);
  doc.setFont(FONT, "bold");

  doc.text(
    best?.name ?? "N/A",
    PAGE_WIDTH / 2,
    147,
    {
      align: "center",
    }
  );

  doc.setTextColor(...SUCCESS);
  doc.setFontSize(27);
  doc.setFont(FONT, "bold");

  doc.text(
    `${scoreText}/100`,
    PAGE_WIDTH / 2,
    170,
    {
      align: "center",
    }
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);
  doc.setFont(FONT, "normal");

  doc.text(
    "Overall Suitability Score",
    PAGE_WIDTH / 2,
    181,
    {
      align: "center",
    }
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);

  doc.text(
    `Candidate locations analyzed: ${sortedLocations.length}`,
    PAGE_WIDTH / 2,
    215,
    {
      align: "center",
    }
  );

  doc.text(
    `Generated: ${generatedDate}`,
    PAGE_WIDTH / 2,
    223,
    {
      align: "center",
    }
  );

  // =====================================================
  // EXECUTIVE DECISION
  // =====================================================

  doc.addPage();

  addPageHeader(
    "Executive Decision"
  );

  sectionTitle(
    "Executive Decision",
    "Summary of the location assessment"
  );

  let y = 48;

  // =====================================================
  // RECOMMENDATION CARD
  // =====================================================

  const cardY = y;
  const cardHeight = 43;

  doc.setFillColor(...LIGHT);
  doc.setDrawColor(...BORDER);

  doc.roundedRect(
    MARGIN,
    cardY,
    CONTENT_WIDTH,
    cardHeight,
    4,
    4,
    "FD"
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);
  doc.setFont(FONT, "bold");

  doc.text(
    "RECOMMENDATION",
    MARGIN + 10,
    cardY + 12
  );

  doc.setTextColor(...DARK);
  doc.setFontSize(17);
  doc.setFont(FONT, "bold");

  doc.text(
    best?.name ?? "N/A",
    MARGIN + 10,
    cardY + 27
  );

  doc.setTextColor(...SUCCESS);
  doc.setFontSize(17);

  doc.text(
    `${scoreText}/100`,
    PAGE_WIDTH - MARGIN - 10,
    cardY + 27,
    {
      align: "right",
    }
  );

  // =====================================================
  // ASSESSMENT SUMMARY
  // =====================================================

  y =
    cardY +
    cardHeight +
    18;

  doc.setTextColor(...DARK);
  doc.setFontSize(FONT_SECTION);
  doc.setFont(FONT, "bold");

  doc.text(
    "Assessment Summary",
    MARGIN,
    y
  );

  y += 9;

  doc.setTextColor(...DARK);
  doc.setFont(FONT, "normal");
  doc.setFontSize(FONT_BODY);

  const summary =
    `AIXLocate evaluated ${sortedLocations.length} candidate locations ` +
    `for AI infrastructure deployment. The locations were compared using ` +
    `available climate and environmental metrics and a suitability scoring system.`;

  const summaryLines =
    doc.splitTextToSize(
      summary,
      CONTENT_WIDTH
    );

  doc.text(
    summaryLines,
    MARGIN,
    y
  );

  y +=
    summaryLines.length *
      5 +
    12;

  const recommendation =
    `${best?.name ?? "The recommended location"} achieved the highest ` +
    `overall suitability score of ${scoreText}/100 among the analyzed candidates.`;

  const recommendationLines =
    doc.splitTextToSize(
      recommendation,
      CONTENT_WIDTH
    );

  doc.text(
    recommendationLines,
    MARGIN,
    y
  );

  // =====================================================
  // KEY METRICS
  // =====================================================

  y +=
    recommendationLines.length *
      5 +
    18;

  doc.setFont(FONT, "bold");
  doc.setFontSize(FONT_SECTION);

  doc.text(
    "Key Climate Indicators",
    MARGIN,
    y
  );

  y += 8;

  autoTable(doc, {
    startY: y,

    head: [
      [
        "Indicator",
        "Value",
        "Interpretation",
      ],
    ],

    body: [
      [
        "Temperature",
        metricValue(
          best?.temperature,
          " °C"
        ),
        "Climate condition",
      ],
      [
        "Cooling Score",
        metricValue(
          best?.cooling_score
        ),
        "Cooling suitability",
      ],
      [
        "Thermal Score",
        metricValue(
          best?.thermal_score
        ),
        "Thermal infrastructure metric",
      ],
      [
        "Solar GHI",
        metricValue(
          best?.solar_ghi
        ),
        "Solar resource indicator",
      ],
      [
        "Solar DNI",
        metricValue(
          best?.solar_dni
        ),
        "Direct solar resource indicator",
      ],
    ],

    theme: "grid",

    styles: {
      font: FONT,
      fontSize: FONT_TABLE,
      cellPadding: 5,
      textColor: DARK,
      lineColor: BORDER,
      valign: "middle",
    },

    headStyles: {
      fillColor: PRIMARY,
      textColor: [255, 255, 255],
      fontStyle: "bold",
      halign: "center",
    },

    columnStyles: {
      0: {
        cellWidth: 48,
      },
      1: {
        cellWidth: 35,
        halign: "center",
      },
      2: {
        cellWidth: 87,
      },
    },

    margin: {
      left: MARGIN,
      right: MARGIN,
    },
  });

  // =====================================================
  // LOCATION RANKING
  // =====================================================

  doc.addPage();

  addPageHeader(
    "Location Ranking"
  );

  sectionTitle(
    "Location Ranking",
    "Comparison of candidate locations by overall suitability"
  );

  y = 48;

  const rankingRows =
    sortedLocations.map(
      (location, index) => {

        const locationScore =
          Number(
            location.suitability_score ??
              0
          );

        // =================================================
        // ASSESSMENT LEVELS
        //
        // 0–39.99   -> Low
        // 40–59.99  -> Moderate
        // 60–79.99  -> Good
        // 80–100    -> High
        // =================================================

        let assessment = "Low";

        if (locationScore >= 80) {
          assessment = "High";
        } else if (locationScore >= 60) {
          assessment = "Good";
        } else if (locationScore >= 40) {
          assessment = "Moderate";
        }

        return [
          index + 1,
          location.name ?? "Unknown",
          `${locationScore.toFixed(2)}/100`,
          assessment,
        ];
      }
    );

  autoTable(doc, {
    startY: y,

    head: [
      [
        "Rank",
        "Location",
        "Suitability",
        "Assessment",
      ],
    ],

    body: rankingRows,

    theme: "grid",

    styles: {
      font: FONT,
      fontSize: 9.5,

      cellPadding: {
        top: 5,
        bottom: 5,
        left: 6,
        right: 6,
      },

      textColor: DARK,
      lineColor: BORDER,
      lineWidth: 0.2,
      valign: "middle",
    },

    headStyles: {
      fillColor: PRIMARY,
      textColor: [255, 255, 255],
      fontSize: 9,
      fontStyle: "bold",
      halign: "center",
      valign: "middle",
      cellPadding: 6,
    },

    columnStyles: {
      0: {
        halign: "center",
        cellWidth: 20,
        fontStyle: "bold",
      },

      1: {
        cellWidth: 70,
        halign: "left",
      },

      2: {
        cellWidth: 38,
        halign: "center",
        fontStyle: "bold",
      },

      3: {
        cellWidth: 42,
        halign: "center",
      },
    },

    didParseCell: (
      data
    ) => {
      if (
        data.section ===
          "body" &&
        data.row.index === 0
      ) {
        data.cell.styles.fontStyle =
          "bold";
      }
    },

    didDrawCell: (
      data
    ) => {
      if (
        data.section ===
          "body" &&
        data.row.index === 0 &&
        data.column.index === 0
      ) {
        doc.setFillColor(
          ...SUCCESS
        );

        doc.circle(
          data.cell.x +
            data.cell.width / 2,
          data.cell.y +
            data.cell.height / 2,
          2,
          "F"
        );
      }
    },

    margin: {
      left: MARGIN,
      right: MARGIN,
    },

    pageBreak: "auto",
    showHead: "everyPage",
  });

  y =
    ((doc as any)
      .lastAutoTable
      ?.finalY ??
      y) +
    16;

  doc.setTextColor(...GRAY);
  doc.setFontSize(
    FONT_SMALL
  );
  doc.setFont(FONT, "normal");

  const rankingNote =
    "Locations are ranked according to the overall suitability score produced by AIXLocate.";

  const rankingNoteLines =
    doc.splitTextToSize(
      rankingNote,
      CONTENT_WIDTH
    );

  doc.text(
    rankingNoteLines,
    MARGIN,
    y
  );

  // =====================================================
  // CLIMATE INTELLIGENCE
  // =====================================================

  doc.addPage();

  addPageHeader(
    "Climate Intelligence"
  );

  sectionTitle(
    "Climate Intelligence",
    "Environmental indicators for each candidate location"
  );

  y = 48;

  sortedLocations.forEach(
    (location) => {

      if (y > 235) {
        doc.addPage();

        addPageHeader(
          "Climate Intelligence"
        );

        y = 25;
      }

      doc.setTextColor(...PRIMARY);
      doc.setFontSize(13);
      doc.setFont(FONT, "bold");

      doc.text(
        location.name ??
          "Unknown",
        MARGIN,
        y
      );

      y += 7;

      autoTable(doc, {
        startY: y,

        head: [
          [
            "Climate Metric",
            "Observed Value",
          ],
        ],

        body: [
          [
            "Temperature",
            metricValue(
              location.temperature,
              " °C"
            ),
          ],
          [
            "Cooling Score",
            metricValue(
              location.cooling_score
            ),
          ],
          [
            "Thermal Score",
            metricValue(
              location.thermal_score
            ),
          ],
          [
            "Solar GHI",
            metricValue(
              location.solar_ghi
            ),
          ],
          [
            "Solar DNI",
            metricValue(
              location.solar_dni
            ),
          ],
        ],

        theme: "striped",

        styles: {
          font: FONT,
          fontSize: 9,
          cellPadding: 4,
          textColor: DARK,
        },

        headStyles: {
          fillColor: [
            75,
            85,
            99,
          ],

          textColor: [
            255,
            255,
            255,
          ],

          fontStyle: "bold",
        },
      });

      y =
        ((doc as any)
          .lastAutoTable
          ?.finalY ??
          y) +
        12;
    }
  );

  // =====================================================
  // SCORING FRAMEWORK
  // =====================================================

  doc.addPage();

  addPageHeader(
    "Scoring Framework"
  );

  sectionTitle(
    "Suitability Assessment",
    "How candidate locations are evaluated"
  );

  y = 48;

  doc.setTextColor(...DARK);
  doc.setFontSize(11);
  doc.setFont(FONT, "normal");

  const scoringText =
    "AIXLocate converts environmental indicators into a normalized " +
    "location suitability score. The final score is used to compare " +
    "candidate locations and identify the strongest climate profile " +
    "for AI infrastructure deployment.";

  const scoringLines =
    doc.splitTextToSize(
      scoringText,
      CONTENT_WIDTH
    );

  doc.text(
    scoringLines,
    MARGIN,
    y
  );

  y +=
    scoringLines.length *
      5 +
    15;

  autoTable(doc, {
    startY: y,

    head: [
      [
        "Evaluation Area",
        "Purpose",
      ],
    ],

    body: [
      [
        "Cooling Conditions",
        "Assess suitability of local climate for cooling requirements.",
      ],
      [
        "Thermal Infrastructure",
        "Represent the temperature-based technical infrastructure metric.",
      ],
      [
        "Solar / Environmental Load",
        "Provide a relative environmental metric based on solar GHI.",
      ],
      [
        "Overall Suitability",
        "Combine the scoring factors into a comparative location score.",
      ],
    ],

    theme: "grid",

    styles: {
      font: FONT,
      fontSize: 9,
      cellPadding: 6,
      textColor: DARK,
      lineColor: BORDER,
    },

    headStyles: {
      fillColor: PRIMARY,
      textColor: [
        255,
        255,
        255,
      ],
      fontStyle: "bold",
    },
  });

  // =====================================================
  // AI RECOMMENDATION
  // =====================================================

  doc.addPage();

  addPageHeader(
    "AI Recommendation"
  );

  sectionTitle(
    "AI Climate Analysis",
    "AI-generated interpretation of the environmental assessment"
  );

  y = 48;

  const analysis =
    result.analysis?.report ??
    "No AI analysis is available for this assessment.";

  const paragraphs =
    analysis
      .split(/\n+/)
      .map(
        (p: string) =>
          p
            .replace(/\*\*/g, "")
            .replace(/^[-•]\s*/, "")
            .trim()
      )
      .filter(Boolean);

  paragraphs.forEach(
    (paragraph: string) => {

      if (y > 255) {
        doc.addPage();

        addPageHeader(
          "AI Recommendation"
        );

        y = 25;
      }

      doc.setTextColor(...DARK);
      doc.setFontSize(FONT_BODY);
      doc.setFont(FONT, "normal");

      const lines =
        doc.splitTextToSize(
          paragraph,
          CONTENT_WIDTH
        );

      doc.text(
        lines,
        MARGIN,
        y
      );

      y +=
        lines.length *
          5 +
        8;
    }
  );

  // =====================================================
  // FINAL DECISION
  // =====================================================

  if (y > 220) {
    doc.addPage();

    addPageHeader(
      "Final Assessment"
    );

    y = 25;
  } else {
    y += 10;
  }

  doc.setFillColor(...LIGHT);
  doc.setDrawColor(...BORDER);

  doc.roundedRect(
    MARGIN,
    y,
    CONTENT_WIDTH,
    45,
    4,
    4,
    "FD"
  );

  doc.setTextColor(...GRAY);
  doc.setFontSize(9);
  doc.setFont(FONT, "bold");

  doc.text(
    "FINAL ASSESSMENT",
    MARGIN + 10,
    y + 12
  );

  doc.setTextColor(...DARK);
  doc.setFontSize(15);
  doc.setFont(FONT, "bold");

  doc.text(
    best?.name ?? "N/A",
    MARGIN + 10,
    y + 28
  );

  doc.setTextColor(...SUCCESS);
  doc.setFontSize(17);

  doc.text(
    `${scoreText}/100`,
    PAGE_WIDTH - MARGIN - 10,
    y + 28,
    {
      align: "right",
    }
  );

  // =====================================================
  // FOOTER
  // =====================================================

  addFooter();

  // =====================================================
  // EXPORT
  // =====================================================

  doc.save(
    "AIXLocate_Climate_Intelligence_Report.pdf"
  );
}