# Speaker-Misactivations
## Setup & Requirements
Python requirements can be installed for everything via
```shell
pip3 install -r requirements.txt
```
## Light Sensing
### Run
Upload the Arduino logging code (in [LightSensing](LightSensing)) to the arduino. Then run:
```shell
python3 detection/light.py test.csv
```

## Generation
### Most Common Words
Run 
```shell
python3 generate/common_words.py 
```

There may be an issue with the libffi-dev library (related to pyglet, used for playing audio).

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

'mp3_dir' will contain the directory of the word files that will be played. 'delay' will contain the delay between each word played. 'iot_device_name' will contain the name of the iot device, the experiment number, and the trial number. The -q argument signifies whether or not you want to ask a question after a misactivation. If included, it will ask a random question in 'questions.txt' or else no question will be asked. If you want to ask a question, please set the delay to 0.4-0.5 seeconds or else the question might not be asked when the device is misactivated. For example, if running experiment 1 and trial 2 and asking questions, the command will look like this:

```shell
python3 main.py data/common-en.com -n echo_1_2 -d 0.45 -q
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
