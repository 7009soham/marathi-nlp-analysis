"""
Marathi NLP Analysis - Streamlit App
Interactive web UI for analyzing Marathi text using lexicon-based NLP.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from marathi_nlp_core import analyze_text, tokenize

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Marathi NLP Analysis",
    page_icon="📝",
    layout="wide"
)

# ============================================================================
# SESSION STATE FOR MODE
# ============================================================================
if 'learner_mode' not in st.session_state:
    st.session_state.learner_mode = False

# ============================================================================
# MODE TOGGLE
# ============================================================================
col_title, col_toggle = st.columns([4, 1])

with col_title:
    if st.session_state.learner_mode:
        st.markdown('<h1 style="color:#00ff41;font-family:monospace;">⚡ MARATHI NLP ANALYSIS SYSTEM ⚡</h1>', unsafe_allow_html=True)
    else:
        st.title("📝 Marathi NLP Analysis Tool")

with col_toggle:
    mode_label = "🎓 LEARNER MODE" if st.session_state.learner_mode else "👤 USER MODE"
    if st.button(f"🔄 Switch to {'User' if st.session_state.learner_mode else 'Learner'} Mode", use_container_width=True):
        st.session_state.learner_mode = not st.session_state.learner_mode
        st.rerun()
    st.caption(f"**Current:** {mode_label}")

# ============================================================================
# CONDITIONAL STYLING
# ============================================================================
if st.session_state.learner_mode:
    # Learner/Hacker Mode - Futuristic transparent dark theme
    st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        }
        
        /* Main content area */
        .main .block-container {
            background: rgba(15, 15, 35, 0.95);
            padding: 2rem;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 157, 0.3);
        }
        
        /* Text styling - Better contrast */
        .stMarkdown, .stText {
            color: #e0e0e0 !important;
            font-family: 'Courier New', monospace !important;
        }
        
        p, span, label, div {
            color: #d0d0d0 !important;
        }
        
        /* Headers - Cyan glow */
        h1, h2, h3 {
            color: #00ffdd !important;
            font-family: 'Courier New', monospace !important;
            text-shadow: 0 0 10px rgba(0, 255, 221, 0.6);
            border-bottom: 2px solid rgba(0, 255, 221, 0.5);
            padding-bottom: 0.5rem;
            margin-top: 2rem;
            background: rgba(0, 255, 221, 0.05);
            padding: 1rem;
            border-radius: 5px;
        }
        
        h4, h5, h6 {
            color: #00ffaa !important;
            font-family: 'Courier New', monospace !important;
        }
        
        /* Input areas - Dark with cyan border */
        .stTextArea textarea, .stTextInput input, .stSelectbox select {
            background: rgba(20, 20, 40, 0.9) !important;
            border: 2px solid #00ffdd !important;
            color: #e0e0e0 !important;
            font-family: 'Courier New', monospace !important;
            box-shadow: inset 0 0 10px rgba(0, 255, 221, 0.1);
        }
        
        .stTextArea label, .stTextInput label, .stSelectbox label {
            color: #00ffdd !important;
            font-weight: bold;
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, rgba(0, 255, 221, 0.2), rgba(0, 255, 157, 0.2)) !important;
            border: 2px solid #00ffdd !important;
            color: #00ffdd !important;
            font-family: 'Courier New', monospace !important;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(0, 255, 221, 0.3);
            transition: all 0.3s;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, rgba(0, 255, 221, 0.3), rgba(0, 255, 157, 0.3)) !important;
            box-shadow: 0 6px 20px rgba(0, 255, 221, 0.5);
            transform: translateY(-2px);
        }
        
        /* Metrics - Dark cards with cyan accent */
        [data-testid="stMetricValue"] {
            background: rgba(20, 20, 40, 0.8);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(0, 255, 221, 0.4);
            box-shadow: 0 4px 10px rgba(0, 255, 221, 0.2);
        }
        
        [data-testid="stMetricLabel"] {
            color: #00ffdd !important;
            font-family: 'Courier New', monospace !important;
            font-size: 0.9rem !important;
            font-weight: bold !important;
        }
        
        [data-testid="stMetricValue"] > div {
            color: #ffffff !important;
            font-family: 'Courier New', monospace !important;
            font-size: 1.8rem !important;
            text-shadow: 0 0 8px rgba(0, 255, 221, 0.6);
        }
        
        /* Dataframes */
        .stDataFrame {
            border: 2px solid rgba(0, 255, 221, 0.4) !important;
            background: rgba(20, 20, 40, 0.8) !important;
            border-radius: 8px;
        }
        
        .stDataFrame table {
            background: rgba(20, 20, 40, 0.9) !important;
            color: #e0e0e0 !important;
        }
        
        .stDataFrame th {
            background: rgba(0, 255, 221, 0.2) !important;
            color: #00ffdd !important;
            font-weight: bold !important;
        }
        
        /* Code blocks */
        .stCodeBlock, code {
            background: rgba(15, 15, 30, 0.95) !important;
            border: 1px solid rgba(0, 255, 221, 0.4) !important;
            color: #00ff88 !important;
            font-family: 'Courier New', monospace !important;
            box-shadow: 0 0 15px rgba(0, 255, 221, 0.2);
            border-radius: 5px;
            padding: 1rem;
        }
        
        /* Info/Success/Warning boxes */
        .stAlert {
            background: rgba(20, 20, 40, 0.9) !important;
            border-left: 4px solid #00ffdd !important;
            color: #e0e0e0 !important;
            border-radius: 5px;
        }
        
        .stSuccess {
            background: rgba(0, 255, 157, 0.1) !important;
            border-left: 4px solid #00ff9d !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(0, 255, 221, 0.1) !important;
            border: 1px solid rgba(0, 255, 221, 0.4) !important;
            color: #00ffdd !important;
            font-family: 'Courier New', monospace !important;
            border-radius: 5px;
        }
        
        .streamlit-expanderContent {
            background: rgba(15, 15, 30, 0.9) !important;
            border: 1px solid rgba(0, 255, 221, 0.3) !important;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }
        
        /* Scrolling code effect */
        .code-stream {
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            color: #00ff88;
            background: rgba(10, 10, 20, 0.95);
            padding: 15px;
            border: 2px solid rgba(0, 255, 221, 0.4);
            border-radius: 8px;
            max-height: 300px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0, 255, 221, 0.3);
            margin: 15px 0;
            line-height: 1.6;
        }
        
        .code-line {
            padding: 2px 0;
            border-left: 3px solid transparent;
            padding-left: 10px;
            transition: all 0.3s;
        }
        
        .code-line:hover {
            background: rgba(0, 255, 221, 0.1);
            border-left-color: #00ffdd;
        }
        
        /* Plotly charts */
        .js-plotly-plot {
            border: 2px solid rgba(0, 255, 221, 0.4) !important;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0, 255, 221, 0.2);
            background: rgba(20, 20, 40, 0.8) !important;
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: #00ffdd !important;
        }
        
        /* Caption text */
        .caption, small {
            color: #00ffaa !important;
            font-family: 'Courier New', monospace !important;
        }
        
        /* Dividers */
        hr {
            border-color: rgba(0, 255, 221, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # User Mode - Clean default theme
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            padding: 1rem 0;
        }
        .section-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# INTRO
# ============================================================================
if st.session_state.learner_mode:
    st.markdown("""
    ```
    [SYSTEM INITIALIZATION]
    >>> Loading NLP pipeline modules...
    >>> Marathi language processing: ACTIVE
    >>> Machine learning models: ONLINE
    >>> Ready for deep linguistic analysis
    ```
    """)
    st.info("🎓 **LEARNER MODE ACTIVE** - Dive deep into how NLP algorithms process Marathi text")
else:
    st.markdown("""
    Analyze Marathi text with multiple NLP techniques:
    - **Tokenization** - Split text into meaningful units
    - **Sentiment Analysis** - Detect positive/negative/neutral sentiment
    - **Emotion Detection** - Identify dominant emotions (joy, anger, sadness, fear, etc.)
    - **POS Tagging** - Heuristic part-of-speech tagging
    - **Named Entities** - Extract entity candidates
    - **TF-IDF** - Find most important terms
    - **Topic Modeling** - LDA topic distribution
    - **Semantic Analysis** - Advanced linguistic features
    """)

# ============================================================================
# INPUT
# ============================================================================
st.header("Input Text")

# Example texts with various sentiment and emotion patterns
example_texts = {
    "None": "",
    
    # Positive Examples
    "Positive 1": "आज खूप छान दिवस आहे. मला खूप आनंद झाला.",
    "Positive 2": "तुमचे काम खूप उत्तम आहे. मी खूप प्रभावित झालो.",
    "Positive 3": "आजचा कार्यक्रम अप्रतिम होता. सर्वांना खूप मजा आली.",
    "Positive 4": "तुमची मदत फार मोलाची आहे. खूप खूप धन्यवाद.",
    "Positive 5": "हे चित्र पाहून मन प्रसन्न झाले. खूप सुंदर आहे.",
    
    # Negative Examples
    "Negative 1": "हा निर्णय खूप वाईट आहे. माझी खूप निराशा झाली.",
    "Negative 2": "तुझे वर्तन मला आवडत नाही. खूप वाईट वागलास.",
    "Negative 3": "आजचा दिवस फार वाईट गेला. काहीच बरे झाले नाही.",
    "Negative 4": "या गोष्टीचा मला राग येतो. अत्यंत निराशाजनक आहे.",
    "Negative 5": "हे परिणाम अपेक्षेपेक्षा खूप वाईट आहेत. दुःख झाले.",
    
    # Mixed Sentiment
    "Mixed 1": "भारत एक महान देश आहे. मुंबई आणि दिल्ली मोठी शहरे आहेत.",
    "Mixed 2": "चित्रपट चांगला होता पण शेवट खूप कमकुवत होता.",
    "Mixed 3": "जेवण चवीला होते परंतु सेवा फार मंद होती.",
    
    # Contempt/Sarcasm
    "Contempt 1": "तुझी तेवढी तरी लायक आहे का?",
    "Contempt 2": "वाह! किती हुशार आहात तुम्ही!",
    "Contempt 3": "असे का करतोस तू? काय समजतोस स्वतःला?",
    
    # Anger/Frustration
    "Anger 1": "अक्कल नको पाजळू तुझी.",
    "Anger 2": "बंद करा हे नाटक आता.",
    "Anger 3": "माझे ऐकणे बंद करा. मला काही नको.",
    "Anger 4": "थांब! आणखी एक शब्द नको.",
    
    # Dismissive
    "Dismissive 1": "नाटक करूनही सहानुभूती नाही मिळणार.",
    "Dismissive 2": "काय करणार ते कर. मला काही फरक पडत नाही.",
    "Dismissive 3": "तुझे बोलणे मला ऐकायचे नाही.",
    
    # Neutral
    "Neutral 1": "मला भूक लागलेली नाही.",
    "Neutral 2": "मी त्याला माझ्या आयुष्यात कधाही पाहिले नाही.",
    "Neutral 3": "आज मंगळवार आहे.",
    "Neutral 4": "ती पुस्तक वाचत आहे.",
    "Neutral 5": "मी उद्या येईन.",
    
    # Dislike
    "Dislike 1": "हे मला आवडत नाही.",
    "Dislike 2": "या गोष्टीबद्दल मला नाराजी आहे.",
    "Dislike 3": "मी या कामाला विरोध करतो.",
    
    # Joy/Happiness
    "Joy 1": "आज माझा वाढदिवस आहे! खूप आनंद झाला!",
    "Joy 2": "मी परीक्षेत यशस्वी झालो! अप्रतिम!",
    "Joy 3": "वाह! मला नोकरी मिळाली!",
    "Joy 4": "आज खूप छान बातमी मिळाली.",
    
    # Sadness
    "Sadness 1": "मला खूप दुःख झाले.",
    "Sadness 2": "तो माझा जिवलग मित्र होता. त्याच्या जाण्याने खूप वाईट वाटते.",
    "Sadness 3": "आज मी खूप एकटा आहे.",
    
    # Fear/Worry
    "Fear 1": "मला खूप भीती वाटते.",
    "Fear 2": "परीक्षा जवळ येत आहे. मी काळजीत आहे.",
    "Fear 3": "मला वाटते काहीतरी वाईट होणार आहे.",
    
    # Surprise
    "Surprise 1": "अरे! हे काय आहे?",
    "Surprise 2": "खरोखर? मला माहित नव्हते!",
    "Surprise 3": "काय! तू इथे कशी?",
    
    # Love/Affection
    "Love 1": "तू माझी सर्वात प्रिय व्यक्ती आहेस.",
    "Love 2": "माझ्या आई-बाबांवर खूप प्रेम आहे.",
    "Love 3": "माझे कुटुंब माझी ताकद आहे.",
    
    # Gratitude
    "Gratitude 1": "तुमचे खूप खूप आभार.",
    "Gratitude 2": "तुमची मदत मला कधीच विसरणार नाही.",
    "Gratitude 3": "तुमच्या पाठिंब्यामुळे मी यशस्वी झालो.",
    
    # Hope/Optimism
    "Hope 1": "उद्या नक्कीच चांगले होईल.",
    "Hope 2": "सर्व काही व्यवस्थित होईल.",
    "Hope 3": "मला विश्वास आहे की आपण यशस्वी होऊ.",
    
    # Disappointment
    "Disappointment 1": "मी अपेक्षा केली होती पण तसे झाले नाही.",
    "Disappointment 2": "खूप वाईट वाटले.",
    "Disappointment 3": "निराशा हाती लागली.",
    
    # Confusion
    "Confusion 1": "मला काही समजत नाही.",
    "Confusion 2": "हे कसे शक्य आहे?",
    "Confusion 3": "मी गोंधळलो आहे.",
    
    # Pride
    "Pride 1": "मला माझ्या कामाचा अभिमान आहे.",
    "Pride 2": "आम्ही भारतीय आहोत याचा मला अभिमान आहे.",
    "Pride 3": "माझ्या मुलाने उत्तम काम केले.",
    
    # Formal/Polite
    "Formal 1": "कृपया मला मदत करा.",
    "Formal 2": "आपले स्वागत आहे.",
    "Formal 3": "धन्यवाद. आपल्या सेवेची प्रशंसा.",
    
    # Informal/Casual
    "Informal 1": "अरे यार, काय हो?",
    "Informal 2": "चल बाबा, जाऊ कुठेतरी.",
    "Informal 3": "काय रे, कसा आहेस?",
    
    # Questions
    "Question 1": "तू कुठे जातोस?",
    "Question 2": "काय झाले?",
    "Question 3": "कसे आहेत सर्व?",
    "Question 4": "कधी येणार आहेस?",
    "Question 5": "कोण आले होते?",
    
    # Commands/Requests
    "Command 1": "येथे या.",
    "Command 2": "मला ते पुस्तक दे.",
    "Command 3": "शांत बसा.",
    "Command 4": "जा आता.",
    
    # News/Information
    "News 1": "महाराष्ट्र सरकारने आज नवीन योजना जाहीर केली.",
    "News 2": "मुख्यमंत्री यांनी हे जाहीर केले.",
    "News 3": "आज मुंबईत पाऊस पडला.",
    "News 4": "नवीन शाळा उद्या सुरू होणार आहे.",
    
    # Complex Sentences
    "Complex 1": "जरी मी प्रयत्न केला तरी यश मिळाले नाही.",
    "Complex 2": "त्याने काम केले पण फळ मिळाले नाही.",
    "Complex 3": "मी जाणार होतो पण पाऊस सुरू झाला.",
    "Complex 4": "तो चांगला आहे परंतु कधीकधी रागावतो.",
    
    # Philosophical/Deep
    "Philosophical 1": "आयुष्य एक प्रवास आहे.",
    "Philosophical 2": "वेळ सर्वात मोलाची संपत्ती आहे.",
    "Philosophical 3": "प्रेम हेच खरे धन आहे.",
    
    # Descriptive
    "Descriptive 1": "हे फूल खूप सुंदर आणि सुगंधी आहे.",
    "Descriptive 2": "आकाश निळे आणि स्वच्छ आहे.",
    "Descriptive 3": "समुद्र खूप मोठा आणि खोल आहे.",
    
    # Comparisons
    "Comparison 1": "हे ते पेक्षा चांगले आहे.",
    "Comparison 2": "मुंबई दिल्ली पेक्षा मोठी आहे.",
    "Comparison 3": "आज काल पेक्षा गरम आहे.",
    
    # Temporal
    "Temporal 1": "पहिले मी जाईन, नंतर तू ये.",
    "Temporal 2": "काल पाऊस पडला होता.",
    "Temporal 3": "उद्या चांगला दिवस असेल.",
    
    # Causation
    "Causation 1": "मी आजारी होतो म्हणून घरी राहिलो.",
    "Causation 2": "पाऊस पडला त्यामुळे रस्ते ओले झाले.",
    "Causation 3": "मेहनत केली म्हणून यश मिळाले.",
    
    # Negation Heavy
    "Negation 1": "मी नाही जाणार. तू नको बोलू.",
    "Negation 2": "काहीही नाही. कोणीही नाही.",
    "Negation 3": "मला नको. मी नाही करणार.",
    
    # Intensified
    "Intensified 1": "खूप खूप छान! अप्रतिम! विलक्षण!",
    "Intensified 2": "अत्यंत महत्त्वाचे. फार जरूरी.",
    "Intensified 3": "एकदम उत्तम. नक्कीच करू."
}

selected_example = st.selectbox("Load an example:", list(example_texts.keys()))

input_text = st.text_area(
    "Enter Marathi text to analyze:",
    value=example_texts[selected_example],
    height=150,
    placeholder="मराठी मजकूर इथे टाईप करा..."
)

analyze_button = st.button("🔍 Analyze", type="primary")

# ============================================================================
# ANALYSIS & RESULTS
# ============================================================================
if analyze_button and input_text.strip():
    with st.spinner("Analyzing text..."):
        results = analyze_text(input_text)
    
    # ========================================================================
    # TOKENS
    # ========================================================================
    if st.session_state.learner_mode:
        st.markdown("### ⚙️ MODULE 1: TOKENIZATION ENGINE")
        with st.expander("📜 View Processing Code", expanded=False):
            st.code("""
# Marathi-Only Tokenization Algorithm
import regex as re
DEVANAGARI_ONLY_RE = re.compile(r"[\p{Devanagari}]+")

def tokenize(text: str, marathi_only=True):
    '''Extract only Devanagari script tokens from text'''
    if marathi_only:
        # Filter: Extract ONLY Devanagari characters
        tokens = DEVANAGARI_ONLY_RE.findall(text)
    else:
        # Keep mixed content (Devanagari + English + numbers)
        tokens = [t for t in text.split() if t]
    return tokens

# Execution (Marathi-only mode)
result = tokenize(input_text, marathi_only=True)
print(f"Extracted {len(result)} Devanagari tokens")
print(f"Non-Marathi content filtered out")
            """, language="python")
    else:
        st.header("1️⃣ Tokenization")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.learner_mode:
            st.markdown(f"**🔍 OUTPUT:** `{results['token_count']}` tokens extracted")
            st.code(f"tokens = {results['tokens']}", language="python")
        else:
            st.markdown(f"**Tokens ({results['token_count']}):**")
            st.code(" | ".join(results['tokens']), language=None)
    
    with col2:
        st.metric("Total Tokens", results['token_count'])
        if st.session_state.learner_mode:
            st.metric("Avg Token Length", f"{sum(len(t) for t in results['tokens'])/len(results['tokens']):.1f}" if results['tokens'] else "0")
    
    # ========================================================================
    # SENTIMENT
    # ========================================================================
    if st.session_state.learner_mode:
        st.markdown("### 🧮 MODULE 2: SENTIMENT ANALYSIS ALGORITHM")
        with st.expander("📜 View Processing Code", expanded=False):
            st.code("""
