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

    def get_parser(self):
        return self.config

    def pairwise(self, iterable):
        a = iter(iterable)
        return zip(a, a)

    def process(self, light, word):
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
            # Need to check if trigger word activated within same time frame since
                if (last_added_word_index == None) or (last_added_word_index != current_word_index):
                    misactivated_words[word].append(light_activation_end_time-light_activation_start_time)
                    last_added_word_index = current_word_index
                else:
                    time_lst = misactivated_words[word]
                    time_lst[-1] += (light_activation_end_time-light_activation_start_time)

        return (dict(misactivated_words), total_valid_activation_count)

if __name__ == '__main__':
    processor = Processor()
    config = processor.get_parser()

    dirpath, files, filenames = next(os.walk(config.path))
    paired_files = processor.pairwise(sorted(filenames))

    trial_num = 1
    merged_dictionary = {}
    merged_observed = 0
    merged_expected = 0
    for light, word in paired_files:
        light_path = os.path.join(dirpath, light)
        word_path = os.path.join(dirpath, word)
        # Dictionary of activated words with values as arrays of lengths of activations
        output = processor.process(light_path, word_path)
        count_dict = {k: len(v) for k, v in output[0].items()}
        merged_dictionary = {k: merged_dictionary.get(k, 0) + count_dict.get(k, 0) for k in set(merged_dictionary) | set(count_dict)}
        merged_observed += len(output[0][processor.iot_keyword])
        merged_expected += output[1]
        print("Trial #: " + str(trial_num))
        print("# of Observed Trigger Word Activations: " + str(len(output[0][processor.iot_keyword])))
        print("# of Expected Trigger Word Activations: " + str(output[1]))
        print("All Activation Counts: " + str(count_dict))
        print("All Activation Times (seconds): " + str(output[0]))
        print('\n')

        trial_num += 1

    print("# of Observed Trigger Word Activations for All Trials: " + str(merged_observed))
    print("# of Expected Trigger Word Activations for All Trials: " + str(merged_expected))
    print("All Activation Counts for All Trials: " + str(merged_dictionary))


    