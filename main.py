import os
from multiprocessing import Process, Value
from generate.play_audio import *
from detection.light import *
import random

config = get_play_parser().parse_args()
delay_between_words = config.delay
ask_questions = config.questions
device_name = config.device_name.lower()
experiment = config.experiment
trial_number = config.trial
tld = config.tld
word_list_filename = config.word_list_filename


def log_activations(generation_active_state, logging_active_state):
    detector = LightDetection(device_name, experiment, trial_number, tld)
    
    while generation_active_state.value == 1:
        detector.log(logging_active_state)
    
    detector.close()


def words_ordered(file='cache/google-10000-english-no-swears.txt'):
    triggers = ['ok_google', 'hey_alexa', 'hey_siri']
    
    with open(file) as f:
        for num, line in enumerate(f):
            yield line.strip().partition(':')[0]
            
            if num % 50 == 0:
                yield random.choice(triggers)
    

def generate_audio(generation_active_state, logging_active_state):
    output_filename = f"./experiments/{device_name}_{experiment}_{trial_number}.{tld}/{device_name}_{tld}_{trial_number}_word_generations.csv"
    word_file = open(output_filename, "w", buffering=1)
    word_file.write('word,start_time,end_time\n')

    root, _, filenames = next(os.walk(config.dir))
    filenames = frozenset(filenames)
    trigger_word = 'hey_alexa' if device_name == 'echo' else 'ok_google' 
    questions = []
    for word in words_ordered('cache/questions.txt'):
        questions.append(word.replace(' ', '_'))
    
    for word in words_ordered(word_list_filename):
        filename = f'{word}.mp3'
        
        if filename in filenames:
            filepath = os.path.join(root, filename)
            bitrate, audio = read(filepath)
            
            # Play sound here
            start_time = str(time.time())
            play_array(audio, bitrate)
            end_time = str(time.time())
            word_file.write(f'{word},{start_time},{end_time}\n')
            
            # Delay before playing next word
            if word == trigger_word:
                time.sleep(2.0)
            else:
                time.sleep(delay_between_words)
            
            # Ask question to misactivated word
            if config.questions:
                if logging_active_state.value == 1 and (word != trigger_word):
                    # Ask question
                    question = random.choice(questions)
                    question_filename = f'{question}.mp3'

                    filepath = os.path.join(root, question_filename)
                    bitrate, audio = read(filepath)
                    
                    # Play question here
                    start_time = str(time.time())
                    play_array(audio, bitrate)
                    end_time = str(time.time())
                    word_file.write(f'{question},{start_time},{end_time}\n')

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
    p1 = Process(name='log', target=log_activations, args=(generation_active_state, logging_active_state,))
    p2 = Process(name='generate', target=generate_audio, args=(generation_active_state, logging_active_state,))
    processes = [p1, p2]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