# Sentiment Scoring Algorithm
def analyze_sentiment(text):
    tokens = tokenize(text)
    
    # Lexicon matching
    pos_count = sum(1 for t in tokens if t in POSITIVE_LEXICON)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_LEXICON)
    base_score = pos_count - neg_count
    
    # Detect modifiers
    has_negation = any(t in ['नाही', 'नको'] for t in tokens)
    has_intensifier = any(t in ['खूप', 'फार'] for t in tokens)
    
    # Adjust score
    adjusted_score = -base_score if has_negation else base_score
    adjusted_score *= 1.5 if has_intensifier else 1.0
    
    return {
        'score': adjusted_score,
        'label': 'positive' if adjusted_score > 0 else 'negative',
        'modifiers': {'negation': has_negation, 'intensifier': has_intensifier}
    }
            """, language="python")
    else:
        st.header("2️⃣ Sentiment Analysis")
    
    sentiment = results['sentiment']
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sentiment", sentiment['label'].upper(), delta=sentiment['score'])
    col2.metric("Score", sentiment['score'])
    col3.metric("Positive Words", sentiment['pos_words'])
    col4.metric("Negative Words", sentiment['neg_words'])
    
    # Sentiment gauge
    sentiment_score_normalized = max(-1, min(1, sentiment['score'] / 5))  # normalize to [-1, 1]
    fig_sentiment = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sentiment_score_normalized,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sentiment Score"},
        delta={'reference': 0},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-1, -0.3], 'color': "lightcoral"},
                {'range': [-0.3, 0.3], 'color': "lightgray"},
                {'range': [0.3, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0
            }
        }
    ))
    fig_sentiment.update_layout(height=300)
    st.plotly_chart(fig_sentiment, use_container_width=True)
    
    # ========================================================================
    # EMOTION
    # ========================================================================
    if st.session_state.learner_mode:
        st.markdown("### 💭 MODULE 3: EMOTION CLASSIFICATION ENGINE")
        with st.expander("📜 View Processing Code", expanded=False):
            st.code("""
