import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Ensure NLTK packages are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

ps = PorterStemmer()

def clean_text(text):
    """
    Standard text normalization pipeline.
    Lowercases text, removes punctuation, and normalizes whitespace.
    """
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Strip punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def transform_text(text):
    """
    Advanced NLP text preprocessing.
    Matches the exact training pipeline: tokenization, alphanumeric filtering,
    English stopword exclusion, and Porter stemming.
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Tokenization
    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        # Fallback if nltk tokenization fails
        tokens = text.split()
        
    # Keep only alphanumeric tokens
    y = [token for token in tokens if token.isalnum()]
    
    # Filter English stopwords and punctuation
    try:
        stop_words = set(stopwords.words('english'))
    except Exception:
        stop_words = set()
        
    filtered = [token for token in y if token not in stop_words and token not in string.punctuation]
    
    # Apply Porter stemming
    stemmed = [ps.stem(token) for token in filtered]
    
    return " ".join(stemmed)
