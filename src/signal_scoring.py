def calculate_signal_score(
    reported_cases,
    signal_rank,
    total_cases,
    evidence_cases,
    serious_cases,
    fatal_cases,
):
    """
    Calculate a transparent safety signal score.

    The score is based on:
    1. Reporting frequency
    2. Signal ranking
    3. Evidence availability
    4. Seriousness
    5. Fatal outcomes

    This score is a prioritization aid.
    It does NOT establish causality.
    """

    # --------------------------------------------------
    # 1. Reporting frequency score
    # --------------------------------------------------

    if total_cases > 0:
        reporting_percentage = (
            reported_cases / total_cases
        ) * 100
    else:
        reporting_percentage = 0

    if reporting_percentage >= 10:
        frequency_score = 30
    elif reporting_percentage >= 5:
        frequency_score = 25
    elif reporting_percentage >= 2:
        frequency_score = 20
    elif reporting_percentage >= 1:
        frequency_score = 15
    elif reporting_percentage > 0:
        frequency_score = 10
    else:
        frequency_score = 0

    # --------------------------------------------------
    # 2. Signal rank score
    # --------------------------------------------------

    if isinstance(signal_rank, int):

        if signal_rank == 1:
            rank_score = 20
        elif signal_rank <= 3:
            rank_score = 15
        elif signal_rank <= 5:
            rank_score = 10
        elif signal_rank <= 10:
            rank_score = 5
        else:
            rank_score = 2

    else:
        rank_score = 0

    # --------------------------------------------------
    # 3. Evidence score
    # --------------------------------------------------

    if evidence_cases >= 50:
        evidence_score = 20
    elif evidence_cases >= 20:
        evidence_score = 15
    elif evidence_cases >= 10:
        evidence_score = 10
    elif evidence_cases > 0:
        evidence_score = 5
    else:
        evidence_score = 0

    # --------------------------------------------------
    # 4. Seriousness score
    # --------------------------------------------------

    if reported_cases > 0:

        serious_percentage = (
            serious_cases / reported_cases
        ) * 100

    else:
        serious_percentage = 0

    if serious_percentage >= 90:
        seriousness_score = 15
    elif serious_percentage >= 75:
        seriousness_score = 12
    elif serious_percentage >= 50:
        seriousness_score = 8
    elif serious_percentage > 0:
        seriousness_score = 4
    else:
        seriousness_score = 0

    # --------------------------------------------------
    # 5. Fatal outcome score
    # --------------------------------------------------

    if reported_cases > 0:

        fatal_percentage = (
            fatal_cases / reported_cases
        ) * 100

    else:
        fatal_percentage = 0

    if fatal_percentage >= 10:
        fatal_score = 15
    elif fatal_percentage >= 5:
        fatal_score = 10
    elif fatal_percentage > 0:
        fatal_score = 5
    else:
        fatal_score = 0

    # --------------------------------------------------
    # Total score
    # --------------------------------------------------

    total_score = (
        frequency_score
        + rank_score
        + evidence_score
        + seriousness_score
        + fatal_score
    )

    # Maximum possible score:
    # 30 + 20 + 20 + 15 + 15 = 100

    total_score = min(total_score, 100)

    # --------------------------------------------------
    # Priority classification
    # --------------------------------------------------

    if total_score >= 75:
        priority = "HIGH"

    elif total_score >= 50:
        priority = "MEDIUM"

    else:
        priority = "LOW"

    return {
        "total_score": total_score,
        "priority": priority,

        "reporting_percentage": round(
            reporting_percentage,
            2
        ),

        "serious_percentage": round(
            serious_percentage,
            2
        ),

        "fatal_percentage": round(
            fatal_percentage,
            2
        ),

        "component_scores": {
            "frequency_score": frequency_score,
            "rank_score": rank_score,
            "evidence_score": evidence_score,
            "seriousness_score": seriousness_score,
            "fatal_score": fatal_score,
        },

        "interpretation": (
            "The signal score is a prioritization measure "
            "based on observed reporting patterns. "
            "It should not be interpreted as evidence of "
            "a causal relationship between the medicinal "
            "product and the reported reaction."
        ),
    }