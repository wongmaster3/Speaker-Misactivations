import csv
import argparse
import os, fnmatch
import json
import copy
import pandas as pd
from collections import defaultdict


class Processor: 
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process audio and light misactivations')
        parser.add_argument('--path', '-fp', help='path to the experiment logs')

        self.config = parser.parse_args()
        self.questions = set(['what_is_the_weather_today', 'what_is_food', 'how_are_you'])
        self.result_json = []

    def get_parser(self):
        return self.config

    def process_trials(self):
        dirpath, files, filenames = next(os.walk(self.config.path))

        for file in files:
            experiment_path = os.path.join(dirpath, file)
            sub_dirpath, _, sub_filenames = next(os.walk(experiment_path))
            parameters_file = open(os.path.join(sub_dirpath, 'parameters.json'), "r", buffering=1)
            new_trial = json.load(parameters_file)
            light_path = None
            word_path = None
            for file in sub_filenames:
                if fnmatch.fnmatch(file, '*_light_activations.csv'):
                    light_path = os.path.join(sub_dirpath, file)
                elif fnmatch.fnmatch(file, '*_word_generations.csv'):
                    word_path = os.path.join(sub_dirpath, file)
            
            iot_keyword = 'hey_alexa' if new_trial['device'] == 'echo' else 'ok_google' 
            (misactivated_words, expected_valid_activation_count) = self.process_trial(light_path, word_path, iot_keyword)
            for word, times in misactivated_words.items():
                for time in times:
                    deep_copy = copy.deepcopy(new_trial)
                    deep_copy['word'] = word
                    deep_copy['duration'] = time
                    self.result_json.append(deep_copy)
        
        return self.result_json
        
    def process_trial(self, light, word, iot_keyword):
        word_time = open(word, mode='r')
        light_time = open(light, mode='r')

        wt_reader = list(csv.DictReader(word_time))
        lt_reader = list(csv.DictReader(light_time))

        misactivated_words = defaultdict(lambda: [])

        total_valid_activation_count = 0
        last_added_word_index = None

        wt_index = 0
        for row in lt_reader:
            light_activation_start_time = float(row['start_time'])
            light_activation_end_time = float(row['end_time'])

            wt_start_time = float(wt_reader[wt_index]['start_time'])
            wt_end_time = float(wt_reader[wt_index]['end_time'])
            while wt_index < len(wt_reader) and light_activation_start_time >= wt_end_time:
                if wt_reader[wt_index]['word'] == iot_keyword:
                    total_valid_activation_count += 1
                wt_index += 1
                if wt_index < len(wt_reader):
                    wt_start_time = float(wt_reader[wt_index]['start_time'])
                    wt_end_time = float(wt_reader[wt_index]['end_time'])

            # Check if start time of light activation occurred within the current word phrase or 
            # if it was triggered after the previous word phrase
            current_word_index = None
            prev_word_index = None
            if light_activation_start_time < wt_start_time:
                current_word_index = wt_index-1
                prev_word_index = wt_index-2
            else:
                if wt_index < len(wt_reader):
                    current_word_index = wt_index
                    prev_word_index = wt_index-1
                else:
                    current_word_index = wt_index-1
                    prev_word_index = wt_index-2
            
            # if 'current word start time - iot activation word end time' < 2, then we need to discard
            # Program said next word before recording light
            word = wt_reader[current_word_index]['word']
            prev_word = wt_reader[prev_word_index]['word']
            if prev_word != iot_keyword or (prev_word == iot_keyword and float(wt_reader[current_word_index]['start_time'])-float(wt_reader[prev_word_index]['end_time']) > 2.0):
                if word in self.questions:
                    prev_word_with_question = prev_word + ': ' + word
                    misactivated_words[prev_word_with_question] = misactivated_words[prev_word]
                    if len(misactivated_words[prev_word_with_question]) == 0:
                        misactivated_words[prev_word_with_question].append((light_activation_end_time-light_activation_start_time))
                    else:
                        misactivated_words[prev_word_with_question][-1] += (light_activation_end_time-light_activation_start_time)
                    del misactivated_words[prev_word]
                else:
                    # Need to check if trigger word activated within same time frame
                    if (last_added_word_index == None) or (last_added_word_index != current_word_index):
                        misactivated_words[word].append(light_activation_end_time-light_activation_start_time)
                        last_added_word_index = current_word_index
                    else:
                        time_lst = misactivated_words[word]
                        time_lst[-1] += (light_activation_end_time-light_activation_start_time)

        return (dict(misactivated_words), total_valid_activation_count)

if __name__ == '__main__':
    processor = Processor()
    all_trials = processor.process_trials()
    with open('results/activations.json', 'w') as f:
        f.write(json.dumps(all_trials, indent=4))
        df = pd.read_json('results/activations.json')
        df.to_csv ('results/activations.csv', index = None)
    