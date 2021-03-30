import serial
import datetime
import sys
import numpy as np
import pandas as pd

# Get command line arguments
output_file = sys.argv[1]

# Logged data
logged_data = []

# Number of samples we are taking
sample_count = 5;

# Put own path in Serial argument
arduino = serial.Serial(port='/dev/cu.usbserial-145220', baudrate='9600')
print(datetime.datetime.now())

def log():
    new_row = []

    on_state = str(arduino.readline())
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

i = 0
while arduino.isOpen() and sample_count > i:
    log()
    i += 1

df = pd.DataFrame(logged_data, columns = ['start', 'end', 'elapsed_time'])
df.to_csv(output_file, index=True)