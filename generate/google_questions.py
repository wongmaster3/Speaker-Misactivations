import argparse

import jsonlines

"""
This script will create a "text source" for the n-gram model from the Google questions and
answers dataset in JSONLines format (unzipped).

To regenerate, download the simplified training data from
https://ai.google.com/research/NaturalQuestions/download.
The simplified source file is huge (over 4gb), so don't put it into git! Unzip, then run this script.
"""

parser = argparse.ArgumentParser(description='Extract questions from Q&A jsonlines as text')
parser.add_argument('filename', help='unzipped JSONLines file (simplified)')
parser.add_argument('output_filename', help='output filename of the text file')

config = parser.parse_args()

with jsonlines.open(config.filename) as reader, open(config.output_filename, 'w') as out:
    for obj in reader:
        question = obj['question_text']
        out.write(f'{question}? ')
