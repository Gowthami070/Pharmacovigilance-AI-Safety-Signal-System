REQUIRED_COLUMNS = [
    "safetyreportid",
    "serious",
    "patient_patientonsetage",
    "patient_patientsex",
    "occurcountry",
    "patient_reaction_reactionmeddrapt",
    "patient_reaction_reactionoutcome",
    "patient_drug_medicinalproduct",
    "patient_drug_activesubstance_activesubstancename",
    "report_date",
]


def validate_data(df):
    """
    Validate the basic structure of the safety dataset.
    """

    errors = []

    # Check whether the dataset is empty
    if df.empty:
        errors.append("Dataset is empty.")

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {missing_columns}"
        )

    # Return validation result
    if errors:
        return False, errors

    return True, []