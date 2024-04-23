import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# Obtengo los tokens de la oración
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Recupero la forma 'base' de la palabra
def stem(word):
    return stemmer.stem(word.lower())

# Creo un array de palabras
# Si la palabra existe en la oración, se le asigna 1, de lo contrario 0
def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1
    return bag
