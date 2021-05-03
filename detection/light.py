import serial
import time


class LightDetection:
    time_out = 3.0
    
    def __init__(self, name, experiment, trial_number, port='/dev/ttyUSB0'):
        self.port = port
        self.arduino = serial.Serial(port=port,
                                     timeout=LightDetection.time_out,
                                     baudrate='9600')
        
        output_filename = f"./light_logs/{name}/{experiment}/{name}_{experiment}_{trial_number}_light_activations.csv"
        self.output_file = open(output_filename, "w", buffering=1)
        
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


