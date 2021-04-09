import argparse
import io
import time
from itertools import chain, islice, product, tee
import pandas as pd

import pyglet
from gtts import gTTS

pyglet.options["audio"] = ("pulse",)


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
    parser.add_argument('--delay', '-d', type=float, default=0.0,
                        help='(additional) delay (in seconds) between playing each segment')
    
    return parser


def common_words(filename='./cache/google-10000-english-no-swears.txt'):
    with open(filename) as f:
        for line in f:
            word = line.strip()
            yield word


def speech(text, lang='en', tld='com'):
    with io.BytesIO() as f:
        gTTS(text=text, lang=lang, tld=tld).write_to_fp(f)
        f.seek(0)

        player = pyglet.media.load('_.mp3', file=f).play()
        while player.playing:
            pyglet.app.platform_event_loop.dispatch_posted_events()
            pyglet.clock.tick()


def generate_multiple(config):
    seq1, seq2 = tee(common_words(config.filename), 2)
    first_sequence = islice(((line,) for line in seq1), config.start, config.end)
    remaining_sequences = product(islice(seq2, config.start, config.end), repeat=config.repeat)
    full_sequence = chain(first_sequence, remaining_sequences)
    
    for word, in full_sequence:
        speech(word, lang=config.lang, tld=config.tld)
        time.sleep(config.delay)


if __name__ == '__main__':
    config = get_generation_arg_parser().parse_args()
    
    generate_multiple(config)

