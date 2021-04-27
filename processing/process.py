import csv
import argparse
from collections import defaultdict


class Processor: 
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process audio and light misactivations')
        parser.add_argument('--word_time', '-wt', help='the time csv of the words')
        parser.add_argument('--light_time', '-lt', help='the time csv of the light misactivations')

        self.config = parser.parse_args()

    def process(self):
        word_time = open(self.config.word_time, mode='r')
        light_time = open(self.config.light_time, mode='r')

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
            
            misactivated_words[word].append(light_activation_end_time-light_activation_start_time)

        return misactivated_words

if __name__ == '__main__':
    processor = Processor()
    processed_tuples = processor.process()
    print(processed_tuples)