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

### Main Program
Run
```shell
python3 main.py <mp3_dir>
```

'mp3_dir' will contain the word files that will be played. Should also put 'mp3_dir' in same directory as 'main.py'.
