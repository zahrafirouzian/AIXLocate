

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

        let assessment =
          "Moderate";

        if (
          locationScore >= 80
        ) {
          assessment =
            "Strong";
        } else if (
          locationScore < 60
        ) {
          assessment =
            "Low";
        }

        return [
          index + 1,
          location.name ??
            "Unknown",
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