import json
def generate_report(report):
    """
    Convert the structured safety signal report
    into a human-readable text report.

    The report includes both:
    1. Overall dataset medicinal products
    2. Signal-associated medicinal products

    Signal-associated medicinal products are based on
    unique safety cases reporting the selected signal.
    """

    signal = report["signal"]

    overview = report["overview"]

    seriousness = report["seriousness"]

    patient_profile = report["patient_profile"]

    geographic = report["geographic_distribution"]

    evidence = report["signal_evidence"]

    outcomes = report["overall_outcomes"]

    drugs = report["top_reported_drugs"]

    # IMPORTANT:
    # These drugs are specifically associated with the
    # selected safety signal.
    signal_associated_drugs = report.get(
        "signal_associated_drugs",
        {}
    )

    time_trend = report["time_trend"]

    assessment = report["assessment"]

    limitations = report["limitations"]

    signal_scoring = report["signal_scoring"]

    lines = []

    # ==================================================
    # HEADER
    # ==================================================

    lines.append("=" * 70)
    lines.append(
        "PHARMACOVIGILANCE SAFETY SIGNAL REPORT"
    )
    lines.append("=" * 70)

    lines.append("")

    lines.append(
        f"Safety Signal: {signal}"
    )

    # ==================================================
    # 1. OVERVIEW
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("1. OVERVIEW")
    lines.append("-" * 70)

    lines.append(
        f"Total dataset rows        : "
        f"{overview['total_rows']}"
    )

    lines.append(
        f"Unique safety cases       : "
        f"{overview['unique_cases']}"
    )

    lines.append(
        f"Cases reporting signal    : "
        f"{overview['reported_cases_for_signal']}"
    )

    lines.append(
        f"Signal rank               : "
        f"{overview['signal_rank']}"
    )

    # ==================================================
    # 2. SERIOUSNESS
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("2. SERIOUSNESS")
    lines.append("-" * 70)

    lines.append(
        f"Serious cases             : "
        f"{seriousness['serious_cases']}"
    )

    lines.append(
        f"Serious case percentage   : "
        f"{seriousness['serious_case_percentage']}%"
    )

    # ==================================================
    # 3. PATIENT PROFILE
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("3. PATIENT PROFILE")
    lines.append("-" * 70)

    # ------------------------------
    # Age
    # ------------------------------

    lines.append("Age Groups:")

    for group, count in patient_profile[
        "age_groups"
    ].items():

        lines.append(
            f"  - {group}: {count}"
        )

    # ------------------------------
    # Sex
    # ------------------------------

    lines.append("")

    lines.append("Sex:")

    for sex, count in patient_profile[
        "sex"
    ].items():

        lines.append(
            f"  - {sex}: {count}"
        )

    # ==================================================
    # 4. GEOGRAPHIC DISTRIBUTION
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("4. GEOGRAPHIC DISTRIBUTION")
    lines.append("-" * 70)

    for country, count in geographic.items():

        lines.append(
            f"  - {country}: {count}"
        )

    # ==================================================
    # 5. SIGNAL-SPECIFIC EVIDENCE
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("5. SIGNAL-SPECIFIC EVIDENCE")
    lines.append("-" * 70)

    lines.append(
        f"Evidence cases            : "
        f"{evidence['evidence_case_count']}"
    )

    # ------------------------------
    # Countries
    # ------------------------------

    lines.append("")

    lines.append("Countries represented:")

    for country, count in evidence[
        "countries"
    ].items():

        lines.append(
            f"  - {country}: {count}"
        )

    # ------------------------------
    # Sex
    # ------------------------------

    lines.append("")

    lines.append("Sex distribution:")

    for sex, count in evidence[
        "sex"
    ].items():

        lines.append(
            f"  - {sex}: {count}"
        )

    # ------------------------------
    # Outcomes
    # ------------------------------

    lines.append("")

    lines.append("Signal outcomes:")

    for outcome, count in evidence[
        "outcomes"
    ].items():

        lines.append(
            f"  - {outcome}: {count}"
        )

    # ==================================================
    # 6. OVERALL REPORTED OUTCOMES
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("6. OVERALL REPORTED OUTCOMES")
    lines.append("-" * 70)

    for outcome, count in outcomes.items():

        lines.append(
            f"  - {outcome}: {count}"
        )

    # ==================================================
    # 7. TOP REPORTED MEDICINAL PRODUCTS
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append(
        "7. TOP REPORTED MEDICINAL PRODUCTS"
    )
    lines.append("-" * 70)

    for drug, count in drugs.items():

        lines.append(
            f"  - {drug}: {count}"
        )

    # ==================================================
    # 8. SIGNAL-ASSOCIATED MEDICINAL PRODUCTS
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append(
        "8. SIGNAL-ASSOCIATED MEDICINAL PRODUCTS"
    )
    lines.append("-" * 70)

    lines.append(
        "Medicinal products reported in cases "
        f"associated with the signal: {signal}"
    )

    lines.append("")

    if signal_associated_drugs:

        for drug, count in signal_associated_drugs.items():

            lines.append(
                f"  - {drug}: {count} case(s)"
            )

    else:

        lines.append(
            "  No signal-associated medicinal "
            "products available."
        )

    # ==================================================
    # 9. REPORTING TIME TREND
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("9. REPORTING TIME TREND")
    lines.append("-" * 70)

    for month, count in time_trend.items():

        lines.append(
            f"  - {month}: {count}"
        )

    # ==================================================
    # 10. SIGNAL SCORING
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("10. SIGNAL SCORING")
    lines.append("-" * 70)

    lines.append(
        f"Total Signal Score       : "
        f"{signal_scoring['total_score']}/100"
    )

    lines.append(
        f"Priority                 : "
        f"{signal_scoring['priority']}"
    )

    lines.append(
        f"Reporting Percentage     : "
        f"{signal_scoring['reporting_percentage']}%"
    )

    lines.append(
        f"Serious Percentage       : "
        f"{signal_scoring['serious_percentage']}%"
    )

    lines.append(
        f"Fatal Percentage         : "
        f"{signal_scoring['fatal_percentage']}%"
    )

    # ------------------------------
    # Component Scores
    # ------------------------------

    lines.append("")

    lines.append("Component Scores:")

    for component, score in signal_scoring[
        "component_scores"
    ].items():

        lines.append(
            f"  - {component}: {score}"
        )

    # ------------------------------
    # Interpretation
    # ------------------------------

    lines.append("")

    lines.append("Interpretation:")

    lines.append(
        f"  {signal_scoring['interpretation']}"
    )

    # ==================================================
    # 11. ASSESSMENT
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("11. ASSESSMENT")
    lines.append("-" * 70)

    lines.append(
        assessment
    )

    # ==================================================
    # 12. LIMITATIONS
    # ==================================================

    lines.append("")
    lines.append("-" * 70)
    lines.append("12. LIMITATIONS")
    lines.append("-" * 70)

    for limitation in limitations:

        lines.append(
            f"  - {limitation}"
        )

    # ==================================================
    # FOOTER
    # ==================================================

    lines.append("")

    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)

def save_json_report(report, file_path):
    """
    Save the structured safety signal report
    as a JSON file.
    """

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )