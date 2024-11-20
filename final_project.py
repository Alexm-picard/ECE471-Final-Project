import time
import board
import busio
import adafruit_sgp30
import spidev

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

spi = spidev.SpiDev()
spi.open(0,0)

sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius=22.1, relative_humidity=44)

spi.max_speed_hz = 1350000
spi.mode = 0b00

def read_adc(channel):
	adc = spi.xfer2([1, (8+channel) << 4 , 0])
	data = ((adc[1] & 3)<<8) + adc[2]
	return data

while True:
	raw_value = read_adc(0)
	voltage = (raw_value * 5) / 1023.0
	print("Voltage (v):" + str(voltage))
	print("eCO2 = %d ppm \t TVOC = %d ppb " % (sgp30.eCO2, sgp30.TVOC))
	time.sleep(1)
spi.close()
