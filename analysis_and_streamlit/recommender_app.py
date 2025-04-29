#imports
import streamlit as st
import pandas as pd
import numpy as np


# text size setting
text_size = st.sidebar.selectbox("Text Size", ["Small", "Medium", "Large"], index=1)

# text size CSS
size_map = {
    "Small": "14px",
    "Medium": "18px",
    "Large": "22px"
}
st.markdown(f"""
    <style>
        html, body, [class*="css"] {{
            font-size: {size_map[text_size]} !important;
        }}
    </style>
""", unsafe_allow_html=True)


# high contrast toggle
high_contrast = st.sidebar.checkbox("High Contrast Mode")

if high_contrast:
    st.markdown("""
        <style>
        body, .stApp {{
            background-color: black !important;
            color: white !important;
        }}
        .stDataFrame, .css-1d391kg, .css-1n76uvr {{
            background-color: #000 !important;
            color: #fff !important;
        }}
        </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <button onclick="readText()">🔊 Read Recommendations</button>
    <script>
        function readText() {
            const synth = window.speechSynthesis;
            let text = "Top recommended locations based on your preferences.";
            synth.speak(new SpeechSynthesisUtterance(text));
        }
    </script>
""", unsafe_allow_html=True)

# list of accessibility categories
accessibility_categories = [
    "blind_lowvision", "deaf_hoh", "chronic_pain_fatigue", "auditory_sensitivity",
    "visual_sensitivity", "mobility", "misc_sens", "predict", "adjust", "speech",
    "bathroom", "cogn_dis", "read", "anxiety", "crowded", "health_safe",
    "transportation", "service_animals"
]

# mapping of category keys to readable names
full_category_names = {
    "blind_lowvision": "Blind & Low Vision",
    "deaf_hoh": "Deaf & Hard of Hearing",
    "chronic_pain_fatigue": "Chronic Pain & Fatigue",
    "auditory_sensitivity": "Auditory Sensitivity",
    "visual_sensitivity": "Visual Sensitivity",
    "mobility": "Mobility",
    "misc_sens": "Miscellaneous Sensitivities",
    "predict": "Predictability",
    "adjust": "Adjustable Options",
    "speech": "Speech/Communication",
    "bathroom": "Accessible Bathrooms",
    "cogn_dis": "Cognitive Accessibility",
    "read": "Readability",
    "anxiety": "Anxiety & Stress",
    "crowded": "Crowdedness",
    "health_safe": "Health & Safety",
    "transportation": "Transportation",
    "service_animals": "Service Animal Accommodations"
}

# load business summary scores computed from review analysis
# scores.csv should have columns including: business_id, title, category, review_count, accessibility_score_adj, and individual category weighted scores (eg, blind_lowvision_score_adj, etc)
@st.cache_data
def load_scores(csv_file="scores.csv"):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

# accessibility need selection
st.sidebar.header("Select Your Accessibility Needs")
user_needs = {}
for cat in accessibility_categories:
    # use readable name for display
    display_name = full_category_names.get(cat, cat)
    if st.sidebar.checkbox(display_name, value=False):
        weight = st.sidebar.slider(f"Importance for {display_name}", 1, 5, 3)
        user_needs[cat] = weight #allow users to input importance

st.sidebar.markdown("---")
st.sidebar.info("Adjust the importance weights to personalize your search.")

# load the business scores-- ensure that scores.csv is available
df_scores = load_scores()

if df_scores.empty:
    st.write("No data available. Please check that scores.csv is in the correct location.")
    st.stop()

# if no accessibility need is selected, show the raw accessibility_score_adj ranking
if not user_needs:
    st.header("All Locations Sorted by Overall Accessibility")
    df_scores = df_scores.sort_values("accessibility_score_adj", ascending=False)
    st.dataframe(df_scores[["business_id", "title", "category", "review_count", "accessibility_score_adj"]])
else:
    # compute a weighted score that incorporates both the per-category scores and the number of reviews
    # assume each selected category has an associated column in df_scores
    def compute_weighted_score(row):
        score = 0
        for cat, weight in user_needs.items():
            col_name = f"{cat}_score_adj"
            # if the column is missing, assign 0
            cat_score = row[col_name] if col_name in row.index else 0
            score += weight * cat_score
        # multiply by log(review_count + 1) to boost locations with more reviews
        review_factor = np.log(row['review_count'] + 1)
        return score * review_factor

    # compute weighted score for each business
    df_scores["weighted_score"] = df_scores.apply(compute_weighted_score, axis=1)

    # sort businesses by the weighted score (higher is better)
    df_sorted = df_scores.sort_values("weighted_score", ascending=False)

    st.header("Recommended Locations")
    st.markdown("Below are the best options according to your selected accessibility needs, importance ratings, and the number of reviews.")

    # display key columns
    display_cols = ["business_id", "title", "category", "review_count", "weighted_score"]
    st.dataframe(df_sorted[display_cols].reset_index(drop=True))

    st.markdown("### Details Per Accessibility Need")
    st.markdown("The weighted score is calculated as a sum of the individual accessibility scores (averaged per review) multiplied by the importance you specify for each need. This score is then boosted by the logarithm of the number of reviews so that locations with more reviews are favored.")

