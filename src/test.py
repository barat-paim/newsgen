import nltk
from nltk.tokenize import sent_tokenize

nltk.download('punkt')

text = "This is a test sentence. We want to see if NLTK is working properly."
sentences = sent_tokenize(text)
print(sentences)