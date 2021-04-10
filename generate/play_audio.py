import argparse
import numpy as np
import os
import pydub
import simpleaudio as sa
import time


def get_play_parser():
    parser = argparse.ArgumentParser(description='Play audio from a directory')
    parser.add_argument('dir', help='source directory of audio files')

    return parser


def read(f, normalized=False):
    """MP3 to numpy array"""
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y


def play_array(array, bitrate):
    player = sa.play_buffer(array, 1, 2, bitrate)
    player.wait_done()


if __name__ == '__main__':
    config = get_play_parser().parse_args()
    root, _, filenames = next(os.walk(config.dir))
    for filename in filenames:
        filepath = os.path.join(root, filename)
        bitrate, audio = read(filepath)
        
        start_time = time.time()
        play_array(audio, bitrate)
        end_time = time.time()
        
        text = filename.split('.')[0]
        print(f'{text},{start_time},{end_time}')



