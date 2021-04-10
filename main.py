import os
from generate.play_audio import *
from detection.light import *

if __name__ == '__main__':
    config = get_play_parser().parse_args()
    root, _, filenames = next(os.walk(config.dir))
    for filename in filenames:
        filepath = os.path.join(root, filename)
        bitrate, audio = read(filepath)
        
        log(filename, play_array, audio, bitrate)
