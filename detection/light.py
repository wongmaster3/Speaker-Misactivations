import atexit
import os
import serial
import time


class LightDetection:
    time_out = 0.1
    
    def __init__(self, name, port='/dev/ttyUSB0'):
        self.port = port
        self.arduino = serial.Serial(port=port,
                                     timeout=LightDetection.time_out,
                                     baudrate='9600')
        
        filename = os.path.join('logs', f'{name}_light_activations.csv')
        self.output_file = open(filename, 'w')
        
        # in case of interruption
        # atexit.register(self.close, self)
        
        # file heading
        self.output_file.write('start_time,end_time\n')
    
    def log(self, logging_active_state):
        # Check if iot device activates on sound within 0.1 seconds
        # If it does, then log it or else do nothing
        on_state = str(self.arduino.readline())
        if on_state[1:] != "''":
            logging_active_state.value = 1
            self.arduino.timeout = None
            start_time = str(time.time())
            off_state = str(self.arduino.readline())
            end_time = str(time.time())
            self.arduino.timeout = LightDetection.time_out
            logging_active_state.value = 0
        
            self.output_file.write(f'{start_time},{end_time}\n')

    def close(self):
        if self.output_file:
            self.output_file.close()
            self.output_file = None


