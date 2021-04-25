import csv
import argparse


class Processor: 
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process audio and light misactivations')
        parser.add_argument('--word_time', '-wt', help='the time csv of the words')
        parser.add_argument('--light_time', '-lt', help='the time csv of the light misactivations')

        config = parser.parse_args()

    def process():
        word_time = open(config.word_time, mode='r')
        light_time = open(config.light_time, mode='r')

        wt_reader = csv.DictReader(word_time)
        lt_reader = csv.DictReader(light_time)

        misactivated_words = []

        wt_index = 0
        for row in lt_reader:
            lower_bound = row['start_time']
            upper_bound = row['end_time']

            wt_start_time = wt_reader[wt_index]['start_time']
            wt_end_time = wt_reader[wt_index]['end_time']
            while wt_index < len(wt_reader) and wt_end_time < lower_bound:
                wt_index += 1
                wt_start_time = wt_reader[wt_index]['start_time']
                wt_end_time = wt_reader[wt_index]['end_time']

            misactivated_words.append((wt_reader[wt_index-1]['word'], upper_bound-lower_bound))

        return misactivated_words

if __name__ == '__main__':
    processor = Processor()
    processed_tuples = processor.process()
    print(processed_tuples)