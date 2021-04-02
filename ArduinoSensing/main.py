import serial
import datetime
import sys
import pandas as pd

# Get command line arguments
output_file = sys.argv[1]

# Logged data
logged_data = []

# Number of samples we are taking
sample_count = 5;

# Put own path for 'port' argument
# Current wait for response from iot device is 5 seconds
arduino = serial.Serial(port='/dev/cu.usbserial-145220', timeout=5.0, baudrate='9600')
print(datetime.datetime.now())

def log(sound):
    # Play sound here
    print("Playing Sound: " + sound)

    # New row in csv file
    new_row = [sound]

    # Check if iot device activates on sound within 5 seconds
    # If it does, then log it or else do nothing
    on_state = str(arduino.readline())
    if on_state[1:] != "''":
        # Since iot device activated, we want to deactivate the timeout for 'readline()'
        arduino.timeout = None

        time_now = str(datetime.datetime.now())
        new_row.append(time_now)
        print("Activated: " + time_now)

        off_state = str(arduino.readline())
        time_now = str(datetime.datetime.now())
        new_row.append(time_now)
        print("Unactivated: " + time_now)

        millis_elapsed = str(arduino.readline())
        millis_elapsed = millis_elapsed[2:len(millis_elapsed)-5]
        new_row.append(millis_elapsed)
        print("Milliseconds Elapsed: " + millis_elapsed + '\n')

        logged_data.append(new_row)

        # We want to set timeout back to 5 seconds since we want to play next noise
        arduino.timeout = 5.0
    else:
        print("No Activation")
        logged_data.append([sound, None, None, None])

i = 0
while arduino.isOpen() and sample_count > i:
    log('haha')
    i += 1

df = pd.DataFrame(logged_data, columns = ['sound', 'start', 'end', 'elapsed_time'])
df.to_csv(output_file, index=False)