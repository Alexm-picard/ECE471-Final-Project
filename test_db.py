import sqlite3

conn = sqlite3.connect('sensor_data.db')
cur = conn.cursor()
def get_posts():
	cur.execute("SELECT * FROM sensor")
	print(cur.fetchall())
	conn.commit()
get_posts()
