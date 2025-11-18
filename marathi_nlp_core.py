"""
Marathi NLP Core Module
Reusable functions for tokenization, sentiment, emotion, POS, entities, TF-IDF, and LDA.
"""

import regex as re
import json
import joblib
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Import semantic analysis module
try:
    from semantic_analysis import get_semantic_summary
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    print("Warning: semantic_analysis module not found. Semantic features disabled.")

# ============================================================================
# REGEX PATTERNS
# ============================================================================
TOKEN_SPLIT_RE = re.compile(r"[^\p{Devanagari}A-Za-z0-9]+")
DEVANAGARI_ONLY_RE = re.compile(r"[\p{Devanagari}]+")

# ============================================================================
# TOKENIZER
# ============================================================================
def tokenize(text: str, marathi_only=True):
    """
    Marathi tokenizer with option to filter non-Devanagari text.
    
    Args:
        text: Input text string
        marathi_only: If True, extract only Devanagari tokens (default: True)
                     If False, include English/numbers
    
    Returns:
        List of tokens
    """
    if not isinstance(text, str):
        return []
    
    if marathi_only:
        # Extract only Devanagari script tokens
        tokens = DEVANAGARI_ONLY_RE.findall(text)
    else:
        # Keep both Devanagari and English/numbers
        tokens = [t for t in TOKEN_SPLIT_RE.split(text) if t]
    
    return tokens

# ============================================================================
# LOAD RESOURCES (called once at module import or app startup)
# ============================================================================

# Sentiment lexicons
def load_sentiment_lexicons():
    """Load positive and negative sentiment word sets from CSV."""
    try:
        df = pd.read_csv("sentiment_lexicon.csv")
        positive = set(df[df["polarity"] == "positive"]["word"])
        negative = set(df[df["polarity"] == "negative"]["word"])
        return positive, negative
    except Exception as e:
        print(f"Warning: Could not load sentiment_lexicon.csv: {e}")
        return set(), set()

# Emotion lexicons
def load_emotion_lexicons():
    """Load emotion lexicons from CSV."""
    try:
        df = pd.read_csv("emotion_lexicon.csv")
        lexicons = {}
        for emo in df["emotion"].unique():
            lexicons[emo] = set(df[df["emotion"] == emo]["word"])
        return lexicons
    except Exception as e:
        print(f"Warning: Could not load emotion_lexicon.csv: {e}")
        return {}

# Stopwords
def load_stopwords():
    """Load stopwords from CSV."""
    try:
        df = pd.read_csv("marathi_stopwords.csv")
        return set(df["stopword"])
    except Exception as e:
        print(f"Warning: Could not load marathi_stopwords.csv: {e}")
        return set()

# Entities
def load_entities():
    """Load named entity candidates from CSV."""
    try:
        df = pd.read_csv("marathi_entities.csv")
        return set(df["entity"])
    except Exception as e:
        print(f"Warning: Could not load marathi_entities.csv: {e}")
        return set()

# TF-IDF Vectorizer (rebuild from vocabulary)
def load_tfidf_vectorizer():
    """
    Load TF-IDF vectorizer. If the .joblib file exists and can be loaded, use it.
    Otherwise, rebuild from vocabulary JSON.
    """
    try:
        vectorizer = joblib.load("tfidf_vectorizer.joblib")
        return vectorizer
    except Exception:
        # Fallback: rebuild from vocabulary and fit on dummy data
        try:
            with open("tfidf_vocab.json", "r", encoding="utf-8") as f:
                vocab = json.load(f)
            vectorizer = TfidfVectorizer(
                tokenizer=tokenize,
                preprocessor=lambda x: x,
                token_pattern=None,
                vocabulary=vocab
            )
            # Fit on a dummy document to initialize the vectorizer
            dummy_text = " ".join(list(vocab.keys())[:100])
            vectorizer.fit([dummy_text])
            return vectorizer
        except Exception as e:
            print(f"Warning: Could not load TF-IDF vectorizer: {e}")
            return None

