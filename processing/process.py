import csv
import argparse
import os
from collections import defaultdict


class Processor: 
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process audio and light misactivations')
        parser.add_argument('--path', '-fp', help='path to the experiment logs')
        parser.add_argument('--company_name', '-cn', help='company name of iot device')

        self.config = parser.parse_args()
        self.iot_keyword = 'hey_alexa' if self.config.company_name == 'amazon' else 'ok_google' 
        self.questions = set(['what_is_the_weather_today', 'what_is_food', 'how_are_you'])

    def get_parser(self):
        return self.config

    def pairwise(self, iterable):
        a = iter(iterable)
        return zip(a, a)

    def process_experiment(self):
        dirpath, files, filenames = next(os.walk(self.config.path))
        paired_files = self.pairwise(sorted(filenames))

        trial_num = 1
        merged_dictionary = {}
        merged_observed = 0
        merged_expected = 0
        for light, word in paired_files:
            light_path = os.path.join(dirpath, light)
            word_path = os.path.join(dirpath, word)
            # Dictionary of activated words with values as arrays of lengths of activations
            (misactivated_words, trigger_activated_words, expected_valid_activation_count) = self.process_trial(light_path, word_path)
            misactivated_words_count_dict = {k: len(v) for k, v in misactivated_words.items()}
            observed_trigger_count = len(trigger_activated_words)
            merged_dictionary = {k: merged_dictionary.get(k, 0) + misactivated_words_count_dict.get(k, 0) for k in set(merged_dictionary) | set(misactivated_words_count_dict)}
            merged_observed += observed_trigger_count
            merged_expected += expected_valid_activation_count
            print("Trial #: " + str(trial_num))
            print("# of Observed Trigger Word Activations: " + str(observed_trigger_count))
            print("# of Expected Trigger Word Activations: " + str(expected_valid_activation_count))
            print("Misactivation Counts: " + str(misactivated_words_count_dict))
            print("Misactivation Times (seconds): " + str(misactivated_words))
            print('\n')

            trial_num += 1

        print("# of Observed Trigger Word Activations for All Trials: " + str(merged_observed))
        print("# of Expected Trigger Word Activations for All Trials: " + str(merged_expected))
        print("All Misactivation Counts for All Trials: " + str(merged_dictionary))

        
    def process_trial(self, light, word):
        word_time = open(word, mode='r')
        light_time = open(light, mode='r')

        wt_reader = list(csv.DictReader(word_time))
        lt_reader = list(csv.DictReader(light_time))

        trigger_activated_words = []
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
                if wt_reader[wt_index]['word'] == self.iot_keyword:
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
            if prev_word != self.iot_keyword or (prev_word == self.iot_keyword and float(wt_reader[current_word_index]['start_time'])-float(wt_reader[prev_word_index]['end_time']) > 2.0):
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
                        if word == self.iot_keyword:
                            trigger_activated_words.append(light_activation_end_time-light_activation_start_time)
                        else:
                            misactivated_words[word].append(light_activation_end_time-light_activation_start_time)
                        last_added_word_index = current_word_index
                    else:
                        if word == self.iot_keyword:
                            trigger_activated_words[-1] += (light_activation_end_time-light_activation_start_time)
                        else:
                            time_lst = misactivated_words[word]
                            time_lst[-1] += (light_activation_end_time-light_activation_start_time)

        return (dict(misactivated_words), trigger_activated_words, total_valid_activation_count)

if __name__ == '__main__':
    processor = Processor()
    processor.process_experiment()
    