"""
Test script to validate sentiment and emotion detection accuracy
"""

from marathi_nlp_core import analyze_sentiment, analyze_emotion, tokenize

# Test cases with expected results
test_cases = [
    {
        "text": "तो माझा जिवलग मित्र होता. त्याच्या जाण्याने खूप वाईट वाटते.",
        "expected_sentiment": "negative",
        "expected_emotion": ["grief", "sadness"],
        "description": "Grief about friend passing away"
    },
    {
        "text": "हे खूप छान आहे! मला आवडले.",
        "expected_sentiment": "positive",
        "expected_emotion": ["joy"],
        "description": "Strong positive with intensifier"
    },
    {
        "text": "मला नाही आवडत. खूप वाईट आहे.",
        "expected_sentiment": "negative",
        "expected_emotion": ["disgust", "anger"],
        "description": "Negation with negative sentiment"
    },
    {
        "text": "कदाचित हे चांगले असेल, पण नक्की नाही.",
        "expected_sentiment": "neutral",
        "expected_emotion": ["uncertainty", "hope"],
        "description": "Mixed with uncertainty"
    },
    {
        "text": "मी खूप खुश आहे! आज सर्वात आनंदी दिवस आहे.",
        "expected_sentiment": "positive",
        "expected_emotion": ["joy"],
        "description": "Very happy - double positive"
    },
    {
        "text": "तुम्हाला लाज वाटली पाहिजे. काय केलेत तुम्ही?",
        "expected_sentiment": "negative",
        "expected_emotion": ["shame", "contempt"],
        "description": "Shame with contempt question"
    },
    {
        "text": "मला तुझा खूप अभिमान वाटतो. तू यशस्वी झालास.",
        "expected_sentiment": "positive",
        "expected_emotion": ["pride", "joy"],
        "description": "Pride in achievement"
    },
    {
        "text": "जुन्या दिवसांची आठवण येते.",
        "expected_sentiment": "neutral",
        "expected_emotion": ["nostalgia"],
        "description": "Nostalgia for old days"
    },
    {
        "text": "मी घाबरलो आहे. भयंकर परिस्थिती आहे.",
        "expected_sentiment": "negative",
        "expected_emotion": ["fear"],
        "description": "Fear situation"
    },
    {
        "text": "आभार! तुमची खूप मदत झाली.",
        "expected_sentiment": "positive",
        "expected_emotion": ["gratitude", "joy"],
        "description": "Gratitude expression"
    }
]

def test_detection():
    """Run tests and report accuracy"""
    import sys
    import io
    
    # Fix Unicode output on Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 80)
    print("MARATHI NLP ACCURACY TEST")
    print("=" * 80)
    print()
    
    correct_sentiment = 0
    correct_emotion = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"TEST {i}: {test['description']}")
        print(f"{'─' * 80}")
        print(f"📝 Text: {test['text']}")
        print()
        
        # Tokenize
        tokens = tokenize(test['text'])
        print(f"🔤 Tokens ({len(tokens)}): {', '.join(tokens)}")
        print()
        
        # Sentiment
        sentiment = analyze_sentiment(test['text'])
        print(f"💭 SENTIMENT ANALYSIS:")
        print(f"   Expected: {test['expected_sentiment'].upper()}")
        print(f"   Detected: {sentiment['label'].upper()}")
        print(f"   Score: {sentiment['score']:.1f}")
        print(f"   Positive words: {sentiment['pos_words']}")
        print(f"   Negative words: {sentiment['neg_words']}")
        
        sentiment_correct = (sentiment['label'] == test['expected_sentiment'] or 
                            (test['expected_sentiment'] == 'neutral' and abs(sentiment['score']) < 2))
        
        if sentiment_correct:
            print(f"   ✅ CORRECT")
            correct_sentiment += 1
        else:
            print(f"   ❌ INCORRECT")
        print()
        
        # Emotion
        emotion = analyze_emotion(test['text'])
        print(f"😊 EMOTION ANALYSIS:")
        print(f"   Expected: {', '.join(test['expected_emotion'])}")
        print(f"   Detected: {emotion['dominant']} (category: {emotion.get('dominant_category', 'none')})")
        print(f"   Confidence: {emotion.get('confidence', 0):.1f}%")
        
        if emotion.get('complex_emotions'):
            print(f"   Complex emotions: {', '.join(f'{k}={v:.2f}' for k, v in emotion['complex_emotions'].items())}")
        
        if emotion.get('counts'):
            print(f"   Basic emotions: {dict(emotion['counts'])}")
        
        emotion_correct = (emotion['dominant'] in test['expected_emotion'] or 
                          emotion.get('dominant_category') in test['expected_emotion'])
        
        if emotion_correct:
            print(f"   ✅ CORRECT")
            correct_emotion += 1
        else:
            print(f"   ❌ INCORRECT")
    
    # Summary
    print()
    print("=" * 80)
    print("📊 RESULTS SUMMARY")
    print("=" * 80)
    print(f"Sentiment Accuracy: {correct_sentiment}/{total} ({correct_sentiment/total*100:.1f}%)")
    print(f"Emotion Accuracy:   {correct_emotion}/{total} ({correct_emotion/total*100:.1f}%)")
    print(f"Overall Accuracy:   {(correct_sentiment+correct_emotion)/(total*2)*100:.1f}%")
    print()
    
    if (correct_sentiment + correct_emotion) / (total * 2) >= 0.8:
        print("✅ EXCELLENT! Detection accuracy is good (≥80%)")
    elif (correct_sentiment + correct_emotion) / (total * 2) >= 0.6:
        print("⚠️  ACCEPTABLE: Detection accuracy is okay (≥60%)")
    else:
        print("❌ NEEDS IMPROVEMENT: Detection accuracy is low (<60%)")
    print()

if __name__ == "__main__":
    test_detection()
