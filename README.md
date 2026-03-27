# 📝 Marathi NLP Analysis

<p align="center">
  <strong>मराठी भाषा विश्लेषण साधन</strong><br/>
  An interactive web application for deep linguistic analysis of Marathi text — sentiment, emotion, POS tagging, NER, TF-IDF, topic modeling, and more.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" alt="Python 3.11"/>
  <img src="https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"/>
  <img src="https://img.shields.io/badge/Language-Marathi%20%7C%20Devanagari-orange" alt="Marathi"/>
  <img src="https://img.shields.io/badge/Accuracy-90%25-brightgreen" alt="90% Accuracy"/>
</p>

---

## 🌟 Overview

**Marathi NLP Analysis** is a full-stack NLP tool built specifically for the **Marathi language** (मराठी), written in the Devanagari script. It provides a rich, interactive Streamlit web interface powered by a custom lexicon-based NLP engine trained on a corpus of **12,000+ Marathi documents**.

The tool requires **no external NLP APIs** — everything runs locally using hand-crafted lexicons, heuristic rules, and pre-trained scikit-learn models, making it fast, private, and fully offline-capable.

### ✨ Highlights

| Feature | Detail |
|---|---|
| 🔤 Devanagari-aware tokenization | Regex-based, handles Unicode Marathi script correctly |
| 💬 Sentiment Analysis | Position-weighted scoring with negation & intensifier handling |
| 😊 Emotion Detection | 10+ emotions including complex ones like grief, shame, nostalgia |
| 🏷️ POS Tagging | Heuristic suffix/pattern-based tagging |
| 🗺️ Named Entity Recognition | Lexicon-matched entity candidates (1,000+ entries) |
| 📊 TF-IDF Analysis | Pre-trained vectorizer rebuilt from vocabulary JSON |
| 🧠 Topic Modeling | LDA model trained on 12,000+ document corpus |
| 🔍 Semantic Analysis | Formality, politeness, tense, text complexity |
| 🎓 Dual UI Mode | User Mode (clean) & Learner Mode (hacker/futuristic theme) |
| 💯 Overall Accuracy | 90% (100% sentiment, 80% emotion) |

---

## 🚀 Live Demo

Deploy your own instance for free on **Streamlit Cloud**:

```
https://<your-username>-marathi-nlp-analysis.streamlit.app
```

See [QUICKSTART.md](QUICKSTART.md) for a 3-step deployment guide, or [DEPLOY.md](DEPLOY.md) for full platform-specific instructions (Streamlit Cloud, Heroku, AWS EC2, Docker).

---

## 🗂️ Project Structure

```
marathi-nlp-analysis/
│
├── app.py                    # Streamlit web application (UI + visualizations)
├── marathi_nlp_core.py       # Core NLP engine (tokenization, analysis functions)
├── semantic_analysis.py      # Semantic feature module (formality, tense, etc.)
├── NLPFINALSEM.ipynb         # Jupyter notebook — corpus processing & model training
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── Procfile                  # Heroku process file
├── setup.sh                  # Shell setup for Heroku/server deployments
├── runtime.txt               # Python runtime version pin
│
├── lda_model.joblib          # Trained LDA topic model
├── tfidf_vectorizer.joblib   # Fitted TF-IDF vectorizer (optional fallback)
├── count_vocab.json          # CountVectorizer vocabulary (JSON)
├── tfidf_vocab.json          # TF-IDF vocabulary (JSON)
│
├── sentiment_lexicon.csv     # Positive/negative word lexicon (215+ entries)
├── emotion_lexicon.csv       # Emotion word lexicon (300+ entries, 10+ emotions)
├── marathi_stopwords.csv     # Marathi stopwords (1,000+ entries)
├── marathi_entities.csv      # Named entity candidates (1,000+ entries)
├── marathi_pos_tokens.csv    # POS-tagged token reference
├── marathi_phrases.csv       # Frequent phrase patterns
├── marathi_ngrams.csv        # Bigrams and trigrams
├── marathi_symbols.csv       # Language symbols and punctuation
│
├── df_clean.csv              # Cleaned training corpus (12,000+ documents)
├── tfidf_top_terms.csv       # Top TF-IDF terms extracted from corpus
├── pos_df.csv                # POS analysis results
├── entities_df.csv           # Extracted entities reference
│
├── test_accuracy.py          # Accuracy test suite (sentiment + emotion)
├── ACCURACY_IMPROVEMENTS.md  # Detailed accuracy changelog
├── DEPLOY.md                 # Full deployment guide
└── QUICKSTART.md             # Quick 3-step deploy guide
```

---

