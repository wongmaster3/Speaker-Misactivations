import multiprocessing
import os
import time
from generate.play_audio import *
from detection.light import *

config = get_play_parser().parse_args()
delay_between_words = config.delay
light_file = open("./logs/" + config.device_name.lower() + "_light_activations.csv", "w")
light_file.write('start_time,end_time\n')
word_file = open("./logs/" + config.device_name.lower() + "_word_generations.csv", "w")
word_file.write('word,start_time,end_time\n')
generation_active_state = True

def log_activations():
    while generation_active_state:
        log(light_file)
    light_file.close()

def generate_audio():
    root, _, filenames = next(os.walk(config.dir))
    for filename in filenames:
        filepath = os.path.join(root, filename)
        bitrate, audio = read(filepath)
        
        # Play sound here
        text = filename.split('.')[0]
        start_time = str(time.time())
        play_array(audio, bitrate)
        end_time = str(time.time())
        word_file.write(f'{text},{start_time},{end_time}\n')
        time.sleep(delay_between_words)
    
    # Close files after logging everything
    word_file.close()
    generation_active_state = False

if __name__ == '__main__':
    jobs = []
    p1 = multiprocessing.Process(name='log', target=log_activations)
    p2 = multiprocessing.Process(name='generate', target=generate_audio)
    p1.start()
    p2.start()
