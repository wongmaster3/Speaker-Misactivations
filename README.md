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
python3 main.py <mp3_dir> -n <iot_device_name> -d <delay>
```

'mp3_dir' will contain the directory of the word files that will be played. 'delay' will contain the delay between each word played. 'iot_device_name' will contain the name of the iot device.

Logs will print out in the logs folder with the format
```shell
<iot_device_name> + _light_activations.csv
<iot_device_name> + _word_generations.csv
```