# Count Vectorizer (rebuild from vocabulary)
def load_count_vectorizer():
    """Load CountVectorizer from vocabulary JSON."""
    try:
        with open("count_vocab.json", "r", encoding="utf-8") as f:
            vocab = json.load(f)
        vectorizer = CountVectorizer(
            tokenizer=tokenize,
            preprocessor=lambda x: x,
            token_pattern=None,
            vocabulary=vocab
        )
        # Fit on dummy data to initialize
        dummy_text = " ".join(list(vocab.keys())[:100])
        vectorizer.fit([dummy_text])
        return vectorizer
    except Exception as e:
        print(f"Warning: Could not load count vocabulary: {e}")
        return None

# LDA Model
def load_lda_model():
    """Load pre-trained LDA model."""
    try:
        return joblib.load("lda_model.joblib")
    except Exception as e:
        print(f"Warning: Could not load lda_model.joblib: {e}")
        return None

# ============================================================================
# INITIALIZE RESOURCES (load once at module level)
# ============================================================================
MARATHI_POSITIVE, MARATHI_NEGATIVE = load_sentiment_lexicons()
EMOTION_LEXICONS = load_emotion_lexicons()
STOPWORD_SET = load_stopwords()
ENTITY_SET = load_entities()
TFIDF_VECTORIZER = load_tfidf_vectorizer()
COUNT_VECTORIZER = load_count_vectorizer()
LDA_MODEL = load_lda_model()

# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================
def sentiment_score(tokens):
    """Compute sentiment score from tokens using lexicon."""
    pos = sum(1 for t in tokens if t in MARATHI_POSITIVE)
    neg = sum(1 for t in tokens if t in MARATHI_NEGATIVE)
    return pos - neg

def sentiment_label(score):
    """Convert sentiment score to label."""
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"

def detect_sentiment_modifiers(tokens, text):
    """Detect sentiment modifiers like negations, intensifiers, and diminishers."""
    modifiers = {}
    
    # Negation detection
    negation_words = {'नाही', 'नको', 'नसते', 'नव्हते', 'नसावे', 'कधीही', 'नाहीत'}
    modifiers['has_negation'] = any(word in tokens for word in negation_words)
    modifiers['negation_count'] = sum(1 for word in tokens if word in negation_words)
    
    # Intensifiers (amplify sentiment)
    intensifiers = {'खूप', 'फार', 'अत्यंत', 'विशेष', 'एकदम', 'नक्कीच'}
    modifiers['has_intensifier'] = any(word in tokens for word in intensifiers)
    modifiers['intensifier_count'] = sum(1 for word in tokens if word in intensifiers)
    
    # Diminishers (reduce sentiment)
    diminishers = {'थोडे', 'जरा', 'किंचित', 'अगदी'}
    modifiers['has_diminisher'] = any(word in tokens for word in diminishers)
    
    # Question form (can indicate sarcasm or genuine inquiry)
    modifiers['is_question'] = '?' in text
    
    return modifiers

