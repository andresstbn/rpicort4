import RPi.GPIO as io
import time 

salidas = (4,17,27,22)
io.setmode(io.BCM)
io.setup(salidas, io.OUT)
io.output(salidas, io.HIGH)
# ~ time.sleep(5)
io.output(27, io.LOW)
for i in range(200):
	io.output(22, io.HIGH)
	time.sleep(0.01)
	io.output(22, io.LOW)
	time.sleep(0.01)
	
time.sleep(1)
io.cleanup()
