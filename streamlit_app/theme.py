import streamlit as st


def apply_theme():

    st.markdown(
        """
<style>

/* =========================================================
   TCRFlowX — WARM CANCER IMMUNOGENOMICS THEME
   Crimson • Coral • Orange • Cream
========================================================= */


/* MAIN BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at 8% 5%,
            rgba(255, 111, 97, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 92% 15%,
            rgba(255, 166, 77, 0.13),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #FFF9F4 0%,
            #FFF4EC 48%,
            #FFF8F2 100%
        );

    color: #3B2024;
}


/* MAIN CONTENT */

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1450px;
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #FFF1EA 0%,
            #FFE9DC 100%
        );

    border-right: 1px solid #F0D2C4;
}

[data-testid="stSidebar"] * {
    color: #5B3033;
}


/* TITLES */

h1 {
    color: #701F2B !important;
    font-weight: 850 !important;
}

h2,
h3 {
    color: #7B2935 !important;
    font-weight: 800 !important;
}


/* HERO */

.tcr-hero {

    padding: 40px 44px;

    border-radius: 28px;

    background:
        linear-gradient(
            120deg,
            #8E2430 0%,
            #D94C45 45%,
            #F28A3C 100%
        );

    box-shadow:
        0 18px 45px rgba(142, 36, 48, 0.20);

    margin-bottom: 28px;
}


.tcr-hero h1 {

    color: #FFFFFF !important;

    font-size: 3.15rem !important;

    margin:
        8px 0 10px 0;
}


.tcr-hero p {

    color:
        rgba(255,255,255,.94) !important;

    font-size: 1.08rem;

    margin-bottom: 0;
}


.hero-eyebrow {

    color: #FFE7D8 !important;

    font-size: .80rem;

    letter-spacing: .15em;

    font-weight: 850;
}


/* KPI CARDS */

.kpi-card {

    background:
        linear-gradient(
            145deg,
            #FFFFFF,
            #FFF7F1
        );

    border:
        1px solid #F0D7C9;

    border-top:
        4px solid #E65D4E;

    border-radius: 20px;

    padding: 22px;

    min-height: 145px;

    box-shadow:
        0 10px 25px
        rgba(112, 47, 40, .08);

    transition:
        transform .2s ease,
        box-shadow .2s ease;
}


.kpi-card:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 14px 34px
        rgba(112, 47, 40, .15);
}


.kpi-label {

    color: #9B5A54 !important;

    font-size: .77rem;

    font-weight: 850;

    letter-spacing: .09em;

    text-transform: uppercase;
}


.kpi-value {

    color: #8E2430 !important;

    font-size: 2.10rem;

    font-weight: 850;

    margin-top: 8px;
}


.kpi-note {

    color: #82625F !important;

    font-size: .84rem;

    margin-top: 6px;
}


/* SECTION HEADERS */

.section-banner {
    margin-top: 30px;
    margin-bottom: 18px;

    padding: 20px 24px;

    background:
        linear-gradient(
            90deg,
            #FFE4D6,
            #FFF1DD
        );

    border-radius: 16px;

    border-left: 6px solid #D94C45;

    box-shadow:
        0 6px 18px rgba(125, 54, 45, .07);
}


.section-banner h3 {
    margin: 0;
    color: #7B2935 !important;
    font-size: 2rem !important;
    line-height: 1.15 !important;
    font-weight: 850 !important;
    letter-spacing: -0.02em !important;
}


/* WHITE CONTENT CARDS */

.content-card {

    background:
        rgba(
            255,
            255,
            255,
            .94
        );

    border:
        1px solid #F0D8CB;

    border-radius: 20px;

    padding: 24px;

    box-shadow:
        0 8px 22px
        rgba(104, 49, 42, .06);
}


/* BIOLOGY FINDINGS */

.insight-card {

    background:
        linear-gradient(
            110deg,
            #FFF0E8,
            #FFF8E9
        );

    border:
        1px solid #F2D9C9;

    border-left:
        5px solid #F28A3C;

    padding: 18px 21px;

    margin-bottom: 13px;

    border-radius: 15px;

    box-shadow:
        0 5px 15px
        rgba(105, 48, 41, .05);
}


.insight-title {

    color: #8E2430 !important;

    font-weight: 800;
}


.muted {

    color: #806762 !important;

    font-size: .88rem;
}


/* STREAMLIT METRIC */

[data-testid="stMetric"] {

    background: #FFFFFF;

    border:
        1px solid #EFD6C9;

    border-top:
        4px solid #F28A3C;

    border-radius: 17px;

    padding: 16px 18px;

    box-shadow:
        0 7px 20px
        rgba(105,48,41,.06);
}


[data-testid="stMetricValue"] {

    color: #8E2430 !important;

    font-weight: 850;
}


/* DATAFRAME */

[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;

    border:
        1px solid #EDD6CA;
}


/* PLOTLY */

[data-testid="stPlotlyChart"] {

    background: #FFFFFF;

    border-radius: 20px;

    padding: 7px;

    border:
        1px solid #F0D9CE;

    box-shadow:
        0 7px 22px
        rgba(105,48,41,.06);
}


/* EXPANDER */

[data-testid="stExpander"] {

    background:
        rgba(255,255,255,.90);

    border:
        1px solid #EED7CB;

    border-radius: 15px;
}


/* BUTTON */

.stButton > button {

    background:
        linear-gradient(
            90deg,
            #B8343E,
            #F28A3C
        );

    color: white;

    border: none;

    border-radius: 12px;

    font-weight: 750;
}


/* INFO */

[data-testid="stAlert"] {

    border-radius: 14px;
}


/* REMOVE EXCESS TOP SPACE */

header[data-testid="stHeader"] {

    background:
        rgba(255,249,244,.92);
}


/* MOBILE */

@media (max-width:900px) {

    .tcr-hero {

        padding:
            28px 24px;
    }

    .tcr-hero h1 {

        font-size:
            2.4rem !important;
    }

}

</style>
        """,
        unsafe_allow_html=True
    )