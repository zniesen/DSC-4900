import streamlit as st
import pandas as pd
import numpy as np

# Text size 
text_size = st.sidebar.selectbox("Text Size", ["Small", "Medium", "Large"], index=1)
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

# TTS
st.markdown("""
    <button onclick="readText()">🔊 Read Recommendations</button>
    <script>
        function readText() {
            const synth = window.speechSynthesis;
            let text = "Top recommended locations based on your accessibility preferences.";
            synth.speak(new SpeechSynthesisUtterance(text));
        }
    </script>
""", unsafe_allow_html=True)


# list of accessibility categories (keys)
accessibility_categories = [
    "blind_lowvision", "deaf_hoh", "chronic_pain_fatigue", "auditory_sensitivity",
    "visual_sensitivity", "mobility", "misc_sens", "predict", "adjust", "speech",
    "bathroom", "cogn_dis", "read", "anxiety", "crowded", "health_safe",
    "transportation", "service_animals"
]

# mapping of category keys to full, human-readable names.
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

# load business summary scores
@st.cache_data
def load_scores(csv_file="scores.csv"):
    try:
        df = pd.read_csv(csv_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return pd.DataFrame()

# user select which accessibility needs and importance
st.sidebar.header("Select Your Accessibility Needs")
user_needs = {}
for cat in accessibility_categories:
    display_name = full_category_names.get(cat, cat)
    if st.sidebar.checkbox(display_name, value=False):
        weight = st.sidebar.slider(f"Importance for {display_name}", 1, 5, 3)
        user_needs[cat] = weight

st.sidebar.markdown("---")
st.sidebar.info("Adjust the importance weights to personalize your search.")

# load the business scores
df_scores = load_scores()

if df_scores.empty:
    st.write("No data available. Please check that scores.csv is in the correct location.")
    st.stop()

if not user_needs:
    st.header("All Locations Sorted by Overall Accessibility")
    df_scores = df_scores.sort_values("accessibility_score_adj", ascending=False)

    # display full names of all accessibility columns
    renamed_cols = {f"{k}_score_adj": v for k, v in full_category_names.items()}
    df_display = df_scores.rename(columns=renamed_cols)

    base_cols = ["title", "category", "review_count", "accessibility_score_adj"]
    extra_cols = [renamed_cols[f"{k}_score_adj"] for k in accessibility_categories if f"{k}_score_adj" in df_display.columns]
    st.dataframe(df_display[base_cols + extra_cols])
else:
    def compute_weighted_score(row):
        score = 0
        for cat, weight in user_needs.items():
            col_name = f"{cat}_score_adj"
            cat_score = row[col_name] if col_name in row.index else 0
            score += weight * cat_score
        review_factor = np.log(row['review_count'] + 1)
        return score * review_factor

    df_scores["weighted_score"] = df_scores.apply(compute_weighted_score, axis=1)
    df_sorted = df_scores.sort_values("weighted_score", ascending=False)

    st.header("Recommended Locations")
    st.markdown("Below are the best options according to your selected accessibility needs, importance ratings, and the number of reviews.")

    # include weighted score + selected accessibility columns
    base_cols = ["title", "category", "review_count", "weighted_score"]
    renamed_cols = {f"{k}_score_adj": v for k, v in full_category_names.items() if f"{k}_score_adj" in df_scores.columns}
    selected_cat_cols = [f"{k}_score_adj" for k in user_needs if f"{k}_score_adj" in df_scores.columns]
    selected_cat_cols_named = [renamed_cols[col] for col in selected_cat_cols]
    df_display = df_sorted.rename(columns=renamed_cols)

    st.dataframe(df_display[base_cols + selected_cat_cols_named].reset_index(drop=True))

    st.markdown("### Details Per Accessibility Need")
    st.markdown("The weighted score is calculated as a sum of the individual accessibility scores (averaged per review) multiplied by the importance you specify for each need. This score is then boosted by the logarithm of the number of reviews so that locations with more reviews are favored.")
