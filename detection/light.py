import serial
import time

# Set time out
time_out = 0.1

# Put own path for 'port' argument
# Current wait for response from iot device is 5 seconds
arduino = serial.Serial(port='/dev/cu.usbserial-145230', timeout=time_out, baudrate='9600')

def log(output_file):
    # Check if iot device activates on sound within 5 seconds
    # If it does, then log it or else do nothing
    on_state = str(arduino.readline())
    if on_state[1:] != "''":
        arduino.timeout = None
        start_time = str(time.time())
        off_state = str(arduino.readline())
        end_time = str(time.time())
        arduino.timeout = time_out

        output_file.write(f'{start_time},{end_time}\n')
