import time
import board
import busio
import adafruit_sgp30
import spidev
from flask import Flask, render_template, jsonify
import random
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
def add_sensor_data(voltage, co2, tvoc):
	connection = sqlite3.connect("sensor_data.db")
	date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	try:
		db_cursor = connection.cursor()
		sql = """INSERT INTO sensor(DATE, VOLTAGE, CO2, TVOC)
			VALUES(?,?,?,?)"""
		db_cursor.execute(sql, (date_time,voltage, co2, tvoc))
		connection.commit()
		connection.close()
		
	except sqlite3.OperationalError:
		connection = sqlite3.connect("sensor_data.db") 
		db_cursor = connection.cursor()
		db_cursor.execute("CREATE TABLE sensor(DATE, VOLTAGE, CO2, TVOC)")
		sql = """INSERT INTO sensor(DATE, VOLTAGE, CO2, TVOC)
			VALUES(?,?,?,?)"""
		db_cursor.execute(sql, (date_time,voltage, co2, tvoc))
		connection.commit()
		connection.close()
#spi = spidev.SpiDev()
#spi.open(0,0)
	
#sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
#sgp30.set_iaq_baseline(0x8973, 0x8AAE)
#sgp30.set_iaq_relative_humidity(celsius=22.1, relative_humidity=44)

#spi.max_speed_hz = 1350000
#spi.mode = 0b00

#def read_adc(channel):
	#adc = spi.xfer2([1, (8+channel) << 4 , 0])
	#data = ((adc[1] & 3)<<8) + adc[2]
	#return data


@app.route('/')
def index():
	return render_template('index.html')	
@app.route('/plot')
def plot(which_graph, time_frame):
	conn = sqlite3.connect('sensor_data.db')
	cursor = conn.cursor()
	sqlite3.exectue("SELECT * FROM sensor")
	data = cursor.fetchall()
	conn.close()
	time, voltage, co2, tvoc = zip(*data)
	plt.figure(figsize = (8,5))
	if which_graph == 0:
		plt.plot(time, voltage, color = 'b')
		plt.title(f'Voltage over {time_length}')
		plt.x_label(f'Time ({time_units})')
		plt.y_label('Voltage (mV)')
		plt.grid();
	elif which_graph == 1:
		plt.plot(time, co2, color = 'b')
		plt.title(f'eCO2 over {time_length}')
		plt.x_label(f'Time ({time_units})')
		plt.y_label('eCO2 (ppm)')
		plt.grid()
	elif which_graph == 2:
		plt.plot(time, tvoc, color = 'b')
		plt.title(f'Total Volitile Organic Compounds (TVOC) over {time_length}')
		plt.x_label(f'Time ({time_units})')
		plt.y_label('TVOC (ppb)')
		plt.grid()
	else:
		print("Error invalid graph was chosen")
		exit()

	output = io.BytesIO()
	plt.savefig(output, format='png')
	output.seek(0)
	plt.close()
	return Response(output.getvalue(), mimetype='image/png')

@app.route('/api/sensor_data')
def data_gather():

	#while True:
		#raw_value = read_adc(0)
		#voltage = (raw_value * 5) / 1023.0
		#print("Voltage (v):" + str(voltage))
		#print("eCO2 = %d ppm \t TVOC = %d ppb " % (sgp30.eCO2, sgp30.TVOC))
	
	
	sensor_data = {"MiCS_5524": random.uniform(0,5),
			"SGP30_co2": random.uniform(0,2000),
			"SGP30_tvoc":  random.uniform(0,1000)}
	add_sensor_data(sensor_data["MiCS_5524"],sensor_data["SGP30_co2"], sensor_data["SGP30_tvoc"]) 
	
	return jsonify(sensor_data)

if __name__ == '__main__':
	app.run(debug=True)
