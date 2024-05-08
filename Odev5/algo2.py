import re
import math

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def tokenize(text):
    return text.split()

def count_words(tokens):
    word_counts = {}
    for token in tokens:
        word_counts[token] = word_counts.get(token, 0) + 1
    return word_counts

def cosine_similarity(vec1, vec2):
    dot_product = sum(vec1[key] * vec2.get(key, 0) for key in vec1)
    magnitude1 = math.sqrt(sum(vec1[key] ** 2 for key in vec1))
    magnitude2 = math.sqrt(sum(vec2[key] ** 2 for key in vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

def text_similarity(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    
    word_counts1 = count_words(tokens1)
    word_counts2 = count_words(tokens2)
    
    similarity = cosine_similarity(word_counts1, word_counts2)
    return similarity
