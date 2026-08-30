from app.models.state import ResearchState
from app.services.llm import ask_llm


def report_node(state: ResearchState):

    # ==================================================
    # SOURCE DATA
    # ==================================================

    location = state["recommendation"]
    locations = state["locations"]

    if not locations:
        raise ValueError("No locations available for report generation.")

    # ==================================================
    # FIND RECOMMENDED LOCATION
    # ==================================================

    best_location_data = next(
        (
            loc
            for loc in locations
            if loc.get("name") == location
        ),
        None,
    )

    if best_location_data is None:
        raise ValueError(
            f"Recommended location '{location}' was not found "
            "in the evaluated locations."
        )

    # ==================================================
    # AUTHORITATIVE SCORE
    # ==================================================

    try:
        score = float(
            best_location_data["suitability_score"]
        )
    except (KeyError, TypeError, ValueError):
        raise ValueError(
            f"Invalid suitability score for '{location}'."
        )

    score_text = f"{score:.2f}"

    # ==================================================
    # AUTHORITATIVE RANKING
    # ==================================================

    sorted_locations = sorted(
        locations,
        key=lambda loc: float(
            loc.get("suitability_score", 0)
        ),
        reverse=True,
    )

    ranking = next(
        (
            index + 1
            for index, loc in enumerate(sorted_locations)
            if loc.get("name") == location
        ),
        None,
    )

    if ranking is None:
        raise ValueError(
            f"Unable to determine ranking for '{location}'."
        )

    # ==================================================
    # COMPARISON LOCATION
    # ==================================================

    comparison_location = None
    comparison_score = None
    score_difference = None

    if ranking > 1:
        comparison_location = sorted_locations[ranking - 2]
    elif len(sorted_locations) > 1:
        comparison_location = sorted_locations[1]

    if comparison_location is not None:
        try:
            comparison_score = float(
                comparison_location.get(
                    "suitability_score",
                    0
                )
            )

            score_difference = round(
                abs(score - comparison_score),
                2
            )

        except (TypeError, ValueError):
            comparison_score = None
            score_difference = None

    # ==================================================
    # LOCKED CLIMATE METRICS
    # ==================================================

    temperature = best_location_data.get("temperature")
    cooling_score = best_location_data.get("cooling_score")
    thermal_score = best_location_data.get("thermal_score")
    solar_ghi = best_location_data.get("solar_ghi")
    solar_dni = best_location_data.get("solar_dni")

    # ==================================================
    # AUTHORITATIVE RANKING STATEMENT
    # ==================================================

    if ranking == 1:
        ranking_statement = (
            f"{location} ranked first among the evaluated candidates "
            "based on the provided scoring metrics."
        )
    else:
        ranking_statement = (
            f"{location} ranked #{ranking} among the evaluated candidates "
            "based on the provided scoring metrics."
        )

    # ==================================================
    # AI REPORT PROMPT
    # ==================================================

    prompt = f"""
You are AIXLocate's report-writing component.

YOUR ROLE IS ONLY TO WRITE A FACTUAL SUMMARY.

You are NOT allowed to make decisions.
You are NOT allowed to evaluate the quality of the climate.
You are NOT allowed to interpret what the numbers mean.
You are NOT allowed to provide engineering conclusions.
You are NOT allowed to provide business conclusions.

The application has already calculated the recommendation,
suitability score and ranking.

These values are AUTHORITATIVE and IMMUTABLE.

==================================================
AUTHORITATIVE DATA
==================================================

Recommended Location:
{location}

Suitability Score:
{score_text}/100

Rank:
#{ranking}

Number of Evaluated Locations:
{len(locations)}

Temperature:
{temperature}

Cooling Score:
{cooling_score}

Thermal Score:
{thermal_score}

Solar GHI:
{solar_ghi}

Solar DNI:
{solar_dni}

Comparison Location:
{comparison_location.get("name") if comparison_location else "N/A"}

Comparison Score:
{
    f"{comparison_score:.2f}"
    if comparison_score is not None
    else "N/A"
}

Score Difference:
{
    f"{score_difference:.2f}"
    if score_difference is not None
    else "N/A"
}

==================================================
AUTHORITATIVE RANKING STATEMENT
==================================================

{ranking_statement}

The application generated this statement.

You MUST preserve its meaning exactly.

==================================================
ABSOLUTE DATA RULES
==================================================

RULE 1 — RECOMMENDATION

The recommended location is exactly:

{location}

You MUST use exactly this name.

Never replace it.

Never suggest another location.

Never say another location is preferable.

Never question the recommendation.

--------------------------------------------------

RULE 2 — SCORE

The authoritative suitability score is:

{score_text}/100

You MUST use exactly:

{score_text}/100

Never calculate another score.

Never estimate another score.

Never round it differently.

Never describe its magnitude.

--------------------------------------------------

RULE 3 — RANK

The authoritative rank is:

#{ranking}

Use exactly this rank.

Never calculate another rank.

Never reinterpret the ranking.

--------------------------------------------------

RULE 4 — FACTS ONLY

Every factual statement must come directly from
the supplied authoritative data.

If a statement cannot be directly supported by the
provided data, DO NOT WRITE IT.

When uncertain, omit the statement.

--------------------------------------------------

RULE 5 — NO INTERPRETATION

You MUST NOT interpret numerical values.

For example, DO NOT say:

high temperature
low temperature
good temperature
bad temperature
favorable temperature
unfavorable temperature
excellent cooling
poor cooling
strong solar resource
weak solar resource
high suitability
low suitability
good score
bad score

Only report the numerical values.

--------------------------------------------------

RULE 6 — NO CAUSAL CLAIMS

NEVER create cause-and-effect relationships.

Do NOT say:

because
therefore
which means
resulting in
leading to
causing
helps
improves
reduces
increases
supports

unless the exact relationship is explicitly present
in the authoritative data.

--------------------------------------------------

RULE 7 — COOLING SCORE

If Cooling Score is mentioned, write:

Cooling Score

or:

cooling efficiency score

Do NOT claim:

better cooling
excellent cooling
efficient cooling
lower cooling cost
cooling savings
improved cooling
optimal cooling

--------------------------------------------------

RULE 8 — THERMAL SCORE

If Thermal Score is mentioned, write:

Thermal Score

or:

technical infrastructure metric

Do NOT claim:

thermal stability
thermal performance
better infrastructure
superior infrastructure
excellent infrastructure

--------------------------------------------------

RULE 9 — SOLAR

Solar GHI and Solar DNI may ONLY be reported
as numerical observations.

Do NOT infer:

energy generation
renewable energy
energy savings
sustainability
lower costs
operational benefits

--------------------------------------------------

RULE 10 — NO QUALITATIVE SCORE LABELS

NEVER use any qualitative label for the suitability score.

Forbidden:

low
moderate
good
high
poor
excellent
optimal
ideal
strong
weak
favorable
unfavorable
superior
best

The score must only appear as:

{score_text}/100

--------------------------------------------------

RULE 11 — NO INDIVIDUAL METRIC COMPARISON

Do NOT say any metric is:

best
highest
lowest
strongest
weakest
superior
inferior
better
worse
optimal
excellent

unless that exact comparison is explicitly provided
as authoritative data.

--------------------------------------------------

RULE 12 — FORBIDDEN CLAIMS

NEVER mention or imply:

cost savings
energy savings
energy efficiency
operational efficiency
financial benefit
business benefit
sustainability
reliability
resilience
safety
risk
danger
engineering superiority
infrastructure superiority
cooling cost
performance improvement
environmental benefit

--------------------------------------------------

RULE 13 — NO EXTRA FACTS

Do NOT invent:

weather conditions
annual climate patterns
infrastructure availability
power availability
water availability
land availability
taxes
electricity prices
construction costs
operating costs
energy consumption
PUE
renewable energy potential
data center capacity
network quality
business conditions
regulatory conditions
geographic advantages

None of these facts were supplied.

--------------------------------------------------

RULE 14 — NO MARKDOWN

Output must contain:

NO headings
NO bullets
NO numbering
NO bold
NO italic
NO Markdown
NO quotation marks
NO labels

--------------------------------------------------

RULE 15 — EXACTLY ONE PARAGRAPH

Return exactly ONE paragraph.

Do not use line breaks.

Do not create sections.

Do not create lists.

--------------------------------------------------

RULE 16 — LENGTH

Write between 70 and 110 words.

Keep the writing concise and factual.

--------------------------------------------------

RULE 17 — REQUIRED CONTENT

The paragraph MUST contain:

1. Recommended location:
{location}

2. Exact score:
{score_text}/100

3. At least one numerical climate metric.

4. A statement that the recommendation is based
on the AIXLocate scoring system.

5. The authoritative ranking.

6. The FINAL SENTENCE must preserve the exact meaning
of this application-generated statement:

{ranking_statement}

--------------------------------------------------

FINAL VALIDATION BEFORE OUTPUT

Before returning the paragraph, silently check:

[ ] Is the location exactly "{location}"?
[ ] Is the score exactly "{score_text}/100"?
[ ] Is the rank exactly "#{ranking}"?
[ ] Is every number copied from supplied data?
[ ] Did I avoid interpreting the score?
[ ] Did I avoid interpreting temperature?
[ ] Did I avoid interpreting solar metrics?
[ ] Did I avoid engineering claims?
[ ] Did I avoid cost/energy claims?
[ ] Did I avoid safety/risk claims?
[ ] Did I avoid causal language?
[ ] Did I avoid words such as excellent, optimal,
    ideal, superior, favorable, good, high, low?
[ ] Is the output exactly one paragraph?
[ ] Is the final sentence consistent with the
    authoritative ranking statement?

If ANY answer is NO, rewrite the paragraph before
returning it.

FINAL OUTPUT:

Return ONLY the final factual paragraph.
"""

    # ==================================================
    # CALL AI
    # ==================================================

    report_text = ask_llm(prompt)

    # ==================================================
    # CLEAN OUTPUT
    # ==================================================

    report_text = report_text.strip()

    # Remove Markdown emphasis
    report_text = report_text.replace("**", "")
    report_text = report_text.replace("__", "")

    # Remove Markdown headings
    report_text = report_text.replace("#", "")

    # Remove accidental bullets
    lines = []

    for line in report_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("- "):
            line = line[2:].strip()

        if line.startswith("• "):
            line = line[2:].strip()

        lines.append(line)

    # Force one paragraph
    report_text = " ".join(lines)

    # ==================================================
    # OUTPUT VALIDATION
    # ==================================================

    forbidden_phrases = [
        "excellent",
        "optimal",
        "ideal",
        "perfect",
        "superior",
        "favorable",
        "unfavorable",
        "best climate",
        "good climate",
        "bad climate",
        "high score",
        "low score",
        "good score",
        "poor score",
        "strong climate",
        "weak climate",
        "energy saving",
        "energy savings",
        "cost reduction",
        "lower cost",
        "cooling cost",
        "cooling savings",
        "energy efficiency",
        "sustainable",
        "sustainability",
        "thermal stability",
        "thermal performance",
        "infrastructure superiority",
        "engineering superiority",
        "operational benefit",
        "financial benefit",
        "business benefit",
        "reliable",
        "reliability",
        "resilience",
        "safe",
        "unsafe",
        "danger",
        "dangerous",
        "risk",
    ]

    report_lower = report_text.lower()

    # --------------------------------------------------
    # Check required authoritative values
    # --------------------------------------------------

    if location not in report_text:
        raise ValueError(
            "AI report validation failed: recommended location is missing."
        )

    if f"{score_text}/100" not in report_text:
        raise ValueError(
            "AI report validation failed: authoritative score is missing."
        )

    if ranking == 1:
        ranking_ok = (
            f"#{ranking}" in report_text
            or f"ranked first" in report_lower
            or "ranked 1" in report_lower
            or "rank 1" in report_lower
            or "ranking 1" in report_lower
            or report_text.startswith("1 ")
        )
    else:
        ranking_ok = (
            f"#{ranking}" in report_text
            or f"ranked {ranking}" in report_lower
            or f"rank {ranking}" in report_lower
            or f"ranking {ranking}" in report_lower
        )

    if not ranking_ok:
        raise ValueError(
            "AI report validation failed: authoritative ranking is missing."
        )

    # --------------------------------------------------
    # Check forbidden claims
    # --------------------------------------------------

    detected_forbidden = [
        phrase
        for phrase in forbidden_phrases
        if phrase in report_lower
    ]

    if detected_forbidden:
        raise ValueError(
            "AI report validation failed. "
            f"Forbidden language detected: {detected_forbidden}"
        )

    # --------------------------------------------------
    # Final paragraph normalization
    # --------------------------------------------------

    report_text = " ".join(
        report_text.split()
    )

    # ==================================================
    # AUTHORITATIVE SCORE PROTECTION
    # ==================================================

    return {
        "report": report_text,
        "report_score": score,
    }