import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Pharmacovigilance AI Safety Signal System",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# CONSTANTS
# ==========================================================

REPORT_FILE = os.path.join(
    "reports",
    "acute_kidney_injury_report.json"
)


# ==========================================================
# LOAD JSON REPORT
# ==========================================================

@st.cache_data
def load_report():

    if not os.path.exists(REPORT_FILE):

        st.error(
            f"Report file not found: {REPORT_FILE}"
        )

        st.stop()

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


report = load_report()


# ==========================================================
# EXTRACT DATA
# ==========================================================

signal = report["signal"]

overview = report["overview"]

seriousness = report["seriousness"]

patient_profile = report["patient_profile"]

signal_evidence = report["signal_evidence"]

signal_scoring = report["signal_scoring"]

signal_associated_drugs = report.get(
    "signal_associated_drugs",
    {}
)

assessment = report.get(
    "assessment",
    ""
)

limitations = report.get(
    "limitations",
    []
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("💊 PV AI System")

    st.markdown(
        """
        ### Navigation

        - 📊 Overview
        - 🚨 Signal Evidence
        - 💊 Medicinal Products
        - 👤 Patient Profile
        - 🌍 Geography
        - 📈 Signal Scoring
        - 🤖 AI Assessment
        - ⚠️ Limitations
        """
    )

    st.divider()

    st.markdown(
        "**Current Signal**"
    )

    st.info(signal)

    st.divider()

    st.caption(
        "AI-assisted pharmacovigilance "
        "signal prioritization system"
    )


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "💊 Pharmacovigilance AI Safety Signal System"
)

st.markdown(
    "### AI-assisted safety signal analysis "
    "for pharmacovigilance case data"
)

st.divider()


# ==========================================================
# SAFETY SIGNAL
# ==========================================================

st.header("🔎 Safety Signal")

st.success(
    f"**{signal}**"
)


# ==========================================================
# KEY PERFORMANCE INDICATORS
# ==========================================================

st.subheader("Key Signal Metrics")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Rows",
        overview["total_rows"]
    )


with col2:

    st.metric(
        "Unique Cases",
        overview["unique_cases"]
    )


with col3:

    st.metric(
        "Signal Cases",
        overview["reported_cases_for_signal"]
    )


with col4:

    st.metric(
        "Signal Rank",
        overview["signal_rank"]
    )


with col5:

    st.metric(
        "Signal Score",
        f"{signal_scoring['total_score']}/100"
    )


# ==========================================================
# PRIORITY
# ==========================================================

priority = signal_scoring["priority"]


if priority == "HIGH":

    st.error(
        f"🚨 Signal Priority: **{priority}**"
    )

elif priority == "MEDIUM":

    st.warning(
        f"⚠️ Signal Priority: **{priority}**"
    )

else:

    st.success(
        f"✅ Signal Priority: **{priority}**"
    )


st.divider()


# ==========================================================
# SERIOUSNESS
# ==========================================================

st.header("🚨 Seriousness")


serious_col1, serious_col2, serious_col3 = st.columns(3)


with serious_col1:

    st.metric(
        "Serious Cases",
        seriousness["serious_cases"]
    )


with serious_col2:

    st.metric(
        "Serious Case Percentage",
        f"{seriousness['serious_case_percentage']}%"
    )


with serious_col3:

    st.metric(
        "Signal Evidence Cases",
        signal_evidence["evidence_case_count"]
    )


st.divider()


# ==========================================================
# SIGNAL-ASSOCIATED MEDICINAL PRODUCTS
# ==========================================================

st.header(
    "💊 Signal-Associated Medicinal Products"
)

st.caption(
    f"Medicinal products reported in cases "
    f"associated with **{signal}**."
)


drug_df = pd.DataFrame(
    list(
        signal_associated_drugs.items()
    ),
    columns=[
        "Medicinal Product",
        "Signal-Associated Cases"
    ]
)


# ----------------------------------------------------------
# Sort
# ----------------------------------------------------------

drug_df = drug_df.sort_values(
    "Signal-Associated Cases",
    ascending=True
)


