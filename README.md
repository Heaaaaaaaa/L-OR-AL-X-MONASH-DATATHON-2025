# L'ORÉAL X MONASH-DATATHON-2025

AI-powered comment analysis system for beauty brand social media insights.

## Project Structure
```markdown

    LOREALXMONASH-DATATHON-2025/
    ├── README.md                    # Project documentation
    ├── Submission.zip               # Complete project files
        ├── CommentSense.ipynb       # Main data processing pipeline
        └── Translate.ipynb          # Translation and relevance analysis
    ├── dashboard.py                 # Streamlit dashboard application
    └── requirement.txt              # Requirement libraries for Streamlit
```

## 🚀 Quick Start for Dashboard

1. **Run CommentSense to get "your_processed_data(En).csv":**

2. **Run dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## ✨ Features

- **Sentiment Analysis**: VADER-based sentiment scoring
- **Category Classification**: ML-powered categorization (skincare, makeup, fragrance, hair)
- **Spam Detection**: Advanced filtering for promotional content
- **Relevance Scoring**: Context-aware similarity matching
- **Interactive Dashboard**: Real-time analytics with filters
- **Multi-language Support**: Translation and English detection

## 📊 Key Metrics

- Quality Comment Ratio: 99.4%
- Spam Detection Rate: 0.57 %%
- Category Distribution: Makeup (46.1%), Skincare (32.2%), Hair (20.6%), Fragrance (1.07%)

## 🛠️ Technical Stack

- **Python 3.9+**
- **Streamlit** - Web dashboard
- **Pandas** - Data processing
- **Scikit-learn** - Machine learning
- **NLTK** - Natural language processing
- **Plotly** - Interactive visualizations

## 📝 Usage

1. **CommentSense.ipynb**: Run the complete data processing pipeline
2. **Translate.ipynb**: Handle multi-language translation and relevance
3. **dashboard.py**: Launch the interactive analytics dashboard

---

**Team**: HAHA | **Competition**: L'Oréal X Monash Datathon 2024
