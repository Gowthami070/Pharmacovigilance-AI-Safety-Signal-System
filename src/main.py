import os
from src.data_loader import load_data

from src.analysis import (
    analyze_case_counts,
    analyze_seriousness,
    analyze_age_groups,
    analyze_sex,
    analyze_country,
    analyze_reactions,
    analyze_serious_reactions,
    analyze_outcomes,
    analyze_drugs,
    analyze_indications,
    analyze_time_trend,
)

from src.evidence import get_reaction_evidence

from src.ai_generator import (
    build_ai_context,
    generate_safety_signal,
)

from src.report_generator import (
    generate_report,
    save_json_report
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = "data/Bisoprolol_icsr_sample_1068rows.xlsx"

SIGNAL = "Acute kidney injury"


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("=" * 60)
    print("PHARMACOVIGILANCE AI SAFETY SIGNAL SYSTEM")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. LOAD DATA
    # --------------------------------------------------------

    print("\nLoading dataset...")

    df = load_data(DATA_PATH)

    print("Dataset loaded successfully!")
    print(f"Total rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


    # --------------------------------------------------------
    # 2. ANALYSIS
    # --------------------------------------------------------

    print("\nAnalyzing case counts...")
    case_counts = analyze_case_counts(df)
    print("Case counts:")
    print(case_counts)


    print("\nAnalyzing seriousness...")
    seriousness = analyze_seriousness(df)
    print("Seriousness:")
    print(seriousness)


    print("\nAnalyzing age groups...")
    age_groups = analyze_age_groups(df)
    print("Age groups:")
    print(age_groups)


    print("\nAnalyzing sex distribution...")
    sex = analyze_sex(df)
    print("Sex:")
    print(sex)


    print("\nAnalyzing countries...")
    countries = analyze_country(df)
    print("Countries:")
    print(countries)


    print("\nAnalyzing adverse reactions...")
    top_reactions = analyze_reactions(df)
    print("Top reactions:")
    print(top_reactions)


    print("\nAnalyzing serious reactions...")
    top_serious_reactions = analyze_serious_reactions(df)
    print("Top serious reactions:")
    print(top_serious_reactions)


    print("\nAnalyzing outcomes...")
    outcomes = analyze_outcomes(df)
    print("Outcomes:")
    print(outcomes)


    print("\nAnalyzing medicinal products...")
    top_drugs = analyze_drugs(df)
    print("Top drugs:")
    print(top_drugs)


    print("\nAnalyzing drug indications...")
    top_indications = analyze_indications(df)
    print("Top indications:")
    print(top_indications)


    print("\nAnalyzing reporting time trend...")
    time_trend = analyze_time_trend(df)
    print("Time trend:")
    print(time_trend)


    # --------------------------------------------------------
    # 3. SIGNAL-SPECIFIC EVIDENCE
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("EXTRACTING SIGNAL-SPECIFIC EVIDENCE")
    print("=" * 60)

    print(f"\nSignal: {SIGNAL}")

    evidence = get_reaction_evidence(
        df,
        SIGNAL
    )

    print(f"Evidence cases found: {len(evidence)}")


    # --------------------------------------------------------
    # 4. BUILD AI CONTEXT
    # --------------------------------------------------------

    print("\nBuilding AI context...")

    context = build_ai_context(
        case_counts,
        seriousness,
        age_groups,
        sex,
        countries,
        top_reactions,
        top_serious_reactions,
        outcomes,
        top_drugs,
        top_indications,
        time_trend,
        evidence,
    )

    print("AI context created successfully!")


    # --------------------------------------------------------
    # 5. GENERATE SAFETY SIGNAL
    # --------------------------------------------------------

    print("\nGenerating safety signal...")

    report = generate_safety_signal(
        context,
        SIGNAL
    )

    print("Safety signal generated successfully!")


    # --------------------------------------------------------
    # 6. GENERATE FINAL REPORT TEXT
    # --------------------------------------------------------

    print("\nGenerating final report...")

    report_text = generate_report(
        report
    )

    print("Final report generated successfully!")


    # --------------------------------------------------------
    # 7. DISPLAY REPORT
    # --------------------------------------------------------

    reports_dir = "reports"

    os.makedirs(reports_dir, exist_ok=True)

    report_file = os.path.join(
        reports_dir,
        "acute_kidney_injury_report.txt"
    )

    with open(report_file, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"Report saved successfully: {report_file}")
    # --------------------------------------------------------
    # Save structured JSON report
    # --------------------------------------------------------

    json_report_file = os.path.join(
        reports_dir,
        "acute_kidney_injury_report.json"
    )

    save_json_report(
        report,
        json_report_file
    )

    print(
        f"JSON report saved successfully: "
        f"{json_report_file}"
    )

    # --------------------------------------------------------
    # 8. COMPLETION MESSAGE
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()