# ----------------------------------------------------------
# Drug Chart
# ----------------------------------------------------------

fig_drugs = px.bar(
    drug_df,
    x="Signal-Associated Cases",
    y="Medicinal Product",
    orientation="h",
    text="Signal-Associated Cases",
    title="Medicinal Products Reported in Signal-Associated Cases"
)


fig_drugs.update_traces(
    textposition="outside"
)


fig_drugs.update_layout(
    height=650,
    xaxis_title="Number of Signal-Associated Cases",
    yaxis_title="Medicinal Product",
    margin=dict(
        l=20,
        r=40,
        t=70,
        b=40
    )
)


st.plotly_chart(
    fig_drugs,
    width="stretch"
)


# ----------------------------------------------------------
# Drug Table
# ----------------------------------------------------------

with st.expander(
    "📋 View Medicinal Product Data"
):

    display_drug_df = drug_df.sort_values(
        "Signal-Associated Cases",
        ascending=False
    )

    st.dataframe(
        display_drug_df,
        width="stretch",
        hide_index=True
    )


st.divider()


# ==========================================================
# PATIENT PROFILE
# ==========================================================

st.header("👤 Patient Profile")


profile_col1, profile_col2 = st.columns(2)


# ==========================================================
# AGE GROUPS
# ==========================================================

with profile_col1:

    st.subheader("Age Groups")


    age_df = pd.DataFrame(
        list(
            patient_profile[
                "age_groups"
            ].items()
        ),
        columns=[
            "Age Group",
            "Cases"
        ]
    )


    age_df = age_df.sort_values(
        "Cases",
        ascending=True
    )


    fig_age = px.bar(
        age_df,
        x="Cases",
        y="Age Group",
        orientation="h",
        text="Cases",
        title="Patient Age Distribution"
    )


    fig_age.update_traces(
        textposition="outside"
    )


    fig_age.update_layout(
        height=400,
        xaxis_title="Cases",
        yaxis_title="Age Group",
        margin=dict(
            l=20,
            r=40,
            t=70,
            b=40
        )
    )


    st.plotly_chart(
        fig_age,
        width="stretch"
    )


# ==========================================================
# SEX DISTRIBUTION
# ==========================================================

with profile_col2:

    st.subheader("Sex Distribution")


    sex_df = pd.DataFrame(
        list(
            patient_profile[
                "sex"
            ].items()
        ),
        columns=[
            "Sex",
            "Cases"
        ]
    )


    sex_df = sex_df.sort_values(
        "Cases",
        ascending=True
    )


    fig_sex = px.bar(
        sex_df,
        x="Cases",
        y="Sex",
        orientation="h",
        text="Cases",
        title="Patient Sex Distribution"
    )


    fig_sex.update_traces(
        textposition="outside"
    )


    fig_sex.update_layout(
        height=400,
        xaxis_title="Cases",
        yaxis_title="Sex",
        margin=dict(
            l=20,
            r=40,
            t=70,
            b=40
        )
    )


    st.plotly_chart(
        fig_sex,
        width="stretch"
    )


st.divider()


# ==========================================================
# SIGNAL-SPECIFIC OUTCOMES
# ==========================================================

st.header(
    "📈 Signal-Specific Outcomes"
)


outcome_df = pd.DataFrame(
    list(
        signal_evidence[
            "outcomes"
        ].items()
    ),
    columns=[
        "Outcome",
        "Cases"
    ]
)


outcome_df = outcome_df.sort_values(
    "Cases",
    ascending=True
)


fig_outcomes = px.bar(
    outcome_df,
    x="Cases",
    y="Outcome",
    orientation="h",
    text="Cases",
    title=f"Outcomes for {signal} Cases"
)


fig_outcomes.update_traces(
    textposition="outside"
)


fig_outcomes.update_layout(
    height=450,
    xaxis_title="Number of Cases",
    yaxis_title="Outcome",
    margin=dict(
        l=20,
        r=40,
        t=70,
        b=40
    )
)


