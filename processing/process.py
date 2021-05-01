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
        self.total_count_of_words = defaultdict(lambda: 0)
        self.iot_keyword = 'hey_alexa' if self.config.company_name == 'amazon' else 'ok_google' 

    def get_parser(self):
        return self.config

    def pairwise(self, iterable):
        a = iter(iterable)
        return zip(a, a)

    def get_total_count_of_words(self):
        return self.total_count_of_words

    def process(self, light, word):
        word_time = open(word, mode='r')
        light_time = open(light, mode='r')

        wt_reader = list(csv.DictReader(word_time))
        lt_reader = list(csv.DictReader(light_time))

        misactivated_words = defaultdict(lambda: [])

        wt_index = 0
        for row in lt_reader:
            light_activation_start_time = float(row['start_time'])
            light_activation_end_time = float(row['end_time'])

            wt_start_time = float(wt_reader[wt_index]['start_time'])
            wt_end_time = float(wt_reader[wt_index]['end_time'])
            while wt_index < len(wt_reader) and light_activation_start_time >= wt_end_time:
                wt_index += 1
                if wt_index < len(wt_reader):
                    wt_start_time = float(wt_reader[wt_index]['start_time'])
                    wt_end_time = float(wt_reader[wt_index]['end_time'])

            # Check if start time of light activation occurred within the current word phrase or 
            # if it was triggered after the previous word phrase
            word = None
            prev_word = None
            current_word_index = None
            prev_word_index = None
            if light_activation_start_time < wt_start_time:
                word = wt_reader[wt_index-1]['word']
                current_word_index = wt_index-1
                prev_word_index = wt_index-2
            else:
                if wt_index < len(wt_reader):
                    word = wt_reader[wt_index]['word']
                    current_word_index = wt_index
                    prev_word_index = wt_index-1
                else: 
                    word = wt_reader[wt_index-1]['word']
                    current_word_index = wt_index-1
                    prev_word_index = wt_index-2
            
            # if 'current word start time - iot activation word end time' < 2, then we need to discard
            # Program said next word before recording light
            prev_word = wt_reader[prev_word_index]['word']
            if prev_word != self.iot_keyword or (prev_word == self.iot_keyword and float(wt_reader[current_word_index]['start_time'])-float(wt_reader[prev_word_index]['end_time']) > 2.0):
                if (word not in misactivated_words) or (word in ['ok_google', 'hey_alexa', 'hey_siri']): 
                    self.total_count_of_words[word] += 1
                misactivated_words[word].append(light_activation_end_time-light_activation_start_time)

        return misactivated_words

if __name__ == '__main__':
    processor = Processor()
    config = processor.get_parser()

    dirpath, _, filenames = next(os.walk(config.path))
    paired_files = processor.pairwise(sorted(filenames))

    for light, word in paired_files:
        light_path = os.path.join(dirpath, light)
        word_path = os.path.join(dirpath, word)
        # Dictionary of activated words with values as arrays of lengths of activations
        output_dict = dict(processor.process(light_path, word_path))
    
    # Prints out total sum of activations per word in all trials in single experiment
    print(dict(processor.get_total_count_of_words()))