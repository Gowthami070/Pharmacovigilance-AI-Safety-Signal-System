import pandas as pd
def analyze_case_counts(df):
    """
    Calculate row count and unique safety report count.
    """

    total_rows = len(df)
    unique_cases = df["safetyreportid"].nunique()

    return {
        "total_rows": total_rows,
        "unique_cases": unique_cases,
    }
def analyze_seriousness(df):
    """
    Calculate serious and non-serious case counts.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    serious_counts = (
        case_df["serious"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .value_counts()
        .to_dict()
    )

    return serious_counts
def analyze_age_groups(df):
    """
    Normalize patient age to years and classify cases into age groups.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    age = case_df["patient_patientonsetage"]
    unit = case_df["patient_patientonsetageunit"].astype(str).str.strip().str.lower()

    age_years = age.copy()

    age_years = age.where(unit == "year")
    age_years = age_years.fillna(
        age.where(unit == "month") / 12
    )
    age_years = age_years.fillna(
        age.where(unit == "week") / 52.1429
    )
    age_years = age_years.fillna(
        age.where(unit == "day") / 365.25
    )

    def classify_age(value):
        if pd.isna(value):
            return "Unknown"
        elif value < 18:
            return "Pediatric"
        elif value < 65:
            return "Adult"
        else:
            return "Older Adult"

    case_df["age_group"] = age_years.apply(classify_age)

    return case_df["age_group"].value_counts().to_dict()
def analyze_sex(df):
    """
    Calculate case counts by patient sex.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    sex_counts = (
        case_df["patient_patientsex"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
        .to_dict()
    )

    return sex_counts
def analyze_country(df):
    """
    Calculate case counts by occurrence country.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    country_counts = (
        case_df["occurcountry"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
        .to_dict()
    )

    return country_counts
def analyze_reactions(df, top_n=20):
    """
    Calculate the most frequently reported adverse reactions.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    reaction_counts = {}

    for value in case_df["patient_reaction_reactionmeddrapt"].dropna():
        reactions = str(value).split(",")

        for reaction in reactions:
            reaction = reaction.strip()

            if reaction:
                reaction_counts[reaction] = (
                    reaction_counts.get(reaction, 0) + 1
                )

    sorted_reactions = sorted(
        reaction_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return dict(sorted_reactions[:top_n])
def analyze_serious_reactions(df, top_n=20):
    """
    Calculate the most frequently reported reactions among serious cases.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    serious_df = case_df[
        case_df["serious"]
        .astype(str)
        .str.strip()
        .str.lower()
        == "serious"
    ]

    reaction_counts = {}

    for value in serious_df[
        "patient_reaction_reactionmeddrapt"
    ].dropna():

        reactions = str(value).split(",")

        for reaction in reactions:
            reaction = reaction.strip()

            if reaction:
                reaction_counts[reaction] = (
                    reaction_counts.get(reaction, 0) + 1
                )

    sorted_reactions = sorted(
        reaction_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return dict(sorted_reactions[:top_n])
def analyze_outcomes(df, top_n=None):
    """
    Calculate counts of reported patient reaction outcomes.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    outcome_counts = {}

    for value in case_df["patient_reaction_reactionoutcome"].dropna():
        outcomes = str(value).split(",")

        for outcome in outcomes:
            outcome = outcome.strip()

            if outcome:
                outcome_counts[outcome] = (
                    outcome_counts.get(outcome, 0) + 1
                )

    sorted_outcomes = sorted(
        outcome_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    if top_n is not None:
        sorted_outcomes = sorted_outcomes[:top_n]

    return dict(sorted_outcomes)
def analyze_drugs(df, top_n=20):
    """
    Calculate the most frequently reported medicinal products.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    drug_counts = {}

    for value in case_df["patient_drug_medicinalproduct"].dropna():

        drugs = set(
            drug.strip()
            for drug in str(value).split(",")
            if drug.strip()
        )

        for drug in drugs:
            drug_counts[drug] = (
                drug_counts.get(drug, 0) + 1
            )

    sorted_drugs = sorted(
        drug_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return dict(sorted_drugs[:top_n])
def analyze_indications(df, top_n=20):
    """
    Calculate the most frequently reported drug indications.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    indication_counts = {}

    for value in case_df["patient_drug_drugindication"].dropna():

        indications = set(
            indication.strip()
            for indication in str(value).split(",")
            if indication.strip()
        )

        for indication in indications:
            indication_counts[indication] = (
                indication_counts.get(indication, 0) + 1
            )

    sorted_indications = sorted(
        indication_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return dict(sorted_indications[:top_n])
def analyze_time_trend(df):
    """
    Calculate monthly case reporting trends.
    """

    case_df = df.drop_duplicates(subset=["safetyreportid"]).copy()

    case_df["report_date"] = pd.to_datetime(
        case_df["report_date"],
        errors="coerce"
    )

    case_df = case_df.dropna(subset=["report_date"])

    monthly_counts = (
        case_df
        .set_index("report_date")
        .resample("ME")
        .size()
    )

    trend = {
        date.strftime("%Y-%m"): int(count)
        for date, count in monthly_counts.items()
    }

    return trend