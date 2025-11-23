import numpy as np
import language_tool_python
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import spacy

nlp = spacy.load("en_core_web_sm")
sentiment_pipeline = pipeline("sentiment-analysis")


def word_tokens(text: str) -> list[str]:
    doc = nlp(text)
    return [token.text for token in doc]


def salutation_score(text: str) -> int:
    sentences = text.split('.')
    if not sentences:
        return 0
    first_sentence = sentences[0].lower().strip()
    excellent_indicators = ['excited', 'thrilled', 'pleasure', 'delighted', 'great', 'happy', 'wonderful']
    good_indicators = ['good morning', 'good afternoon', 'good evening', 'good day', 'everyone', 'everybody']
    basic_indicators = ['hi', 'hello', 'hey']
    if any(word in first_sentence for word in excellent_indicators):
        return 5
    if any(phrase in first_sentence for phrase in good_indicators):
        return 4
    if any(first_sentence.startswith(word) for word in basic_indicators):
        return 2
    return 0


def keyword_score(text: str):
    text_lower = text.lower()
    must_have_categories = {
        'name': ['my name is', 'i am', "i'm", 'myself', 'called', 'this is'],
        'age': ['years old', 'age', 'aged', 'i am', "i'm", 'turn'],
        'school_class': ['school', 'class', 'grade', 'student', 'studying', 'college', 'university'],
        'family': ['family', 'mother', 'father', 'parents', 'mom', 'dad', 'sister', 'brother', 'siblings'],
        'hobbies': ['hobby', 'hobbies', 'interest', 'interests', 'like to', 'enjoy', 'love to', 'free time']
    }
    good_to_have_categories = {
        'family_details': ['live with', 'family members', 'we have', 'together', 'household'],
        'origin': ['from', 'origin', 'born in', 'grew up', 'hometown', 'city', 'country'],
        'goals': ['goal', 'dream', 'aspire', 'want to', 'hope to', 'future', 'become', 'ambition'],
        'fun_fact': ['fun fact', 'interesting', 'unique', 'something about me', 'did you know'],
        'strengths': ['strength', 'good at', 'talent', 'skill', 'achievement', 'proud of', 'excel']
    }
    score = 0
    found = {'must_have': [], 'good_to_have': []}
    for category, keywords in must_have_categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                score += 4
                found['must_have'].append(category)
                break
    for category, keywords in good_to_have_categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                score += 2
                found['good_to_have'].append(category)
                break
    return min(score, 30), found


def flow_score(text: str) -> int:
    sentences = [s.strip().lower() for s in text.split('.') if s.strip()]
    if len(sentences) < 3:
        return 0
    sal_score = salutation_score(sentences[0])
    basic_text = " ".join(sentences[1:-2])
    basic_score = keyword_score(basic_text)[0]
    closing_words = ["thank you", "have a nice day", "take care", "good bye",
                     "that's all for now", "we'll stop here", "let's conclude",
                     "we're done", "that covers everything"]
    last_sentences = " ".join(sentences[-2:])
    if sal_score != 0 and basic_score != 0 and any(word in last_sentences for word in closing_words):
        return 5
    return 0


def grammar_errors(text: str) -> int:
    tool = language_tool_python.LanguageTool("en-US")
    matches = tool.check(text)
    errors = len(matches)
    score = max(0, 1 - errors / 10)
    if score > 0.9:
        return 10
    elif score >= 0.7:
        return 8
    elif score >= 0.5:
        return 6
    elif score >= 0.3:
        return 4
    else:
        return 2


def type_token_ratio(text: str) -> int:
    words = word_tokens(text)
    if not words:
        return 2
    total_words = len(words)
    distinct_words = len(set([w.lower() for w in words]))
    result = distinct_words / total_words
    if result > 0.9:
        return 10
    elif result >= 0.7:
        return 8
    elif result >= 0.5:
        return 6
    elif result >= 0.3:
        return 4
    else:
        return 2


def fillerwords_score(text: str) -> int:
    filler_words = ["um", "like", "uh", "er", "ahh", "ah", "hmm", "mm",
                    "basically", "actually", "you know", "kind of", "sort of"]
    words = word_tokens(text.lower())
    total = len(words)
    if total == 0:
        return 15
    count = sum(1 for w in words if w in filler_words)
    ratio = (count / total) * 100
    if ratio <= 3:
        return 15
    elif ratio <= 6:
        return 12
    elif ratio <= 9:
        return 9
    elif ratio <= 12:
        return 6
    else:
        return 3


def sentiment_score(text: str) -> int:
    result = sentiment_pipeline(text)[0]
    score = result["score"]
    if score >= 0.9:
        return 15
    elif score >= 0.7:
        return 12
    elif score >= 0.5:
        return 9
    elif score >= 0.3:
        return 6
    else:
        return 3


def speech_rate(text: str, duration: int = 60) -> int:
    words = word_tokens(text)
    minutes = max(duration / 60, 0.1)
    wpm = len(words) / minutes
    if wpm >= 161:
        return 2
    elif wpm >= 141:
        return 6
    elif wpm >= 111:
        return 10
    elif wpm >= 81:
        return 6
    else:
        return 2


def total_score(text: str, duration: int = 60):
    sal_score = salutation_score(text)
    key_score, found = keyword_score(text)
    flow = flow_score(text)
    speech = speech_rate(text, duration)
    grammar = grammar_errors(text)
    ttr = type_token_ratio(text)
    filler = fillerwords_score(text)
    sent_score = sentiment_score(text)
    total = sal_score + key_score + flow + speech + grammar + ttr + filler + sent_score
    return total, sal_score, key_score, flow, speech, grammar, ttr, filler, sent_score
