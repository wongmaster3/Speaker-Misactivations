import serial
import time

# Number of samples we are taking
time_out = 1.0

# Put own path for 'port' argument
# Current wait for response from iot device is 5 seconds
arduino = serial.Serial(port='/dev/cu.usbserial-141220', timeout=time_out, baudrate='9600')

def log(filename, play_audio_func, audio, bitrate):
    text = filename.split('.')[0]

    # Play sound here
    play_audio_func(audio, bitrate)

    # Check if iot device activates on sound within 5 seconds
    # If it does, then log it or else do nothing
    on_state = str(arduino.readline())
    if on_state[1:] != "''":
        # Since iot device activated, we want to deactivate the timeout for 'readline()'
        arduino.timeout = None

        start_time = str(time.time())
        off_state = str(arduino.readline())
        end_time = str(time.time())

        print(f'{text},{start_time},{end_time}')

        # We want to set timeout back to 5 seconds since we want to play next noise
        arduino.timeout = time_out
    else:
        print(f'{text},NA,NA')
