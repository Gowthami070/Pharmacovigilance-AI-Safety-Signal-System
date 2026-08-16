import pandas as pd
from collections import defaultdict

from src.signal_scoring import calculate_signal_score


def build_ai_context(
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
    evidence=None
):
    """
    Build a structured context for AI-based safety signal generation.
    """

    context = {
        "case_counts": case_counts,
        "seriousness": seriousness,
        "age_groups": age_groups,
        "sex": sex,
        "countries": countries,
        "top_reactions": top_reactions,
        "top_serious_reactions": top_serious_reactions,
        "outcomes": outcomes,
        "top_drugs": top_drugs,
        "top_indications": top_indications,
        "time_trend": time_trend,
    }

    if evidence is not None:
        context["evidence"] = evidence
    else:
        context["evidence"] = []

    return context


def generate_safety_signal(context, signal):
    """
    Generate a structured pharmacovigilance safety signal report.

    The function combines:
    - Overall dataset statistics
    - Seriousness
    - Patient demographics
    - Geographic distribution
    - Signal-specific evidence
    - Signal-associated medicinal products
    - Outcomes
    - Reported medicinal products
    - Drug indications
    - Time trend
    - Signal prioritization score

    Important:
    This analysis describes reporting patterns only.
    It does NOT establish causality.
    """

    # ==========================================================
    # 1. Extract context
    # ==========================================================

    case_counts = context["case_counts"]
    seriousness = context["seriousness"]
    age_groups = context["age_groups"]
    sex = context["sex"]
    countries = context["countries"]
    top_reactions = context["top_reactions"]
    top_serious_reactions = context["top_serious_reactions"]
    outcomes = context["outcomes"]
    top_drugs = context["top_drugs"]
    top_indications = context["top_indications"]
    time_trend = context["time_trend"]

    evidence = context.get("evidence", [])
    # ==========================================================
    # Signal-associated medicinal products
    # ==========================================================

    signal_drug_cases = defaultdict(set)

    for case in evidence:

        case_id = case.get("safetyreportid")

        drug_value = case.get("drug", "")

        if not drug_value:
            continue

        drug_list = str(drug_value).split(",")

        for drug in drug_list:

            drug = drug.strip()

            if not drug:
                continue

            # Count each drug only once per safety case
            signal_drug_cases[drug].add(case_id)

    signal_associated_drugs = {

        drug: len(case_ids)

        for drug, case_ids in signal_drug_cases.items()

    }

    # Sort by number of unique signal cases
    signal_associated_drugs = dict(
        sorted(
            signal_associated_drugs.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    # ==========================================================
    # 2. Basic case information
    # ==========================================================

    total_rows = case_counts.get(
        "total_rows",
        0
    )

    unique_cases = case_counts.get(
        "unique_cases",
        0
    )

    # ==========================================================
    # 3. Number of cases reporting selected signal
    # ==========================================================

    reported_cases = 0

    for reaction, count in top_reactions.items():

        if (
            str(reaction).strip().lower()
            == signal.strip().lower()
        ):

            reported_cases = count
            break

    # ==========================================================
    # 4. Determine signal rank
    # ==========================================================

    sorted_reactions = sorted(
        top_reactions.items(),
        key=lambda item: item[1],
        reverse=True
    )

    signal_rank = None

    for index, (reaction, count) in enumerate(
        sorted_reactions,
        start=1
    ):

        if (
            str(reaction).strip().lower()
            == signal.strip().lower()
        ):

            signal_rank = index
            break

    if signal_rank is None:
        signal_rank = "Not in top reactions"

    # ==========================================================
    # 5. Overall seriousness calculation
    # ==========================================================

    serious_cases = 0

    for key, value in seriousness.items():

        if (
            str(key).strip().lower()
            == "serious"
        ):

            serious_cases = value
            break

    if unique_cases:

        serious_percentage = round(
            (serious_cases / unique_cases) * 100,
            1
        )

    else:

        serious_percentage = 0

    # ==========================================================
    # 6. Signal-specific evidence analysis
    # ==========================================================

    evidence_countries = {}
    evidence_sex = {}
    evidence_outcomes = {}

    for case in evidence:

        # ------------------------------------------------------
        # Country
        # ------------------------------------------------------

        country = case.get(
            "country",
            "Unknown"
        )

        if country is None:
            country = "Unknown"

        country = str(country).strip()

        if not country:
            country = "Unknown"

        # ------------------------------------------------------
        # Sex
        # ------------------------------------------------------

        sex_value = case.get(
            "sex",
            "Unknown"
        )

        if sex_value is None or pd.isna(sex_value):
            sex_value = "Unknown"

        sex_value = str(sex_value).strip()

        if (
            not sex_value
            or sex_value.lower() == "nan"
        ):

            sex_value = "Unknown"

        # ------------------------------------------------------
        # Outcome
        # ------------------------------------------------------

        outcome = case.get(
            "outcome",
            "Unknown"
        )

        if outcome is None:
            outcome = "Unknown"

        outcome = str(outcome).strip()

        # ======================================================
        # Count country
        # ======================================================

        evidence_countries[country] = (
            evidence_countries.get(country, 0) + 1
        )

        # ======================================================
        # Count sex
        # ======================================================

        evidence_sex[sex_value] = (
            evidence_sex.get(sex_value, 0) + 1
        )

        # ======================================================
        # Normalize outcome
        #
        # A single case may contain multiple outcome values.
        # We convert them into ONE case-level outcome.
        #
        # Priority:
        # fatal
        # not recovered
        # recovering
        # recovered with sequelae
        # recovered
        # unknown
        # ======================================================

        outcome_values = [
            value.strip().lower()
            for value in outcome.split(",")
            if value.strip()
        ]

        if not outcome_values:

            case_outcome = "Unknown"

        elif "fatal" in outcome_values:

            case_outcome = "fatal"

        elif (
            "not recovered/not resolved/ongoing"
            in outcome_values
        ):

            case_outcome = (
                "not recovered/not resolved/ongoing"
            )

        elif "recovering/resolving" in outcome_values:

            case_outcome = "recovering/resolving"

        elif (
            "recovered/resolved with sequelae"
            in outcome_values
        ):

            case_outcome = (
                "recovered/resolved with sequelae"
            )

        elif "recovered/resolved" in outcome_values:

            case_outcome = "recovered/resolved"

        elif "unknown" in outcome_values:

            case_outcome = "unknown"

        else:

            case_outcome = "Unknown"

        # ======================================================
        # Count normalized outcome
        # ======================================================

        evidence_outcomes[case_outcome] = (
            evidence_outcomes.get(case_outcome, 0) + 1
        )

    # ==========================================================
    # 7. Signal-associated medicinal products
    #
    # Count UNIQUE CASES per drug.
    #
    # Important:
    # If the same drug appears multiple times in one case,
    # that case is counted only once for that drug.
    # ==========================================================

    signal_drug_cases = defaultdict(set)

    for case in evidence:

        safetyreportid = case.get(
            "safetyreportid"
        )

        drug_value = case.get(
            "drug"
        )

        if drug_value is None:
            continue

        drug_value = str(drug_value).strip()

        if (
            not drug_value
            or drug_value.lower() == "nan"
        ):
            continue

        for drug in drug_value.split(","):

            drug = drug.strip()

            if not drug:
                continue

            signal_drug_cases[drug].add(
                safetyreportid
            )

    signal_associated_drugs = dict(
        sorted(
            (
                (
                    drug,
                    len(case_ids)
                )
                for drug, case_ids
                in signal_drug_cases.items()
            ),
            key=lambda item: item[1],
            reverse=True
        )[:20]
    )

    # ==========================================================
    # 8. Calculate signal-specific seriousness
    # ==========================================================

    signal_serious_cases = 0

    for case in evidence:

        serious_value = case.get(
            "serious",
            "Unknown"
        )

        if (
            str(serious_value).strip().lower()
            == "serious"
        ):

            signal_serious_cases += 1

    # ==========================================================
    # 9. Calculate fatal signal outcomes
    # ==========================================================

    signal_fatal_cases = evidence_outcomes.get(
        "fatal",
        0
    )

    # ==========================================================
    # 10. Calculate signal score
    # ==========================================================

    signal_score = calculate_signal_score(
        reported_cases=reported_cases,
        signal_rank=signal_rank,
        total_cases=unique_cases,
        evidence_cases=len(evidence),
        serious_cases=signal_serious_cases,
        fatal_cases=signal_fatal_cases
    )

    # ==========================================================
    # 11. Create final structured report
    # ==========================================================

    report = {

        # ------------------------------------------------------
        # Signal
        # ------------------------------------------------------

        "signal":
            signal,

        # ------------------------------------------------------
        # Overview
        # ------------------------------------------------------

        "overview": {

            "total_rows":
                total_rows,

            "unique_cases":
                unique_cases,

            "reported_cases_for_signal":
                reported_cases,

            "signal_rank":
                signal_rank,
        },

        # ------------------------------------------------------
        # Seriousness
        # ------------------------------------------------------

        "seriousness": {

            "serious_cases":
                serious_cases,

            "serious_case_percentage":
                serious_percentage,
        },

        # ------------------------------------------------------
        # Patient profile
        # ------------------------------------------------------

        "patient_profile": {

            "age_groups":
                age_groups,

            "sex":
                sex,
        },

        # ------------------------------------------------------
        # Geographic distribution
        # ------------------------------------------------------

        "geographic_distribution":
            countries,

        # ------------------------------------------------------
        # Signal-specific evidence
        # ------------------------------------------------------

        "signal_evidence": {

            "evidence_case_count":
                len(evidence),

            "countries":
                evidence_countries,

            "sex":
                evidence_sex,

            "outcomes":
                evidence_outcomes,
        },

        # ------------------------------------------------------
        # Signal-associated medicinal products
        # ------------------------------------------------------

        "signal_associated_drugs":
            signal_associated_drugs,
        # ------------------------------------------------------
        # Top reported drugs
        # ------------------------------------------------------

        "top_reported_drugs":
            top_drugs,

        # ------------------------------------------------------
        # Signal-associated medicinal products
        # ------------------------------------------------------

        "signal_associated_drugs":
            signal_associated_drugs,

        # ------------------------------------------------------
        # Top indications
        # ------------------------------------------------------

        "top_reported_indications":
            top_indications,

        # ------------------------------------------------------
        # Signal scoring
        # ------------------------------------------------------

        "signal_scoring":
            signal_score,

        # ------------------------------------------------------
        # Signal scoring
        # ------------------------------------------------------

        "signal_scoring":
            signal_score,

        # ------------------------------------------------------
        # Overall outcomes
        # ------------------------------------------------------

        "overall_outcomes":
            outcomes,

        # ------------------------------------------------------
        # Top reported drugs
        # ------------------------------------------------------

        "top_reported_drugs":
            top_drugs,

        # ------------------------------------------------------
        # Top indications
        # ------------------------------------------------------

        "top_reported_indications":
            top_indications,

        # ------------------------------------------------------
        # Time trend
        # ------------------------------------------------------

        "time_trend":
            time_trend,

        # ------------------------------------------------------
        # Assessment
        # ------------------------------------------------------

        "assessment": (

            f"{signal} was the most frequently reported adverse "
            f"reaction in the analyzed dataset, with "
            f"{reported_cases} reported case(s). "

            f"The signal-specific evidence contains "
            f"{len(evidence)} matching case(s), of which "
            f"{signal_serious_cases} were classified as serious. "

            f"The signal-specific evidence includes "
            f"{signal_fatal_cases} fatal outcome(s). "

            f"The signal ranked {signal_rank} among the reported "
            f"adverse reactions and received a prioritization score "
            f"of {signal_score['total_score']}/100, resulting in a "
            f"{signal_score['priority']} priority classification. "

            f"Among the signal-associated medicinal products, "
            f"the most frequently reported were "
            f"{', '.join(list(signal_associated_drugs.keys())[:3])}. "

            "These medicinal products were reported in cases "
            "associated with the signal; the observed co-reporting "
            "does not establish a causal relationship between any "
            "specific medicinal product and the reported reaction. "

            "The findings should therefore be interpreted as "
            "reporting-pattern evidence intended to support "
            "further pharmacovigilance investigation."
        ),

        # ------------------------------------------------------
        # Limitations
        # ------------------------------------------------------

        "limitations": [

            "The analysis is based on reported safety cases.",

            "The signal score is a project-specific "
            "prioritization measure and is not a validated "
            "causal inference method.",

            "Reporting frequency does not establish causality.",

            "Multiple drugs may be reported within the same case.",

            "Missing or incomplete patient information may "
            "affect subgroup analysis.",

            "The dataset may contain duplicate information "
            "across related records.",

        ],
    }

    return report