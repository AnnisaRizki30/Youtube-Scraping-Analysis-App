# NLP
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
import string 
import re
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Data Manipulation
import pandas as pd
import numpy as np
import itertools


# Create Stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ----------------Get stopword from NLTK stopword ---------
# Get Indonesian stopword
list_stopwords = stopwords.words('indonesian')
# ------------------ Adding stopword manually ----------
# Added words to delete
list_stopwords.extend(['yg', 'dg', 'rt', 'dgn', 'ny', 'd', 'klo', 'kalo', 'amp', 'biar', 'bikin', 'bilang',
                    'krn', 'nya', 'nih', 'sih', 'tidak', 'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 'jd', 
                    'jgn', 'sdh', 'aja', 'n', 't', 'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', '&amp', 'yah', 
                    'bgt', 'hahaha', 'jg', 'ng', 'kurang', 'wkwk', 'wkwkwk', 'wkwkwkwk','pasu','dip', 'byang', 
                    'bang', 'bu', 'ku', 'banget'])

# Convert list into stopwords dictionary
list_stopwords = set(list_stopwords)
# Delete word 'baik' in stopwords dictionary list
list_stopwords.remove('baik')


def text_preprocessing(text): 
    text = text.lower()
    text = remove_text_special(text)
    text = remove_number(text)
    text = remove_punctuation(text)
    text = remove_singl_char(text)
    text = remove_duplicate_words(text)
    text = remove_emoji(text)

    # Tokenizing
    tokens = word_tokenize(text)

    slang_word = convert_slang_word_term(tokens)
    negation = negation_handling(slang_word)

    # # Removing stop words
    stopwords = [token for token in negation if token not in list_stopwords]

    # Stemming
    stemmed_tokens = [stemmer.stem(token) for token in stopwords]
    return " ".join(stemmed_tokens).strip()

# Remove special text
def remove_text_special(text):
    # Remove space
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
    # Remove mention, tag, link, and hastag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
    # Remove non-ascii characters from the string
    text = re.sub(r'[^\x00-\x7f]',r'', text)
    # Remove url uncomplete
    return text.replace("http://", " ").replace("https://", " ")

# Remove number
def remove_number(text):
    return  re.sub(r"\d+", "", text)

# Remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("","",string.punctuation))

# Remove single character
def remove_singl_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)

# Remove duplicate words
def remove_duplicate_words(text):
    return  ''.join(ch for ch, _ in itertools.groupby(text))

# Remove emoticon
def remove_emoji(text):
    emoji_pattern = re.compile("["
                        u"\U0001F600-\U0001F64F"  # emoticons
                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        u"\U00002500-\U00002BEF"  # chinese char
                        u"\U00002702-\U000027B0"
                        u"\U00002702-\U000027B0"
                        u"\U000024C2-\U0001F251"
                        u"\U0001f926-\U0001f937"
                        u"\U00010000-\U0010ffff"
                        u"\u2640-\u2642"
                        u"\u2600-\u2B55"
                        u"\u200d"
                        u"\u23cf"
                        u"\u23e9"
                        u"\u231a"
                        u"\ufe0f"  # dingbats
                        u"\u3030"
                        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


# Read slang vocabulary dictionary
convert_slang_word = pd.read_csv("C:\\Users\\Annisa Rizki\\Desktop\\Annisa Lianda\\Job Freelance\\Ytb-Scraping-Analysis\\data\\new_kamusalay.csv") 

# Create a variable in the form of a dictionary that will store the results of convert slang word function
convert_slang_word_dict = {}

for index, row in convert_slang_word.iterrows():
    if row[0] not in convert_slang_word_dict:
        convert_slang_word_dict[row[0]] = row[1] 

# Function for convert slang word
def convert_slang_word_term(document):
    return [convert_slang_word_dict[term] if term in convert_slang_word_dict else term for term in document]


# Function for do negation handling
def negation_handling(text):
    negation_text = []
    for i in range(len(text)):
        word = text[i]
        if text[i-1] not in ['ga', 'tidak', 'kurang', 'gak', 'enggak', 'nggak', 'tak']:
            negation_text.append(word)
        else:
            word = "%s_%s" %(text[i-1],word)
            negation_text.append(word)
    return negation_text
