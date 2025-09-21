import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download required NLTK data with better error handling
def _download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading punkt_tab...")
        nltk.download('punkt_tab')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading stopwords...")
        nltk.download('stopwords')
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    except LookupError:
        print("Downloading averaged_perceptron_tagger_eng...")
        nltk.download('averaged_perceptron_tagger_eng')

# Try to initialize NLTK, fallback to simple extraction if it fails
try:
    _download_nltk_data()
    NLTK_AVAILABLE = True
except Exception as e:
    print(f"NLTK initialization failed: {e}")
    print("Falling back to simple keyword extraction")
    NLTK_AVAILABLE = False

def extract_keywords(text: str, top_n: int = 3):
    if not text.strip():
        return []

    if NLTK_AVAILABLE:
        # Use NLTK if available
        try:
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalpha()]
            tagged = nltk.pos_tag(words)
            nouns = [word for word, pos in tagged if pos.startswith("NN")]
            nouns = [w for w in nouns if w not in stopwords.words("english")]
            freq = Counter(nouns)
            return [word for word, _ in freq.most_common(top_n)]
        except Exception as e:
            print(f"NLTK processing failed: {e}, falling back to simple extraction")
            # Fall through to simple extraction
    
    # Simple fallback extraction (no NLTK required)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    stopwords_simple = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'man', 'men', 'put', 'say', 'she', 'too', 'use'}
    words = [w for w in words if w not in stopwords_simple and len(w) > 3]
    freq = Counter(words)
    return [word for word, _ in freq.most_common(top_n)]
