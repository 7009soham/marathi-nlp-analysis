"""
Semantic Analysis Module
Advanced semantic features for Marathi text analysis.
"""

from collections import Counter
import regex as re

# ============================================================================
# SEMANTIC PATTERNS
# ============================================================================

def analyze_semantic_features(tokens, text):
    """Analyze semantic features of the text."""
    features = {}
    
    # 1. Formality Detection
    formal_markers = {'कृपया', 'धन्यवाद', 'नमस्कार', 'आदरपूर्वक', 'विनंती'}
    informal_markers = {'अरे', 'काय', 'बाबा', 'रे', 'यार'}
    
    formal_count = sum(1 for t in tokens if t in formal_markers)
    informal_count = sum(1 for t in tokens if t in informal_markers)
    
    if formal_count > informal_count:
        features['formality'] = 'formal'
        features['formality_score'] = min(formal_count / len(tokens) * 10, 1.0)
    elif informal_count > formal_count:
        features['formality'] = 'informal'
        features['formality_score'] = min(informal_count / len(tokens) * 10, 1.0)
    else:
        features['formality'] = 'neutral'
        features['formality_score'] = 0.5
    
    # 2. Politeness Level
    polite_markers = {'कृपया', 'नम्रतेने', 'आपण', 'तुम्ही'}
    impolite_markers = {'तू', 'तुझा', 'तुझे'}
    
    polite_count = sum(1 for t in tokens if t in polite_markers)
    impolite_count = sum(1 for t in tokens if t in impolite_markers)
    
    if polite_count > 0:
        features['politeness'] = 'polite'
    elif impolite_count > 0:
        features['politeness'] = 'casual/direct'
    else:
        features['politeness'] = 'neutral'
    
    # 3. Temporal References
    past_markers = {'होते', 'होती', 'होता', 'झाले', 'केले', 'गेले'}
    present_markers = {'आहे', 'आहेत', 'आहोत', 'करतो', 'करते', 'होतो'}
    future_markers = {'होईल', 'होणार', 'करणार', 'जाईल', 'येईल'}
    
    has_past = any(t in past_markers for t in tokens)
    has_present = any(t in present_markers for t in tokens)
    has_future = any(t in future_markers for t in tokens)
    
    time_refs = []
    if has_past: time_refs.append('past')
    if has_present: time_refs.append('present')
    if has_future: time_refs.append('future')
    
    features['temporal_references'] = time_refs if time_refs else ['unspecified']
    
    # 4. Causality Detection
    causal_markers = {'कारण', 'म्हणून', 'त्यामुळे', 'त्यासाठी', 'ने'}
    features['has_causality'] = any(t in causal_markers for t in tokens)
    
    # 5. Comparison/Contrast
    comparison_markers = {'पण', 'परंतु', 'किंवा', 'अथवा', 'तरी'}
    features['has_contrast'] = any(t in comparison_markers for t in tokens)
    
    # 6. Certainty/Uncertainty
    certain_markers = {'नक्कीच', 'खरच', 'अवश्य', 'निश्चित'}
    uncertain_markers = {'कदाचित', 'शक्यतो', 'बहुधा', 'कधी'}
    
    if any(t in certain_markers for t in tokens):
        features['certainty'] = 'high'
    elif any(t in uncertain_markers for t in tokens):
        features['certainty'] = 'low'
    else:
        features['certainty'] = 'medium'
    
    # 7. Action vs State
    action_verbs = {'करणे', 'जाणे', 'येणे', 'खाणे', 'पिणे', 'बोलणे', 'लिहिणे'}
    state_verbs = {'असणे', 'राहणे', 'दिसणे', 'वाटणे'}
    
    action_count = sum(1 for t in tokens if any(av in t for av in action_verbs))
    state_count = sum(1 for t in tokens if any(sv in t for sv in state_verbs))
    
    if action_count > state_count:
        features['verb_type'] = 'action-oriented'
    elif state_count > action_count:
        features['verb_type'] = 'state-oriented'
    else:
        features['verb_type'] = 'balanced'
    
    # 8. Complexity Metrics
    avg_word_length = sum(len(t) for t in tokens) / len(tokens) if tokens else 0
    unique_ratio = len(set(tokens)) / len(tokens) if tokens else 0
    
    features['lexical_diversity'] = round(unique_ratio, 2)
    features['avg_word_length'] = round(avg_word_length, 2)
    
    if avg_word_length > 6 and unique_ratio > 0.7:
        features['complexity'] = 'high'
    elif avg_word_length < 4 and unique_ratio < 0.5:
        features['complexity'] = 'low'
    else:
        features['complexity'] = 'medium'
    
    return features

