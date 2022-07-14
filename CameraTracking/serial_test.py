from time import sleep
import serial

a= [0xff,0x02,0x00,0x07,0x00,0x50,0x59]
b = [0xff,0x01,0x04,0x0a,0x0a]
c= [0xff,0x01,0x00,0x07,0x00,0x50,0x58]
d = [0xff,0x01,0x04,0x0b,0x0b]

portx = "/dev/ttyUSB0"
bps = 9600
timex = 5
ser = serial.Serial(portx, bps, timeout=timex)
while True:
    ser.write(bytearray("abcdefg abc ","ascii"))
    sleep(0.5)
    '''print("YPA")
    ser.write(bytearray(a))
    sleep(0.1)
    ser.write(bytearray(b))
    sleep(0.1)
    ser.write(bytearray(c))
    sleep(0.1)
    ser.write(bytearray(d))
    sleep(0.1)'''