def analyze_sentiment(text: str):
    """Return enhanced sentiment analysis with modifiers and context."""
    tokens = tokenize(text)
    
    if not tokens:
        return {"score": 0, "label": "neutral", "pos_words": 0, "neg_words": 0, "note": "No tokens found"}
    
    # Count positive and negative words with position awareness
    pos_words = [t for t in tokens if t in MARATHI_POSITIVE]
    neg_words = [t for t in tokens if t in MARATHI_NEGATIVE]
    pos_count = len(pos_words)
    neg_count = len(neg_words)
    
    # Calculate base score with weighted importance (later words matter more)
    base_score = 0
    for i, token in enumerate(tokens):
        weight = 1.0 + (i / len(tokens)) * 0.3  # 1.0 to 1.3 weight
        if token in MARATHI_POSITIVE:
            base_score += weight
        elif token in MARATHI_NEGATIVE:
            base_score -= weight
    
    # Get modifiers
    modifiers = detect_sentiment_modifiers(tokens, text)
    
    # Adjust score based on modifiers with better logic
    adjusted_score = base_score
    
    # Negation handling with proximity and preference detection
    if modifiers['has_negation']:
        negation_positions = [i for i, t in enumerate(tokens) if t in {'नाही', 'नको', 'नसते', 'नव्हते', 'नसावे', 'कधीही', 'नाहीत'}]
        
        # Check if it's a preference expression (negated like/want)
        preference_words = {'आवडत', 'आवड', 'पसंद', 'इच्छा', 'मना'}
        has_negated_preference = False
        
        for neg_pos in negation_positions:
            # Check words within 2 positions after negation
            for i in range(neg_pos + 1, min(neg_pos + 3, len(tokens))):
                if any(pref in tokens[i] for pref in preference_words):
                    has_negated_preference = True
                    break
        
        # If "नाही आवडत" pattern, it's negative dislike
        if has_negated_preference:
            adjusted_score = -2.0  # Strong negative
        else:
            # Standard negation logic
            # Check if negation is near sentiment words (within 3 tokens)
            negates_sentiment = False
            for neg_pos in negation_positions:
                for i, token in enumerate(tokens):
                    if token in MARATHI_POSITIVE or token in MARATHI_NEGATIVE:
                        if abs(i - neg_pos) <= 3:
                            negates_sentiment = True
                            break
            
            if negates_sentiment:
                if modifiers['negation_count'] == 1:
                    adjusted_score = -base_score
                elif modifiers['negation_count'] >= 2:  # Double negation cancels out
                    adjusted_score = base_score
            else:
                # Negation not near sentiment words, add slight negative bias
                adjusted_score = base_score - 0.5
    
    # Intensifiers amplify (stronger effect if near sentiment words)
    if modifiers['has_intensifier']:
        if abs(base_score) > 0:
            adjusted_score = adjusted_score * 1.6
        else:
            # Intensifier alone adds emotion
            adjusted_score = 1.0 if 'खूप' in tokens else 0.5
    
    # Diminishers reduce
    if modifiers['has_diminisher'] and base_score != 0:
        adjusted_score = adjusted_score * 0.6
    
    # Question with negative words indicates stronger negative sentiment
    if modifiers['is_question']:
        if neg_count > pos_count:
            adjusted_score = adjusted_score * 1.4
        elif pos_count > neg_count:
            adjusted_score = adjusted_score * 0.9  # Questions reduce positive certainty
    
    # Mixed sentiment detection (both positive and negative present)
    is_mixed = (pos_count > 0 and neg_count > 0 and abs(adjusted_score) < 2)
    
    label = sentiment_label(int(adjusted_score))
    if is_mixed:
        label = "mixed"
    
    result = {
        "score": int(adjusted_score),
        "base_score": base_score,
        "label": label, 
        "pos_words": pos_count, 
        "neg_words": neg_count,
        "modifiers": modifiers,
        "confidence": min((pos_count + neg_count) / len(tokens) * 100, 100) if tokens else 0
    }
    
    # Add interpretation notes
    notes = []
    if modifiers['has_negation']:
        notes.append("Negation detected - sentiment may be inverted")
    if modifiers['has_intensifier']:
        notes.append("Intensifier present - sentiment amplified")
    if modifiers['is_question'] and neg_count > 0:
        notes.append("Question with negative tone - possible sarcasm/contempt")
    if pos_count == 0 and neg_count == 0:
        notes.append("No sentiment words in lexicon")
    
    if notes:
        result["interpretation"] = " | ".join(notes)
    
    return result

# ============================================================================
# EMOTION DETECTION
# ============================================================================
def emotion_scores(tokens):
    """Count emotion words in tokens."""
    counts = Counter()
    for t in tokens:
        for emo, lex in EMOTION_LEXICONS.items():
            if t in lex:
                counts[emo] += 1
    return counts

def dominant_emotion(counts):
    """Get dominant emotion from counts."""
    if not counts:
        return "none"
    emo, c = counts.most_common(1)[0]
    return emo if c > 0 else "none"

