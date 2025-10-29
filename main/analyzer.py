from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import streamlit as st
import pandas as pd

@st.cache_resource
def get_analyzer():
    return SentimentIntensityAnalyzer()

@st.cache_data
def load_data():
    try:
        products = pd.read_csv("products_updated.csv")
        reviews = pd.read_csv("reviews.csv")
        return products, reviews
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.stop()