import argparse
import numpy as np
import pydub
import simpleaudio as sa


class AudioPlayer:
    def __init__(self):
        pass


def get_play_parser():
    parser = argparse.ArgumentParser(description='Play audio from a directory')
    parser.add_argument('dir', help='source directory of audio files')
    parser.add_argument('--device_name', '-n', default='output',
                        help='name of device under test')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                        help='(additional) delay (in seconds) between playing each segment')
    parser.add_argument('--experiment', '-e', default='test',
                    help='name of experiment')
    parser.add_argument('--trial', '-t', type=int, default=1,
                    help='trial number of experiment')
    parser.add_argument('--questions', '-q', action='store_true',
                    help='determine whether to ask questions or not after misactivation')

    return parser


def read(f, normalized=False):
    """MP3 filename to numpy array"""
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