def analyze_discourse_markers(tokens):
    """Analyze discourse structure markers."""
    discourse = {}
    
    # Topic introduction
    intro_markers = {'पहिले', 'सुरुवातीला', 'प्रथम', 'आधी'}
    discourse['has_introduction'] = any(t in intro_markers for t in tokens)
    
    # Conclusion markers
    conclusion_markers = {'शेवटी', 'अखेर', 'निष्कर्ष', 'सारांश'}
    discourse['has_conclusion'] = any(t in conclusion_markers for t in tokens)
    
    # Elaboration
    elaboration_markers = {'म्हणजेच', 'उदाहरणार्थ', 'अर्थात', 'तसेच'}
    discourse['has_elaboration'] = any(t in elaboration_markers for t in tokens)
    
    # Addition
    addition_markers = {'आणि', 'तसेच', 'सुद्धा', 'व'}
    discourse['has_addition'] = sum(1 for t in tokens if t in addition_markers)
    
    # Contrast
    contrast_markers = {'पण', 'परंतु', 'मात्र', 'तरी'}
    discourse['has_contrast'] = sum(1 for t in tokens if t in contrast_markers)
    
    return discourse

def detect_speech_acts(tokens, text):
    """Detect the primary speech act (assertive, directive, commissive, expressive, declarative)."""
    speech_acts = []
    
    # Question (Directive - seeking information)
    if '?' in text or any(q in tokens for q in ['का', 'काय', 'कसे', 'कुठे', 'केव्हा', 'कोण']):
        speech_acts.append('interrogative')
    
    # Command/Request (Directive)
    imperative_markers = {'करा', 'जा', 'ये', 'बोला', 'घ्या', 'दे'}
    if any(t in imperative_markers for t in tokens):
        speech_acts.append('directive')
    
    # Statement (Assertive)
    if any(t in tokens for t in ['आहे', 'आहेत', 'होते', 'होती']):
        speech_acts.append('assertive')
    
    # Expression of feeling (Expressive)
    expressive_markers = {'वाह', 'अरे', 'अहो', 'हाय', 'धन्यवाद', 'क्षमा'}
    if any(t in expressive_markers for t in tokens):
        speech_acts.append('expressive')
    
    return speech_acts if speech_acts else ['unclassified']

def analyze_semantic_relations(tokens):
    """Identify semantic relations between concepts."""
    relations = []
    
    # Possession
    possession_markers = {'चा', 'ची', 'चे', 'च्या', 'माझा', 'तुझा', 'त्याचा'}
    if any(t in possession_markers for t in tokens):
        relations.append('possession')
    
    # Location
    location_markers = {'येथे', 'तेथे', 'मध्ये', 'वर', 'खाली', 'पुढे', 'मागे'}
    if any(t in location_markers for t in tokens):
        relations.append('location')
    
    # Time
    time_markers = {'आता', 'मग', 'नंतर', 'आधी', 'तेव्हा', 'सध्या'}
    if any(t in time_markers for t in tokens):
        relations.append('temporal')
    
    # Comparison
    comparison_markers = {'सारखा', 'पेक्षा', 'जास्त', 'कमी', 'समान'}
    if any(t in comparison_markers for t in tokens):
        relations.append('comparison')
    
    return relations if relations else ['none']

def get_semantic_summary(tokens, text):
    """Generate comprehensive semantic analysis summary."""
    return {
        'features': analyze_semantic_features(tokens, text),
        'discourse': analyze_discourse_markers(tokens),
        'speech_acts': detect_speech_acts(tokens, text),
        'semantic_relations': analyze_semantic_relations(tokens)
    }
