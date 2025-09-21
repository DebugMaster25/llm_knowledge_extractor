import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
def _download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')

# Initialize NLTK data
_download_nltk_data()

def extract_keywords(text: str, top_n: int = 3):
    if not text.strip():
        return []

    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha()]
    tagged = nltk.pos_tag(words)
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    nouns = [w for w in nouns if w not in stopwords.words("english")]
    freq = Counter(nouns)
    return [word for word, _ in freq.most_common(top_n)]