## ⚙️ Installation & Local Setup

### Prerequisites

- Python **3.9+** (3.11 recommended)
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/7009soham/marathi-nlp-analysis.git
cd marathi-nlp-analysis
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

> **Note:** If the `.joblib` model files are missing, run all cells in `NLPFINALSEM.ipynb` to regenerate them. The app will still function without them (TF-IDF and LDA sections will be skipped).

### Docker (Alternative)

```bash
# Using Docker Compose (recommended)
docker-compose up

# Or build and run manually
docker build -t marathi-nlp-analysis .
docker run -p 8501:8501 marathi-nlp-analysis
```

---

## 🖥️ Using the Web App

1. **Enter Text** — Type or paste any Marathi text (Devanagari script) in the input box.
2. **Load an Example** — Use the dropdown (105 categorized example sentences) to quickly try a sample.
3. **Click Analyze** — Press the **🔍 Analyze** button.
4. **Explore Results** — Scroll through eight analysis panels:

| Panel | What You See |
|---|---|
| **Tokenization** | Token list, count, Marathi-only vs. mixed mode |
| **Sentiment** | Score, positive/negative word counts, gauge chart |
| **Emotion** | Dominant emotion, per-emotion word counts, bar chart |
| **POS Tagging** | Tagged token table, part-of-speech distribution pie chart |
| **Named Entities** | Extracted entity candidates from the text |
| **TF-IDF** | Most important terms (bar chart) |
| **Topic Modeling** | LDA topic distribution, top words per topic |
| **Semantic Analysis** | Formality, politeness, tense, complexity indicators |

### 🎓 Learner Mode

Click **🔄 Switch to Learner Mode** in the top-right corner to activate a futuristic dark/hacker theme with code-style explanations — great for presentations and demos.

---

## 🧠 How It Works

### NLP Pipeline

```
Input Text (Marathi / Devanagari)
        │
        ▼
┌────────────────────┐
│   Tokenizer        │  Devanagari regex, Marathi-only or mixed mode
└────────┬───────────┘
         │
         ├──▶ Sentiment Analysis   ──▶ Position-weighted score + negation/intensifier handling
         ├──▶ Emotion Detection    ──▶ Lexicon matching + complex emotion priority rules
         ├──▶ POS Tagging          ──▶ Heuristic suffix/pattern rules
         ├──▶ Named Entity Recog.  ──▶ Token lookup against entity lexicon
         ├──▶ TF-IDF               ──▶ Pre-trained vocab vectorizer → top terms
         ├──▶ Topic Modeling       ──▶ CountVectorizer → LDA → topic distribution
         └──▶ Semantic Analysis    ──▶ Formality, politeness, tense, complexity
```

### Sentiment Analysis (100% accuracy)

- **Position-weighted scoring**: tokens later in a sentence contribute up to 1.3× more weight.
- **Proximity-aware negation**: detects negation words (`नाही`, `नको`, `नसते` …) within 3 tokens of a sentiment word and flips the score.
- **Preference expressions**: correctly handles constructs like `नाही आवडत` ("don't like").
- **Intensifiers** (`खूप`, `फार`) amplify scores by 1.6×; **diminishers** (`थोडे`, `जरा`) reduce them to 0.6×.

### Emotion Detection (80% accuracy)

- Checks **complex emotions first** (grief, shame, gratitude, nostalgia) before falling back to basic emotions.
- **Contextual grief detection**: past tense + relationship word + loss word → boosted grief score.
- **Confidence scoring** based on emotion word density.
- Maps fine-grained emotions to base categories for display.

### Supported Emotions

`joy` · `anger` · `sadness` · `fear` · `surprise` · `disgust` · `trust` · `anticipation` · `love` · `pride` · `grief` · `shame` · `gratitude` · `nostalgia` · `hope` · `contempt`

---

## 🐍 Python API

You can use the core NLP engine as a standalone Python module:

```python
from marathi_nlp_core import tokenize, analyze_sentiment, analyze_emotion

# Tokenize
tokens = tokenize("आज खूप छान दिवस आहे. मला खूप आनंद झाला.")
# → ['आज', 'खूप', 'छान', 'दिवस', 'आहे', 'मला', 'खूप', 'आनंद', 'झाला']

# Sentiment Analysis
result = analyze_sentiment("मला नाही आवडत. खूप वाईट आहे.")
print(result['label'])    # → "negative"
print(result['score'])    # → -2.45 (weighted)

# Emotion Detection
result = analyze_emotion("तो माझा जिवलग मित्र होता. त्याच्या जाण्याने खूप वाईट वाटते.")
print(result['dominant'])    # → "grief"
print(result['confidence'])  # → high (contextual boosting active)

# Full pipeline
from marathi_nlp_core import analyze_text
full = analyze_text("मी खूप खुश आहे! आज सर्वात आनंदी दिवस आहे.")
# Returns: tokens, sentiment, emotion, pos_tags, entities, tfidf_terms, lda_topics, semantic
```

