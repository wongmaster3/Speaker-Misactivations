# Speaker-Misactivations
## Setup & Requirements
Python requirements can be installed for everything via
```shell
pip3 install -r requirements.txt
```

On linux, you may have to first install python3 and ALSA (dev packages) first; on Debian/Ubuntu flavors:
```shell
sudo apt-get install -y python3-dev libasound2-dev
```

## Light Sensing
### Run
Upload the Arduino logging code (in [LightSensing](LightSensing)) to the arduino. Then run:
```shell
python3 detection/light.py test.csv
```

## Generation
### Words
The source file should just be a text file that contains one word per line. Then, run
```shell
python3 generate/generate_audio.py -f <filename> --name <name>
```

### N-Gram Generation
For n-gram model generated sentences, run
```shell
python3 generate/ngrams.py <source textfile> <number of sentences> --order <n> --output-filename <filename>
```
where `<source textfile>` is the text file containing text to build the model off of, `<order>` is the max size of the n-gram (currently using 8), and <filename> is the output file (used for next step). 

Then to actually generate the audio files, run 
```shell
python3 generate/generate_audio.py -f <filename> --name <name> --has-prefix
```
where `<filename>` is the file that was generated via the previous script and `<name>` is just a name for the dataset (note the `--has-prefix` switch; this is because sentences can sometimes contain illegal filename characters).


## Main Program
1. Change line 6 (serial port) in
```shell
./detection/light.py
```
to match the serial port of the Arduino on your machine. 

2. Run
```shell
python3 main.py <mp3_dir> -n <iot_device_name> -d <delay> -q
```

'mp3_dir' will contain the directory of the word files that will be played. 'delay' will contain the delay between each word played. 'iot_device_name' will contain the name of the iot device, the experiment number, and the trial number. The -q argument signifies whether or not you want to ask a question after a misactivation. If included, it will ask a random question in 'questions.txt' or else no question will be asked. If you want to ask a question, please set the delay to 0.4-0.5 seeconds or else the question might not be asked when the device is misactivated. For example, if running com words folder and trial 2 and asking questions, the command will look like this:

```shell
python3 main.py data/common-en.com -n echo -e com -t 2 -d 0.45 -q
```
It seems like 0.35 seconds or higher is the best for recording misactivations. 

Logs will print out in the logs folder with the format
```shell
<iot_device_name> + _light_activations.csv
<iot_device_name> + _word_generations.csv
```

## Process Script
Run 
```shell
python3 processing/process.py -fp <folder_to_experiment_csv_files> -cn <company_name>
```

The 'folder_to_experiment_csv_files' string will contain the file path to the experiments folder with the device name. The 'company_name' will contain the company name of the iot device (amazon or google). For example,
```shell
python3 processing/process.py -fp ./light_logs/echo/experiment_1 -cn amazon
```
