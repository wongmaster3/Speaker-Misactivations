import argparse
import time
from itertools import chain, islice, product, tee
from tqdm import tqdm


def get_defaults(parser):
    args = parser.parse_args()
    return {key: parser.get_default(key) for key in vars(args)}


def get_generation_arg_parser():
    parser = argparse.ArgumentParser(description='Generate and play a sequence of spoken audio.')
    parser.add_argument('--filename', '-f', default='./cache/google-10000-english-no-swears.txt',
                        help='path to text file containing text per line')
    parser.add_argument('--lang', default='en',
                        help='language to use for speech')
    parser.add_argument('--tld', default='com',
                        help='top level domain (of Google) for language variants')
    parser.add_argument('--repeat', '-r', type=int, default=1,
                        help='number of times to repeat the sequence')
    parser.add_argument('--start', '-s', type=int, default=0,
                        help='index to start playing the sequence at')
    parser.add_argument('--end', type=int, default=None,
                        help='index to stop playing segments')
    parser.add_argument('--delay', '-d', type=float, default=3.0,
                        help='(additional) delay (in seconds) between playing each segment')
    
    parser.add_argument('--has-prefix', action='store_true',
                        help='switch for when the audio list uses prefix ids')
    parser.add_argument('--name', default='common',
                        help='name of the dataset')
    
    return parser


def eachline(filename='./cache/google-10000-english-no-swears.txt', has_prefix=False):
    with open(filename) as f:
        for line in f:
            word = line.strip()
            
            if has_prefix:
                yield word.partition(':')[0:3:2]
            else:
                yield word


def prefixed_speech(text, identifier, lang='en', tld='com', name='common'):
    from gtts import gTTS

    tts_request = gTTS(text=text, lang=lang, tld=tld)
    tts_request.save(f'temp/{name}-{lang}.{tld}/{identifier}.mp3')


def generated_sequence(config):
    seq1, seq2 = tee(eachline(config.filename, config.has_prefix), 2)
    first_sequence = islice(((line,) for line in seq1), config.start, config.end)
    remaining_sequences = product(islice(seq2, config.start, config.end), repeat=config.repeat)
    full_sequence = chain(first_sequence, remaining_sequences)
    
    for word, in full_sequence:
        yield word


if __name__ == '__main__':
    config = get_generation_arg_parser().parse_args()
    
    for word in tqdm(generated_sequence(config)):
        if config.has_prefix:
            prefixed_speech(word[1], word[0], lang=config.lang, tld=config.tld, name=config.name)
        else:
            prefixed_speech(word, word, lang=config.lang, tld=config.tld, name=config.name)
        time.sleep(config.delay)

