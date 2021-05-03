import itertools
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import Laplace


class NGramSentences:
    
    def __init__(self, n=3, filename='cache/booktext.txt'):
        with open(filename) as file:
            text = file.read()
        
        tokens = [list(map(str.lower, word_tokenize(sent))) for sent in sent_tokenize(text)]
        train, vocab = padded_everygram_pipeline(3, tokens)
        
        self.model = Laplace(3)
        self.model.fit(train, vocab)
    
    def generate(self, prev_word='<s>', max_words=25):
        return itertools.takewhile(
                lambda word: word != '</s>',
                itertools.dropwhile(
                        lambda word: word == '<s>',
                        (word for word in self.model.generate(max_words, text_seed=[prev_word]))))


gen = NGramSentences(8)
