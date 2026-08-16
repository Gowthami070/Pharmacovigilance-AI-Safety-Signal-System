def get_reaction_evidence(df, reaction):
    """
    Retrieve individual cases that reported a specific reaction.

    The outcome corresponding to the requested reaction is extracted
    using the same position in the reaction and outcome lists.
    """

    case_df = df.drop_duplicates(
        subset=["safetyreportid"]
    ).copy()

    matching_cases = []

    target_reaction = str(reaction).strip().lower()

    for _, row in case_df.iterrows():

        reaction_value = row[
            "patient_reaction_reactionmeddrapt"
        ]

        outcome_value = row[
            "patient_reaction_reactionoutcome"
        ]

        if reaction_value is None:
            continue

        reactions = [
            item.strip()
            for item in str(reaction_value).split(",")
        ]

        outcomes = [
            item.strip()
            for item in str(outcome_value).split(",")
        ]

        # Find the requested reaction
        for index, current_reaction in enumerate(reactions):

            if current_reaction.lower() == target_reaction:

                # Get outcome at the same position
                if index < len(outcomes):
                    reaction_outcome = outcomes[index]
                else:
                    reaction_outcome = "unknown"

                matching_cases.append({
                    "safetyreportid": row["safetyreportid"],
                    "reaction": reaction,
                    "serious": row["serious"],
                    "outcome": row[
                        "patient_reaction_reactionoutcome"
                    ],
                    "country": row["occurcountry"],
                    "sex": row["patient_patientsex"],
                    "report_date": row["report_date"],
                    "drug": row[
                        "patient_drug_medicinalproduct"
                    ]
                })

                break

    return matching_cases


def get_case_evidence(df, safetyreportid):
    """
    Retrieve evidence for a specific safety case.
    """

    case_df = df[
        df["safetyreportid"] == safetyreportid
    ].copy()

    if case_df.empty:
        return None

    row = case_df.iloc[0]

    return {
        "safetyreportid": row["safetyreportid"],
        "serious": row["serious"],
        "reaction": row[
            "patient_reaction_reactionmeddrapt"
        ],
        "outcome": row[
            "patient_reaction_reactionoutcome"
        ],
        "country": row["occurcountry"],
        "sex": row["patient_patientsex"],
        "report_date": row["report_date"],
        "drug": row[
            "patient_drug_medicinalproduct"
        ]
    }