import argparse
import itertools
import random
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import Laplace
from nltk.tokenize.treebank import TreebankWordDetokenizer

detokenize = TreebankWordDetokenizer().detokenize


def get_ngram_generation_parser():
    parser = argparse.ArgumentParser(description='Generate words using a n-gram model built with a text '
                                                 'source')
    
    parser.add_argument('filename',
                        help='filename of the source text for creating the n-gram model')
    parser.add_argument('sentences', type=int,
                        help='number of sentences to generate')
    
    parser.add_argument('--output-filename', '-f', default='sentences.txt',
                        help='filename to output the list of generated sentences')
    parser.add_argument('--order', '-o', type=int, default=3,
                        help='max order of the n-grams (e.g. 3 will use up to tri-grams)')
    parser.add_argument('--max-words', '-m', default=25,
                        help='maximum number of words per sentence')
    
    return parser


def random_prefix():
    return '%010x' % random.randrange(16**10)


class NGramSentences:
    
    def __init__(self, n=3, filename='cache/book.txt'):
        with open(filename) as file:
            text = file.read()
        
        tokens = [list(map(str.lower, word_tokenize(sent))) for sent in sent_tokenize(text)]
        train, vocab = padded_everygram_pipeline(3, tokens)
        
        self.model = Laplace(n)
        self.model.fit(train, vocab)
    
    def generate(self, prev_word='<s>', max_words=25):
        return detokenize(list(itertools.takewhile(
                lambda word: word != '</s>',
                itertools.dropwhile(
                        lambda word: word == '<s>',
                        (word for word in self.model.generate(max_words, text_seed=[prev_word]))))))


if __name__ == '__main__':
    config = get_ngram_generation_parser().parse_args()
    
    print(f'Creating the {config.order}-gram model from {config.filename}...')
    gen = NGramSentences(n=config.order, filename=config.filename)
    
    print(f'Generating {config.sentences} sentences...')
    with open(config.output_filename, 'w', buffering=1) as f:
        for _ in range(config.sentences):
            sentence = gen.generate(max_words=config.max_words)
            f.write(f'{random_prefix()}:{sentence}\n')