def detect_complex_emotions(tokens, text):
    """Detect complex emotions using patterns and negations."""
    complex_emotions = {}
    tokens_set = set(tokens)
    
    # Negation markers
    negation_words = {'नाही', 'नको', 'नसते', 'नव्हते', 'नसावे', 'कधीही', 'राहिला'}
    has_negation = bool(tokens_set & negation_words)
    
    # Question patterns
    has_question = '?' in text or 'का' in tokens
    
    # Grief/Loss markers - expanded with better context detection
    grief_markers = {'जाणे', 'वाईट', 'वाटते', 'जिवलग', 'गमावले', 'शोकग्रस्त', 'मृत्यू', 
                     'मरण', 'निधन', 'गेले', 'गेला', 'मिस', 'आठवते', 'हृदयविदारक', 'वियोग',
                     'रडणे', 'अश्रूंनी', 'विरहाचे', 'होता', 'होती', 'शोकाकूल', 'दुख', 'दुःखी',
                     'शोक', 'विरह', 'वियोगी', 'दुखप्रद'}
    
    # Contextual grief patterns (past tense + relationship + loss)
    past_tense = {'होता', 'होती', 'होते', 'गेला', 'गेली', 'गेले'}
    relationships = {'मित्र', 'आई', 'बाबा', 'आजी', 'आजोबा', 'भाऊ', 'बहीण', 'नातू', 'जिवलग', 'प्रिय'}
    loss_verbs = {'जाणे', 'जाण्याने', 'गमावले', 'मिस', 'सोडून', 'विरह'}
    
    has_past_context = bool(tokens_set & past_tense)
    has_relationship = bool(tokens_set & relationships)
    has_loss = bool(tokens_set & loss_verbs)
    
    grief_score = len(tokens_set & grief_markers)
    
    # Boost grief score if contextual patterns present
    if has_past_context and has_relationship and has_loss:
        grief_score += 2
    elif (has_past_context and has_loss) or (has_relationship and has_loss):
        grief_score += 1
    
    # Contempt/Sarcasm patterns
    contempt_markers = {'तेवढी', 'तरी', 'लायक', 'काय'}
    has_contempt_pattern = len(tokens_set & contempt_markers) >= 2 and has_question
    
    # Dismissive patterns
    dismissive_markers = {'नाटक', 'सहानुभूती', 'मिळणार'}
    has_dismissive = len(tokens_set & dismissive_markers) >= 2 and has_negation
    
    # Frustration/Anger intensifiers
    anger_intensifiers = {'अक्कल', 'पाजळू', 'बंद', 'थांब', 'रागवणारे', 'कोप', 'कडवट'}
    has_anger_intensifier = bool(tokens_set & anger_intensifiers)
    
    # Uncertainty/Doubt
    doubt_markers = {'कदाचित', 'शक्य', 'नक्की', 'खरे', 'गोंधळ', 'अस्पष्ट', 'संभ्रम', 'अनिश्चित'}
    has_doubt = bool(tokens_set & doubt_markers)
    
    # Nostalgia/Longing
    nostalgia_markers = {'जुन्या', 'आठवणी', 'पूर्वीच्या', 'भूतकाळ', 'पूर्वी', 'मागच्या', 'जुने'}
    has_nostalgia = bool(tokens_set & nostalgia_markers)
    
    # Guilt/Shame
    guilt_markers = {'दोष', 'अपराध', 'ग्लानी', 'पश्चात्ताप', 'लाज', 'शरम', 'लज्जा', 'शर्मिंदा'}
    has_guilt = bool(tokens_set & guilt_markers)
    
    # Relief
    relief_markers = {'सुटका', 'आराम', 'शांती', 'दिलासा', 'मुक्त', 'स्वस्थ'}
    has_relief = bool(tokens_set & relief_markers)
    
    # Gratitude
    gratitude_markers = {'कृतज्ञ', 'आभार', 'धन्यवाद', 'उपकार', 'कौतुक'}
    has_gratitude = bool(tokens_set & gratitude_markers)
    
    # Envy/Jealousy
    envy_markers = {'मत्सर', 'हेवा', 'ईर्ष्या', 'संशय', 'शंका', 'जळत'}
    has_envy = bool(tokens_set & envy_markers)
    
    # Boredom
    boredom_markers = {'कंटाळा', 'कंटाळवाणा', 'नीरस', 'बोअर', 'आळस'}
    has_boredom = bool(tokens_set & boredom_markers)
    
    # Awe/Wonder
    awe_markers = {'अद्भुत', 'चमत्कारिक', 'अलौकिक', 'भव्यपणा', 'प्रभावशाली'}
    has_awe = bool(tokens_set & awe_markers)
    
    # Hope
    hope_markers = {'आशा', 'अपेक्षा', 'भरवसा', 'शक्यता', 'संधी', 'होणार', 'होईल'}
    has_hope = bool(tokens_set & hope_markers)
    
    # Despair
    despair_markers = {'हताश', 'हताशा', 'नाउमेद', 'व्यर्थ', 'असहाय', 'नाकाम', 'निष्फळ'}
    has_despair = bool(tokens_set & despair_markers)
    
    # Contentment/Peace
    contentment_markers = {'संतुष्ट', 'संतोष', 'तृप्त', 'शांत', 'समाधान'}
    has_contentment = bool(tokens_set & contentment_markers)
    
    # Excitement
    excitement_markers = {'रोमांच', 'जोश', 'उत्तेजना', 'थरार', 'उन्माद'}
    has_excitement = bool(tokens_set & excitement_markers)
    
    # Calculate complex emotions with proper scoring
    if grief_score >= 2:
        complex_emotions['grief'] = min(0.9, 0.6 + (grief_score * 0.1))
    elif grief_score == 1:
        complex_emotions['grief'] = 0.5
    
    if has_contempt_pattern:
        complex_emotions['contempt'] = 0.8
    if has_dismissive:
        complex_emotions['dismissiveness'] = 0.7
    if has_anger_intensifier and has_negation:
        complex_emotions['frustration'] = 0.75
    if has_negation and not (has_contempt_pattern or has_dismissive or grief_score):
        complex_emotions['negation_tone'] = 0.6
    if has_doubt:
        complex_emotions['uncertainty'] = 0.65
    if has_question and not has_contempt_pattern:
        complex_emotions['curiosity'] = 0.5
    if has_nostalgia:
        complex_emotions['nostalgia'] = 0.7
    if has_guilt:
        complex_emotions['guilt'] = 0.75
    if has_relief:
        complex_emotions['relief'] = 0.8
    if has_gratitude:
        complex_emotions['gratitude'] = 0.85
    if has_envy:
        complex_emotions['envy'] = 0.7
    if has_boredom:
        complex_emotions['boredom'] = 0.6
    if has_awe:
        complex_emotions['awe'] = 0.8
    if has_hope:
        complex_emotions['hope'] = 0.75
    if has_despair:
        complex_emotions['despair'] = 0.85
    if has_contentment:
        complex_emotions['contentment'] = 0.8
    if has_excitement:
        complex_emotions['excitement'] = 0.75
    
    return complex_emotions

