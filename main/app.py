import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

import analyzer as az


st.set_page_config(layout="wide", page_title="Sentiment Analyzer")


# Load data
products, reviews = az.load_data()
analyzer = az.get_analyzer()


st.title("🧠 Product Sentiment Analyzer")
st.markdown("""
Analyze customer sentiment for different products based on real reviews.
Select a product below to begin.
""")


product_list = ["Select a product..."] + products["title"].tolist()
product_choice = st.selectbox("Choose a product", product_list, index=0)

if product_choice == "Select a product...":
    st.info("👆 Please select a product from the dropdown above to view sentiment analysis.")
    st.stop()


product_row = products[products["title"] == product_choice].iloc[0]
pid = product_row["product_id"]


prod_reviews = reviews[reviews["product_id"] == pid].copy()

if len(prod_reviews) == 0:
    st.warning("No reviews found for this product.")
    st.stop()


if "rating" not in prod_reviews.columns:
    st.warning("⚠️ Ratings column not found in CSV. Please add a 'rating' column with values 1-5.")
    st.stop()


with st.spinner("Analyzing reviews..."):
    prod_reviews["scores"] = prod_reviews["review_text"].apply(analyzer.polarity_scores)
    prod_reviews["compound"] = prod_reviews["scores"].apply(lambda x: x["compound"])
    
    # Create sentiment label
    prod_reviews["label"] = prod_reviews["compound"].apply(
        lambda c: "Positive" if c >= 0.05 else ("Negative" if c <= -0.05 else "Neutral")
    )


counts = prod_reviews["label"].value_counts().reindex(["Positive", "Neutral", "Negative"]).fillna(0).astype(int)
total_reviews = len(prod_reviews)
percentages = (counts / total_reviews * 100).round(1)
avg_score = prod_reviews["compound"].mean()
avg_rating = prod_reviews["rating"].mean()


if avg_score >= 0.4:
    sentiment_summary = "### 🟢 **Overall Sentiment: Very Positive** — Most users loved this product."
    sentiment_color = "green"
elif avg_score >= 0.1:
    sentiment_summary = "### 🟡 **Overall Sentiment: Generally Positive / Mixed** — Users found it good overall with a few issues."
    sentiment_color = "orange"
elif avg_score > -0.05:
    sentiment_summary = "### ⚪ **Overall Sentiment: Neutral / Mixed** — Balanced opinions."
    sentiment_color = "gray"
else:
    sentiment_summary = "### 🔴 **Overall Sentiment: Negative / Bad Reviews** — Many users were dissatisfied."
    sentiment_color = "red"


st.subheader("Product Information")
col_info1, col_info2 = st.columns([2, 1])
with col_info1:
    st.write(f"**Product:** {product_row['title']}")
    st.write(f"**Price:** ${product_row['price']:.2f}")
with col_info2:
    st.metric("Average Rating", f"{'⭐' * int(round(avg_rating))}", f"{avg_rating:.2f}/5.0")

st.divider()


st.subheader("📊 Sentiment Summary")

col1, col2 = st.columns([1, 1])

with col1:
    st.metric("Total Reviews", f"{total_reviews}")
    st.metric("Avg Sentiment Score", f"{avg_score:.3f}")
    st.markdown("**Breakdown:**")
    st.write(f"🟢 Positive: {counts['Positive']} ({percentages['Positive']}%)")
    st.write(f"⚪ Neutral: {counts['Neutral']} ({percentages['Neutral']}%)")
    st.write(f"🔴 Negative: {counts['Negative']} ({percentages['Negative']}%)")

with col2:

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(counts.index, counts.values, color=["#4CAF50", "#9E9E9E", "#F44336"], width=0.6)
    ax.set_title("Sentiment Distribution", fontsize=12, fontweight='bold')
    ax.set_ylabel("Review Count", fontsize=10)
    ax.set_xlabel("Sentiment", fontsize=10)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=9)
    ax.grid(axis='y', alpha=0.3)
    

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)

st.divider()

st.markdown(sentiment_summary)

st.divider()

st.subheader("💬 Sample Reviews")

sample_size = min(8, len(prod_reviews))
sample_reviews = prod_reviews.sample(sample_size)


sample_reviews["stars"] = sample_reviews["rating"].apply(lambda x: "⭐" * int(x))


display_df = sample_reviews[["review_id", "review_text", "stars", "label", "compound"]].reset_index(drop=True)
display_df.columns = ["Review ID", "Review Text", "Rating", "Sentiment", "Score"]


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Review Text": st.column_config.TextColumn(width="large"),
        "Score": st.column_config.NumberColumn(format="%.3f"),
    }
)