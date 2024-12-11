import time
import board
import busio
import adafruit_sgp30
import spidev
from flask import Flask, render_template, jsonify
import random
import sqlite3

app = Flask(__name__)
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
#def add_sensor_data(voltage, co2, tvoc):
#	connection = sqlite3.connect("sensor_data.db")
#	date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#	try:
#		db_cursor = connection.cursor()
#		sql = """INSERT INTO sensor(DATE, VOLTAGE, CO2, TVOC)
#			VALUES(?,?,?,?)"""
#		db_cursor.execute(sql, (date_time,voltage, co2, tvoc))
#		connection.commit()
#		connection.close()
#		
#	except sqlite3.OperationalError:
#		connection = sqlite3.connect("sensor_data.db") 
#		db_cursor = connection.cursor()
#		db_cursor.execute("CREATE TABLE sensor(DATE, VOLTAGE, CO2, TVOC)")
#		sql = """INSERT INTO sensor(DATE, VOLTAGE, CO2, TVOC)
#			VALUES(?,?,?,?)"""
#		db_cursor.execute(sql, (date_time,voltage, co2, tvoc))
#		connection.commit()
#		connection.close()
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


@app.route('/')
def index():
	return render_template('index.html')	

@app.route('/api/sensor_data')
def data_gather():
	raw_value = read_adc(0)
	voltage = (raw_value * 5) / 1023.0
	sensor_data = {"MiCS_5524": voltage,
			"SGP30_co2": sgp30.eCO2,
			"SGP30_tvoc":  sgp30.TVOC}
#	add_sensor_data(sensor_data["MiCS_5524"],sensor_data["SGP30_co2"], sensor_data["SGP30_tvoc"]) 
	
	return jsonify(sensor_data)

if __name__ == '__main__':
	app.run(debug=True)
