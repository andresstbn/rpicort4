import minimalmodbus
import serial
from time import sleep
import RPi.GPIO 


class ModbusInstrument:
	ADDR_ENABLE = 0x8000
	ADDR_MODO = 0x8001
	
	def __init__(self):
		self.sdrv = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
		self.sdrv.serial.baudrate = 9600
		self.sdrv.serial.bytesize = 8
		self.sdrv.serial.parity   = serial.PARITY_NONE
		self.sdrv.serial.stopbits = 1
		self.sdrv.serial.timeout  = 0.2
		self.sdrv.mode = minimalmodbus.MODE_ASCII
		
	def posicionar(self):
		# ~ self.sdrv.write_register(0x8000, 1)
		self.read_print(0x8000)
		self.sdrv.write_register(0x8002, 10000)
	
	def read_print(self, register):
		r = self.sdrv.read_register(register)
		print('{} 0x{:x}: {}'.format(register, register, r))
		return r

	def write(self, register, value):
		self.sdrv.write_register(register, value)
		
if __name__ == '__main__':
	pins_servo = [17, 22, 25, 4]
	io = RPi.GPIO
	io.setmode(io.BCM)
	io.setup(pins_servo, io.OUT)
	# ~ io.setup(self.pin_sbloqueo, io.IN, pull_up_down=io.PUD_DOWN)
	io.output(pins_servo, io.HIGH)
	io.output(pins_servo[2], io.LOW)
	
		
	sleep(0.1)
	

	i = ModbusInstrument()
	i.write(33, 1)
	i.write(34, 100)
	for j in range(2000):
		io.output(pins_servo[3], io.LOW)
		sleep(.0000001)
		io.output(pins_servo[3], io.HIGH)
		sleep(.000001)
	# ~ i.posicionar()
	i.sdrv.write_register(6,0x0011)
	# ~ i.read_print(0) #Version
	# ~ i.read_print(2) #Password
	# ~ i.read_print(44)#Command pulse mode
	# ~ i.read_print(23)#Command pulse mode
	# ~ i.read_print(4)
	# ~ i.read_print(6)
	# ~ i.read_print(87)
	i.write(0x8000, 1)
	i.write(0x8001, 2)
	# ~ i.read_print(0x8000)
	# ~ i.read_print(0x8001)
	i.posicionar()
	# ~ i.read_print(0x8002)
	
	# ~ i.read_print(33)
	# ~ i.read_print(34)
	# ~ i.read_print(49)
	# ~ i.read_print(0x8008)
	# ~ i.read_print(0x800A)
	io.cleanup()