def analyze_emotion(text: str):
    """Return emotion analysis for input text with complex emotion detection."""
    tokens = tokenize(text)
    
    if not tokens:
        return {"dominant": "none", "counts": {}, "note": "No tokens found"}
    
    # Basic emotion counts with weighted scoring
    counts = Counter()
    for i, token in enumerate(tokens):
        weight = 1.0 + (i / len(tokens)) * 0.2  # Later words slightly more important
        for emotion, lexicon in EMOTION_LEXICONS.items():
            if token in lexicon:
                counts[emotion] += weight
    
    # Complex emotion detection
    complex_emo = detect_complex_emotions(tokens, text)
    
    # Determine dominant emotion with complex emotions having priority
    dominant = "none"
    max_score = 0
    
    # Check complex emotions first (higher confidence)
    if complex_emo:
        for emotion, score in complex_emo.items():
            if score > max_score:
                max_score = score
                dominant = emotion
    
    # Check basic emotions if no strong complex emotion
    if max_score < 0.7 and counts:
        basic_dominant = counts.most_common(1)[0][0] if counts else "none"
        basic_score = counts[basic_dominant] / len(tokens) if counts else 0
        
        # Override with basic emotion if it's significantly stronger
        if basic_score > max_score * 1.2:  # Changed from 1.5 to 1.2 for better sensitivity
            dominant = basic_dominant
            max_score = basic_score
    
    # Special case: If shame appears with high count, prefer it over guilt
    if 'shame' in counts and counts['shame'] >= 2:
        dominant = 'shame'
        max_score = counts['shame'] / len(tokens)
    
    # Map complex emotion names to simpler categories when appropriate
    emotion_mapping = {
        'grief': 'sadness',
        'despair': 'sadness',
        'longing': 'sadness',
        'nostalgia': 'sadness',
        'relief': 'joy',
        'gratitude': 'joy',
        'contentment': 'joy',
        'excitement': 'joy',
        'hope': 'anticipation',
        'contempt': 'disgust',
        'envy': 'anger',
        'frustration': 'anger',
        'guilt': 'fear',
        'shame': 'fear',
        'uncertainty': 'fear',
        'awe': 'surprise'
    }
    
    # Keep detailed complex emotion but also provide base category
    result = {
        "dominant": dominant,
        "dominant_category": emotion_mapping.get(dominant, dominant),
        "counts": dict(counts),
        "complex_emotions": complex_emo,
        "all_scores": {**dict(counts), **complex_emo}  # Combined scores
    }
    
    # Add confidence metric
    if counts or complex_emo:
        total_emotion_words = sum(counts.values())
        complex_score = sum(complex_emo.values()) if complex_emo else 0
        result["confidence"] = min((total_emotion_words * 10 + complex_score * 50) / len(tokens), 100)
    else:
        result["confidence"] = 0
        result["note"] = "No emotion indicators detected."
    
    return result