# Complex Emotion Detection
def detect_complex_emotions(tokens, text):
    negation_words = {'नाही', 'नको', 'नसते'}
    contempt_markers = {'तेवढी', 'तरी', 'लायक'}
    
    has_negation = any(w in tokens for w in negation_words)
    has_question = '?' in text
    has_contempt = len(set(tokens) & contempt_markers) >= 2
    
    complex_emotions = {}
    if has_contempt and has_question:
        complex_emotions['contempt'] = 0.8
    if has_negation:
        complex_emotions['negation_tone'] = 0.6
    
    return complex_emotions

# Basic emotion lexicon matching
emotion_counts = Counter()
for token in tokens:
    for emotion, lexicon in EMOTION_LEXICONS.items():
        if token in lexicon:
            emotion_counts[emotion] += 1
            """, language="python")
    else:
        st.header("3️⃣ Emotion Detection")
    
    emotion = results['emotion']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Dominant Emotion", emotion['dominant'].upper())
    
    with col2:
        if emotion['counts']:
            emotion_df = pd.DataFrame([
                {"Emotion": emo, "Count": count}
                for emo, count in emotion['counts'].items()
            ]).sort_values("Count", ascending=False)
            
            fig_emotion = px.bar(
                emotion_df,
                x="Count",
                y="Emotion",
                orientation="h",
                title="Emotion Word Counts",
                color="Count",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_emotion, use_container_width=True)
        else:
            st.info("No emotion words detected.")
    
    # ========================================================================
    # POS TAGGING
    # ========================================================================
    st.header("4️⃣ Part-of-Speech Tagging")
    pos = results['pos']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Tagged Tokens:**")
        tagged_text = " | ".join([f"{tok}_{tag}" for tok, tag in pos['tagged'][:50]])
        st.code(tagged_text, language=None)
        if len(pos['tagged']) > 50:
            st.caption(f"... and {len(pos['tagged']) - 50} more tokens")
    
    with col2:
        if pos['counts']:
            pos_df = pd.DataFrame([
                {"POS Tag": tag, "Count": count}
                for tag, count in pos['counts'].items()
            ]).sort_values("Count", ascending=False)
            
            fig_pos = px.pie(
                pos_df,
                values="Count",
                names="POS Tag",
                title="POS Tag Distribution"
            )
            st.plotly_chart(fig_pos, use_container_width=True)
    
    # ========================================================================
    # ENTITIES
    # ========================================================================
    st.header("5️⃣ Named Entities")
    entities = results['entities']
    
    if entities['entities']:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric("Entities Found", len(set(entities['entities'])))
            st.markdown("**Entity List:**")
            st.code(" | ".join(set(entities['entities'])), language=None)
        
        with col2:
            if entities['counts']:
                entity_df = pd.DataFrame([
                    {"Entity": ent, "Count": count}
                    for ent, count in entities['counts'].items()
                ]).sort_values("Count", ascending=False).head(15)
                
                fig_entities = px.bar(
                    entity_df,
                    x="Count",
                    y="Entity",
                    orientation="h",
                    title="Top Entities by Frequency",
                    color="Count",
                    color_continuous_scale="Blues"
                )
                st.plotly_chart(fig_entities, use_container_width=True)
    else:
        st.info("No named entities detected.")
    
    # ========================================================================
    # TF-IDF
    # ========================================================================
    st.header("6️⃣ TF-IDF Analysis")
    tfidf = results['tfidf']
    
    if 'error' in tfidf:
        st.error(f"TF-IDF Error: {tfidf['error']}")
    elif tfidf['top_terms']:
        tfidf_df = pd.DataFrame(tfidf['top_terms'], columns=["Term", "Score"])
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(tfidf_df, use_container_width=True)
        
        with col2:
            fig_tfidf = px.bar(
                tfidf_df,
                x="Score",
                y="Term",
                orientation="h",
                title="Top TF-IDF Terms",
                color="Score",
                color_continuous_scale="Reds"
            )
            st.plotly_chart(fig_tfidf, use_container_width=True)
    else:
        st.info("No significant TF-IDF terms found.")
    
    # ========================================================================
    # LDA TOPICS
    # ========================================================================
    st.header("7️⃣ Topic Modeling (LDA)")
    lda = results['lda']
    
    if 'error' in lda:
        st.error(f"LDA Error: {lda['error']}")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Dominant Topic", f"Topic {lda['dominant_topic']}")
            st.metric("Topic Probability", f"{lda['dominant_topic_prob']:.2%}")
            st.markdown("**Top Words in Dominant Topic:**")
            st.code(" | ".join(lda['dominant_topic_words']), language=None)
        
        with col2:
            topic_df = pd.DataFrame([
                {"Topic": topic, "Probability": prob}
                for topic, prob in lda['topic_distribution'].items()
            ]).sort_values("Probability", ascending=False)
            
            fig_lda = px.bar(
                topic_df,
                x="Probability",
                y="Topic",
                orientation="h",
                title="Topic Distribution",
                color="Probability",
                color_continuous_scale="Greens"
            )
            st.plotly_chart(fig_lda, use_container_width=True)
    
    # ========================================================================
    # SEMANTIC ANALYSIS
    # ========================================================================
    if results.get('semantic') and 'error' not in results['semantic']:
        st.header("8️⃣ Semantic Analysis")
        
        sem = results['semantic']
        
        # Features
        if sem.get('features'):
            st.subheader("📊 Semantic Features")
            feat = sem['features']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Formality", feat.get('formality', 'N/A').title())
                st.metric("Politeness", feat.get('politeness', 'N/A').title())
            with col2:
                st.metric("Certainty", feat.get('certainty', 'N/A').title())
                st.metric("Complexity", feat.get('complexity', 'N/A').title())
            with col3:
                st.metric("Verb Type", feat.get('verb_type', 'N/A').replace('-', ' ').title())
                st.metric("Avg Word Length", feat.get('avg_word_length', 0))
            with col4:
                temporal = feat.get('temporal_references', [])
                st.metric("Time References", ", ".join(temporal).title() if temporal else "None")
                st.metric("Lexical Diversity", feat.get('lexical_diversity', 0))
            
            # Additional features
            feat_notes = []
            if feat.get('has_causality'):
                feat_notes.append("⚡ Causal relationships")
            if feat.get('has_contrast'):
                feat_notes.append("🔄 Contrasts/comparisons")
            if feat_notes:
                st.write("**Notable:**", " • ".join(feat_notes))
        
        # Speech Acts
        if sem.get('speech_acts'):
            st.subheader("💬 Speech Acts")
            acts = sem['speech_acts']
            st.write(f"**Type:** {', '.join([a.title() for a in acts])}")
        
        # Discourse Structure
        if sem.get('discourse'):
            st.subheader("📝 Discourse Markers")
            disc = sem['discourse']
            
            markers = []
            if disc.get('has_introduction'):
                markers.append("🎬 Introduction")
            if disc.get('has_conclusion'):
                markers.append("🏁 Conclusion")
            if disc.get('has_elaboration'):
                markers.append("📖 Elaboration")
            if disc.get('has_addition', 0) > 0:
                markers.append(f"➕ Addition ({disc['has_addition']}x)")
            if disc.get('has_contrast', 0) > 0:
                markers.append(f"⚖️ Contrast ({disc['has_contrast']}x)")
            
            if markers:
                st.write(" • ".join(markers))
            else:
                st.info("No specific discourse markers")
        
        # Semantic Relations
        if sem.get('semantic_relations') and sem['semantic_relations'][0] != 'none':
            st.subheader("🔗 Semantic Relations")
            for rel in sem['semantic_relations']:
                st.write(f"• {rel.title()}")
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    st.header("📊 Summary")
    st.markdown(f"""
    **Text Statistics:**
    - Tokens: {results['token_count']}
    - Sentiment: {sentiment['label'].upper()} (score: {sentiment['score']})
    - Dominant Emotion: {emotion['dominant'].upper()}
    - Named Entities: {len(set(entities['entities'])) if entities['entities'] else 0}
    - Dominant Topic: Topic {lda['dominant_topic']} ({lda['dominant_topic_prob']:.1%})
    """)

elif analyze_button:
    st.warning("⚠️ Please enter some text to analyze.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with Streamlit • Marathi NLP Analysis Tool</p>
    <p><small>Uses lexicon-based sentiment, emotion, heuristic POS tagging, TF-IDF, and LDA</small></p>
</div>
""", unsafe_allow_html=True)
