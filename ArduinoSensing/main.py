import serial
from time import sleep

# Put own path in Serial argument
arduino = serial.Serial(port='/dev/cu.usbserial-145220', baudrate='9600')

while True:
    print(arduino.readline())
    sleep(0.1)


