from multiprocessing import Process, Manager, Value
import os
from generate.play_audio import *
from detection.light import *


def get_main_parser():
    parser = argparse.ArgumentParser(description='Play and log audio--everything.')
    
    return parser


config = get_play_parser().parse_args()
delay_between_words = config.delay


def log_activations(generation_active_state):
    detector = LightDetection(config.device_name.lower())
    
    while generation_active_state.value == 1:
        detector.log()
    
    detector.close()


def generate_audio(generation_active_state):
    word_file = open("./logs/" + config.device_name.lower() + "_word_generations.csv", "w")
    word_file.write('word,start_time,end_time\n')

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
    generation_active_state.value = 0


if __name__ == '__main__':
    # Generation flag
    generation_active_state = Value('i', 1)
    p1 = Process(name='log', target=log_activations, args=(generation_active_state,))
    p2 = Process(name='generate', target=generate_audio, args=(generation_active_state,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