st.plotly_chart(
    fig_outcomes,
    width="stretch"
)


with st.expander(
    "📋 View Outcome Data"
):

    st.dataframe(
        outcome_df.sort_values(
            "Cases",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )


st.divider()


# ==========================================================
# SIGNAL-SPECIFIC GEOGRAPHIC DISTRIBUTION
# ==========================================================

st.header(
    "🌍 Signal-Specific Geographic Distribution"
)


country_df = pd.DataFrame(
    list(
        signal_evidence[
            "countries"
        ].items()
    ),
    columns=[
        "Country",
        "Cases"
    ]
)


country_df = country_df.sort_values(
    "Cases",
    ascending=True
)


fig_country = px.bar(
    country_df,
    x="Cases",
    y="Country",
    orientation="h",
    text="Cases",
    title=f"Geographic Distribution of {signal} Cases"
)


fig_country.update_traces(
    textposition="outside"
)


fig_country.update_layout(
    height=500,
    xaxis_title="Signal Cases",
    yaxis_title="Country",
    margin=dict(
        l=20,
        r=40,
        t=70,
        b=40
    )
)


st.plotly_chart(
    fig_country,
    width="stretch"
)


with st.expander(
    "📋 View Geographic Data"
):

    st.dataframe(
        country_df.sort_values(
            "Cases",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )


st.divider()


# ==========================================================
# SIGNAL SCORING
# ==========================================================

st.header("📊 Signal Scoring")


score_col1, score_col2, score_col3, score_col4 = st.columns(4)


with score_col1:

    st.metric(
        "Total Score",
        f"{signal_scoring['total_score']}/100"
    )


with score_col2:

    st.metric(
        "Priority",
        signal_scoring["priority"]
    )


with score_col3:

    st.metric(
        "Reporting Percentage",
        f"{signal_scoring['reporting_percentage']}%"
    )


with score_col4:

    fatal_percentage = signal_scoring.get(
        "fatal_percentage",
        "N/A"
    )

    st.metric(
        "Fatal Percentage",
        f"{fatal_percentage}%"
    )


# ==========================================================
# SCORE COMPONENTS
# ==========================================================

st.subheader("Score Components")


score_components = signal_scoring.get(
    "component_scores",
    {}
)


if score_components:

    score_df = pd.DataFrame(
        list(
            score_components.items()
        ),
        columns=[
            "Component",
            "Score"
        ]
    )


    score_df = score_df.sort_values(
        "Score",
        ascending=True
    )


    fig_score = px.bar(
        score_df,
        x="Score",
        y="Component",
        orientation="h",
        text="Score",
        title="Signal Score Component Breakdown"
    )


    fig_score.update_traces(
        textposition="outside"
    )


    fig_score.update_layout(
        height=400,
        xaxis_title="Score",
        yaxis_title="Component",
        margin=dict(
            l=20,
            r=40,
            t=70,
            b=40
        )
    )


    st.plotly_chart(
        fig_score,
        width="stretch"
    )


st.divider()


# ==========================================================
# AI ASSESSMENT
# ==========================================================

st.header("🤖 AI-Assisted Signal Assessment")


if assessment:

    st.info(
        assessment
    )

else:

    st.warning(
        "AI assessment is not available in the generated report."
    )


st.divider()


# ==========================================================
# LIMITATIONS
# ==========================================================

st.header("⚠️ Limitations")


if limitations:

    for limitation in limitations:

        st.markdown(
            f"- {limitation}"
        )

else:

    st.info(
        "No limitations were provided in the report."
    )


st.divider()


# ==========================================================
# IMPORTANT INTERPRETATION
# ==========================================================

st.header(
    "ℹ️ Interpretation"
)


st.warning(
    "This dashboard presents reporting patterns "
    "for pharmacovigilance signal prioritization. "
    "The signal score is a project-specific "
    "prioritization measure and does not establish "
    "a causal relationship between a medicinal product "
    "and the reported adverse reaction."
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()


st.caption(
    "Pharmacovigilance AI Safety Signal System | "
    "AI-assisted reporting-pattern analysis"
)