# imports
import re
import os
import pandas as pd
import numpy as np
import nltk
import spacy

from nltk.sentiment import SentimentIntensityAnalyzer

# nltk and spacy setup
nltk.download('punkt', quiet=True)
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)

nlp = spacy.load("en_core_web_sm")
stop_words = set(nltk.corpus.stopwords.words('english'))

sia = SentimentIntensityAnalyzer() # sentiment analyzer

accessibility_terms = {
    "blind_lowvision": ["braille", "blind", "low vision", "sight impaired", "braille signs",
                     "tactile", "audio", "description", "large print", "low vision", "tactile paths",
                     "high contrast signage", "braille maps", "audible signals", "tactile cues", "text-to-speech",
                     "clutter", "clear floors"],
    "deaf_hoh": ["deaf", "hard of hearing", "sign language", "ASL", "interpreter", "written ordering"
                 "captioning", "assistive listening device", "hearing aid",
                 "asl interpreter", "captions", "low background noise"],
    "chronic_pain_fatigue": ["chronic", "pain", "fatigue", "tired", "overwhelmed", "exhausted", "burnout",
                           "resting areas", "benches", "fatigue", "low energy access", "minimal walking",
                           "short distances", "chronic pain friendly", "seating", "crowded", "to rest", "back support",
                           "lean on", "leaning on", ],
    "auditory_sensitivity": ["auditory", "sensitivity", "noise",  "quiet", "loud", "noisy", "peaceful", "music",
                 "noise-cancelling headphones", "quiet space", "low lighting", "noise control", "low sensory stimulation", "overstimulating"],
    "visual_sensitivity": ["visual sensitivity", "light sensitivity", "well-lit", "bright", "dim", "low", "soft", "natural",
                 "harsh", "ambient", "glare", "sunglasses","flashing lights", "low sensory stimulation", "overstimulating"],
    "mobility": ["wheelchair", "ramp", "step-free", "elevator", "stairs", "handicap", "entrance", "ADA compliant",
                 "wide", "curb", "path", "route", "walker", "walking frame", "elevator", "roll-in", "grab bars", "lowered",
                 "clear floors", "clean floors", "steep", "gradual incline", "incline", ],
    "misc_sens": ["sensitivity", "fragrance", "scent", "smell"],
    "predict": ["predictable", "routine", "structured", "organized", "schedule", "plan", "reservation"],
    "adjust": ["adjustable", "modification", "flexible", "custom", "options", "accommodations"],
    "speech": ["speech", "communication", "interaction", "simple", "clear", "plain language", "text-to-speech",
               "speech-friendly", "voice recognition support", "difficulty speaking", "speech-to-text", "aac device friendly"],
    "bathroom": ["accessible bathroom", "restroom", "roll-in", "grab bars", "lowered",
                 "emergency alarm", "accessible restroom", "family restroom", "private bathroom",
                 "changing station", "bathroom", "gender neutral bathroom", "menstrual", "menstruation"],
    "cogn_dis": ["agency respected", "attended checkout""cognitive disability", "intellectual disability", "dementia", "alzheimers", "down syndrome", "simple instructions", "memory aids", "clear signage", "cognitive overload", "dementia-friendly", "easy navigation"],
    "read": ["readable", "easy to read", "signage", "contrast", "font size", "clear print", "large print", "line spacing", "easy-read materials", "text-to-speech", "readable fonts"],
    "anxiety": ["anxiety", "stress", "overwhelmed", "panic attack", "anxious", "overwhelming", "calming space", "calming", "relaxing", "stressful", "panic", "socially accessible", "comfortable"],
    "crowded": ["crowded", "busy", "overcrowded", "crowd", "chaotic"],
    "health_safe": ["health", "safety", "secure", "hygiene", "sanitize", "sanitizer", "disinfect", "PPE", "vaccination",
                    "clean", "wellness", "allergy", "asthma", "gloves", "hepa", "precaution", "airflow", "contactless",
                     "allergen", "ingredients", "cautious", "health-conscious"],
    "transportation": ["transportation", "accessible", "transport", "parking", "valet", "close", "bus", "taxi",
                       "shuttle", "public", "ride-hailing"],
    "service_animals": ["service animal", "service dog", "pet relief area"]
} # used to assess the presence of accessibility-related content in each review.
#adjust as needed

# precompile regexes
compiled_keywords = {
    category: re.compile('|'.join(map(re.escape, keywords)), flags=re.IGNORECASE)
    for category, keywords in accessibility_terms.items()
}

# analysis functions
def analyze_accessibility_and_sentiment(df):
    df = df.copy()
    df['review_text'] = df['review_text'].fillna('').astype(str)
    df['sentiment_score'] = df['review_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df['sentiment'] = df['sentiment_score'].apply(
        lambda x: 'positive' if x > 0.05 else 'negative' if x < -0.05 else 'neutral'
    )

    for category, pattern in compiled_keywords.items():
        df[f'{category}_matches'] = df['review_text'].apply(lambda x: pattern.findall(x))
        df[f'{category}_count'] = df[f'{category}_matches'].apply(len)
        df[f'{category}_score'] = df['sentiment_score'] * df[f'{category}_count']
        df[f'{category}_keywords'] = df[f'{category}_matches'].apply(lambda x: ', '.join(set(x)))

    score_cols = [f'{cat}_score' for cat in accessibility_terms]
    df['accessibility_score'] = df[score_cols].sum(axis=1)
    return df

#aggregates review accessibility information for each business
def summarize_per_business(df):
    df['review_count'] = 1

    agg_funcs = {
        'review_count': 'sum',
        'sentiment_score': 'mean',
        'sentiment': lambda x: x.mode().iloc[0] if not x.mode().empty else 'neutral',
        'title': 'first' if 'title' in df.columns else (lambda x: ''),
        'category': 'first' if 'category' in df.columns else (lambda x: ''),
        'accessibility_score': 'sum'
    }

    for cat in accessibility_terms:
        agg_funcs[f'{cat}_score'] = 'sum'
        agg_funcs[f'{cat}_keywords'] = lambda x: '; '.join(
            sorted(set(k.strip() for klist in x for k in klist.split(',') if klist))
        )

    summary = df.groupby('business_id').agg(agg_funcs).reset_index()

    # Rename raw scores
    summary.rename(columns={
        'accessibility_score': 'accessibility_score_raw',
        **{f'{cat}_score': f'{cat}_score_raw' for cat in accessibility_terms}
    }, inplace=True)

    # Adjusted scores
    summary['accessibility_score_adj'] = summary['accessibility_score_raw'] / summary['review_count']
    for cat in accessibility_terms:
        summary[f'{cat}_score_adj'] = summary[f'{cat}_score_raw'] / summary['review_count']

    return summary


# processes data in chunks to preserve RAM
def process_in_chunks(file_path, output_path, chunk_size=10000): #adjust chunk size as needed
    first_chunk = not os.path.exists(output_path)

    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size, low_memory=False)):
        print(f"\nProcessing chunk {i+1}...")

        if 'review_text' not in chunk.columns or 'business_id' not in chunk.columns:
            print("Missing required columns. Skipping chunk.")
            continue

        chunk = analyze_accessibility_and_sentiment(chunk)
        business_summary = summarize_per_business(chunk)

        business_summary.to_csv(output_path, mode='a', index=False, header=first_chunk)
        first_chunk = False
        print(f"Saved {len(business_summary)} rows to {output_path}")


# main function
if __name__ == "__main__":
    input_file = "merged.csv"  # large dataset with reviews
    output_file = "scores.csv"  # final one-row-per-business output
    process_in_chunks(input_file, output_file)
