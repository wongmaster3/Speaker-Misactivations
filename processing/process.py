import csv
import argparse
import os
from collections import defaultdict


class Processor: 
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process audio and light misactivations')
        parser.add_argument('--path', '-fp', help='the time csv of the words')

        self.config = parser.parse_args()
        self.total_count_of_words = defaultdict(lambda: 0)

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
            if light_activation_start_time < wt_start_time:
                word = wt_reader[wt_index-1]['word']
            else:
                if wt_index < len(wt_reader):
                    word = wt_reader[wt_index]['word']
                else: 
                    word = wt_reader[wt_index-1]['word']
            
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
        processor.process(light_path, word_path)
    
    print(processor.get_total_count_of_words())
        