---

## 📊 Accuracy

| Task | Score | Benchmark |
|---|---|---|
| Sentiment Analysis | **100%** (10/10) | +10% vs. baseline |
| Emotion Detection | **80%** (8/10) | +20% vs. baseline |
| **Overall** | **90%** | +15% vs. baseline |

See [ACCURACY_IMPROVEMENTS.md](ACCURACY_IMPROVEMENTS.md) for a detailed breakdown of every test case, algorithm changes, and lexicon expansions.

---

## 📁 Data & Lexicons

All lexicons and data files are generated by running `NLPFINALSEM.ipynb`:

| File | Contents | Size |
|---|---|---|
| `sentiment_lexicon.csv` | Positive/negative words | 215+ entries |
| `emotion_lexicon.csv` | Emotion-tagged words | 300+ entries |
| `marathi_stopwords.csv` | Common function words | 1,000+ entries |
| `marathi_entities.csv` | Named entity candidates | 1,000+ entries |
| `marathi_phrases.csv` | Frequent phrase patterns | — |
| `marathi_ngrams.csv` | Bigrams and trigrams | — |
| `df_clean.csv` | Cleaned training corpus | 12,000+ documents |
| `lda_model.joblib` | Trained LDA model | ~50 MB |
| `count_vocab.json` | CountVectorizer vocabulary | ~200 KB |
| `tfidf_vocab.json` | TF-IDF vocabulary | ~300 KB |

---

## 🚢 Deployment

| Platform | Guide | Cost |
|---|---|---|
| **Streamlit Cloud** ⭐ | [QUICKSTART.md](QUICKSTART.md) | Free |
| Heroku | [DEPLOY.md](DEPLOY.md#heroku) | ~$7/month |
| AWS EC2 | [DEPLOY.md](DEPLOY.md#aws) | ~$30/month |
| Docker | [DEPLOY.md](DEPLOY.md#docker) | Self-hosted |

**Recommended**: Start with Streamlit Cloud free tier — zero configuration, auto-deploys on every `git push`.

---

## 🔧 Development

### Adding New Features

1. **New Lexicons** — Add a CSV file and register a loader in `marathi_nlp_core.py`.
2. **New Analysis Function** — Add to `marathi_nlp_core.py` and wire it into `app.py`.
3. **New Visualizations** — Use Plotly Express or Plotly Graph Objects in `app.py`.

### Running Tests

```bash
python test_accuracy.py
```

Expected output:

```
Sentiment Accuracy: 100% (10/10)
Emotion Accuracy:    80% (8/10)
Overall Accuracy:    90%
```

### Performance Tips

| Metric | Value |
|---|---|
| Cold start | 15–20 seconds (model loading) |
| Warm analysis | < 1 second per request |
| Memory usage | ~200–300 MB |
| Concurrent users | 10–20 (Streamlit Cloud free tier) |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `Warning: Could not load lda_model.joblib` | Run the export cell in `NLPFINALSEM.ipynb` |
| `Can't pickle <function <lambda>>` | App auto-falls back to `tfidf_vocab.json`; no action needed |
| `Warning: Could not load sentiment_lexicon.csv` | Run all cells in `NLPFINALSEM.ipynb` |
| Devanagari not rendering | Install *Noto Sans Devanagari* font; update browser Unicode settings |
| Slow first load | Expected — models load once and are cached via `@st.cache_resource` |

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/my-improvement`
3. Make your changes and run `python test_accuracy.py` to validate.
4. Submit a pull request with a clear description.

**Ideas for contributions:**

- Expand lexicons (disgust, anger categories)
- Implement sarcasm detection
- Add compound emotion detection (joy + surprise)
- Train an ML classifier for edge cases
- Add export functionality (download results as CSV/JSON)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **Dataset**: Marathi text corpus (12,000+ documents)
- **NLP Libraries**: [scikit-learn](https://scikit-learn.org), [regex](https://pypi.org/project/regex/), [pandas](https://pandas.pydata.org), [numpy](https://numpy.org)
- **Visualization**: [Plotly](https://plotly.com), [Streamlit](https://streamlit.io)
- **Language**: Marathi (मराठी) — spoken by 83 million+ people, primarily in Maharashtra, India

---

<p align="center">Built with ❤️ for the Marathi language and NLP community</p>
