from multiprocessing import Process, Manager, Value
from generate.play_audio import *
from detection.light import *
import random

config = get_play_parser().parse_args()
delay_between_words = config.delay


def log_activations(generation_active_state, logging_active_state):
    detector = LightDetection(config.device_name.lower())
    
    while generation_active_state.value == 1:
        detector.log(logging_active_state)
    
    detector.close()


def words_ordered(file='cache/google-10000-english-no-swears.txt'):
    triggers = ['ok_google', 'hey_alexa', 'hey_siri']
    
    with open(file) as f:
        for num, line in enumerate(f):
            yield line.strip()
            
            if num % 50 == 0:
                yield random.choice(triggers)


def generate_audio(generation_active_state, logging_active_state):
    word_file = open("./light_logs/" + config.device_name.lower() + "_word_generations.csv", "w")
    word_file.write('word,start_time,end_time\n')

    root, _, filenames = next(os.walk(config.dir))
    filenames = frozenset(filenames)
    for word in words_ordered():
        filename = f'{word}.mp3'
        
        if filename in filenames:
            filepath = os.path.join(root, filename)
            bitrate, audio = read(filepath)
            
            # Play sound here
            start_time = str(time.time())
            play_array(audio, bitrate)
            end_time = str(time.time())
            word_file.write(f'{word},{start_time},{end_time}\n')
            time.sleep(delay_between_words)
            # Need to wait in case light activation occurs in middle or after
            # the saying of the word
            while logging_active_state.value == 1:
                time.sleep(1.0)
    
    # Close files after logging everything
    word_file.close()
    generation_active_state.value = 0


if __name__ == '__main__':
    # Generation flag
    generation_active_state = Value('i', 1)
    logging_active_state = Value('i', 0)
    p1 = Process(name='log', target=log_activations, args=(generation_active_state,logging_active_state,))
    p2 = Process(name='generate', target=generate_audio, args=(generation_active_state,logging_active_state,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