# ============================================================================
# POS TAGGING (Heuristic)
# ============================================================================
def heuristic_pos_tag(token: str) -> str:
    """Very simple heuristic POS tagger for Marathi tokens."""
    if not token:
        return "X"
    if token.isdigit():
        return "NUM"
    if len(token) <= 2:
        return "PART"
    if token.endswith(("ने", "ला", "वर", "कडे", "च्या", "मध्ये", "साठी")):
        return "PP"
    if token.endswith(("ला", "ली", "ले", "तात", "त आहे", "त होते")):
        return "VERB"
    return "NOUN"

def analyze_pos(text: str):
    """Return POS tags for input text."""
    tokens = tokenize(text)
    tagged = [(tok, heuristic_pos_tag(tok)) for tok in tokens]
    pos_counts = Counter([tag for _, tag in tagged])
    return {"tagged": tagged, "counts": dict(pos_counts)}

# ============================================================================
# NAMED ENTITIES
# ============================================================================
def extract_entities(text: str):
    """Extract named entity candidates from text using lexicon."""
    tokens = tokenize(text)
    entities = [t for t in tokens if t in ENTITY_SET]
    entity_counts = Counter(entities)
    return {"entities": entities, "counts": dict(entity_counts)}

# ============================================================================
# TF-IDF ANALYSIS
# ============================================================================
def analyze_tfidf(text: str, top_n=10):
    """Return top TF-IDF terms for input text with robust fallback."""
    tokens = tokenize(text)
    
    # Try using trained vectorizer if available
    if TFIDF_VECTORIZER is not None:
        try:
            tfidf_matrix = TFIDF_VECTORIZER.transform([text])
            feature_names = np.array(TFIDF_VECTORIZER.get_feature_names_out())
            scores = tfidf_matrix.toarray()[0]
            
            # Get non-zero scores
            top_indices = scores.argsort()[::-1][:top_n]
            top_terms = feature_names[top_indices]
            top_scores = scores[top_indices]
            
            result = [(term, float(score)) for term, score in zip(top_terms, top_scores) if score > 0]
            
            if result:
                return {"top_terms": result}
        except Exception as e:
            pass  # Fall through to backup method
    
    # Fallback: compute simple TF-IDF manually
    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    stopword_set = STOPWORD_SET
    
    if total_tokens == 0:
        return {"top_terms": []}
    
    # Calculate TF and filter by relevance
    tf_scores = {}
    for term, count in token_counts.items():
        if term not in stopword_set and len(term) > 2:
            # Simple TF score with length bonus for longer words
            tf = count / total_tokens
            length_bonus = min(len(term) / 10.0, 0.5)
            tf_scores[term] = tf + length_bonus
    
    sorted_terms = sorted(tf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    return {
        "top_terms": sorted_terms,
        "note": "Using fallback TF analysis (some terms may not be in training vocabulary)"
    }

# ============================================================================
# LDA TOPIC MODELING
# ============================================================================
def analyze_lda(text: str):
    """Return LDA topic distribution for input text with robust fallback."""
    tokens = tokenize(text)
    
    if not tokens:
        return {"error": "No tokens found in text"}
    
    # Try using trained LDA model if available
    if LDA_MODEL is not None and COUNT_VECTORIZER is not None:
        try:
            doc_term_matrix = COUNT_VECTORIZER.transform([text])
            
            # Check if any features matched
            if doc_term_matrix.nnz == 0:
                # No words in vocabulary, use fallback
                raise ValueError("No vocabulary overlap")
            
            topic_dist = LDA_MODEL.transform(doc_term_matrix)[0]
            top_topic_idx = topic_dist.argmax()
            top_topic_prob = topic_dist[top_topic_idx]
            
            feature_names = np.array(COUNT_VECTORIZER.get_feature_names_out())
            topic_words = feature_names[LDA_MODEL.components_[top_topic_idx].argsort()[::-1][:10]]
            
            return {
                "topic_distribution": {f"Topic {i}": float(prob) for i, prob in enumerate(topic_dist)},
                "dominant_topic": int(top_topic_idx),
                "dominant_topic_prob": float(top_topic_prob),
                "dominant_topic_words": list(topic_words)
            }
        except Exception as e:
            pass  # Fall through to backup method
    
    # Fallback: analyze based on word characteristics
    token_counts = Counter(tokens)
    stopword_set = STOPWORD_SET
    entity_set = ENTITY_SET
    
    # Simple heuristic topic inference
    content_words = [t for t in tokens if t not in stopword_set and len(t) > 2]
    entity_words = [t for t in tokens if t in entity_set]
    
    # Determine pseudo-topic based on content
    has_entities = len(entity_words) > 0
    avg_word_length = sum(len(t) for t in content_words) / len(content_words) if content_words else 0
    unique_ratio = len(set(tokens)) / len(tokens) if tokens else 0
    
    # Create pseudo topic distribution
    n_topics = 5
    pseudo_dist = np.ones(n_topics) * 0.1  # baseline probability
    
    if has_entities:
        pseudo_dist[0] += 0.4  # Topic 0: Named Entity heavy
    if avg_word_length > 6:
        pseudo_dist[1] += 0.4  # Topic 1: Formal/technical
    if unique_ratio > 0.7:
        pseudo_dist[2] += 0.4  # Topic 2: Diverse vocabulary
    
    # Normalize
    pseudo_dist = pseudo_dist / pseudo_dist.sum()
    
    top_topic_idx = pseudo_dist.argmax()
    top_words = [term for term, _ in token_counts.most_common(10)]
    
    return {
        "topic_distribution": {f"Topic {i}": float(prob) for i, prob in enumerate(pseudo_dist)},
        "dominant_topic": int(top_topic_idx),
        "dominant_topic_prob": float(pseudo_dist[top_topic_idx]),
        "dominant_topic_words": top_words,
        "note": "Using fallback topic analysis (text has limited vocabulary overlap with training data)"
    }

# ============================================================================
# COMPLETE ANALYSIS
# ============================================================================
def analyze_text(text: str, marathi_only=True):
    """Run complete NLP analysis on input text with semantic features.
    
    Args:
        text: Input text string
        marathi_only: If True, analyze only Devanagari tokens (default: True)
    
    Returns:
        Dictionary with all analysis results
    """
    # Tokenize with Marathi-only filter
    tokens = tokenize(text, marathi_only=marathi_only)
    
    # Validate we have tokens
    if not tokens:
        return {
            "tokens": [],
            "token_count": 0,
            "sentiment": {"score": 0, "label": "neutral", "pos_words": 0, "neg_words": 0, "note": "No Marathi tokens found"},
            "emotion": {"dominant": "none", "counts": {}, "note": "No Marathi tokens found"},
            "pos": {"tagged": [], "counts": {}},
            "entities": [],
            "tfidf": {"top_terms": [], "note": "No tokens to analyze"},
            "lda": {"dominant_topic": None, "note": "No tokens to analyze"},
            "note": "Input contains no Marathi (Devanagari) text"
        }
    
    analysis = {
        "tokens": tokens,
        "token_count": len(tokens),
        "sentiment": analyze_sentiment(text),
        "emotion": analyze_emotion(text),
        "pos": analyze_pos(text),
        "entities": extract_entities(text),
        "tfidf": analyze_tfidf(text, top_n=15),
        "lda": analyze_lda(text)
    }
    
    # Add semantic analysis if available
    if SEMANTIC_AVAILABLE:
        try:
            analysis["semantic"] = get_semantic_summary(tokens, text)
        except Exception as e:
            analysis["semantic"] = {"error": f"Semantic analysis failed: {str(e)}"}
    
    return analysis
