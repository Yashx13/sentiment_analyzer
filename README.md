
# Product Sentiment Analyzer

A Streamlit-based dashboard that analyzes product reviews using sentiment analysis, providing visual breakdowns of customer opinions and ratings.

---

## 📦 Installation Steps

### 1. Clone the repository
```bash
    git clone https://github.com/Yashx13/sentiment_analyzer.git
    cd sentiment_analyzer
```

### 2. Create a virtual environment
```bash
    python -m venv .psenv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```bash
    .psenv/Scripts/Activate.ps1
```

**Windows (Command Prompt):**
```bash
    .psenv/Scripts/activate.bat
```

**Linux/macOS:**
```bash
source .psenv/bin/activate
```

+ **Install all Dependencies**
```bash
    pip install -r requirements.txt
```

+ **Run the Project**
<br> In ordinary folder (non-env) you would need to do ```python -m streamlit run app.py``` but here the virtual environment keeps it consistent
```bash
    streamlit run main/app.py
```
This will open the application in your browser at `https://localhost:8501`

## 📁 Project Structure
```
sentiment_analyzer/
├── main/
│   ├── app.py          # application
│   ├── analyzer.py     # analysis logic
│   └── csv/            # Files for data
│       ├── products.csv
│       └── product_reviews.csv
├── requirements.txt    # dependencies 
└── README.md

```
