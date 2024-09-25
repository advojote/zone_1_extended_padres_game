"""
Elder Coxson
Import missionaries and areas from imos
"""

import csv
import mysql.connector
import dotenv
import os

dotenv.load_dotenv()

mydb = mysql.connector.connect(
    host='localhost',
    user=os.environ['DATABASE_USERNAME'],
    password=os.environ['DATABASE_PASSWORD'],
    database='zone_1_game_data',
)

areas = {}
districts = {}

cursor = mydb.cursor()

# Get the areas
cursor.execute('SELECT * FROM areas')
res = cursor.fetchall()
for area in res:
    areas[area[1]] = area[0]

# Get the districts
cursor.execute('SELECT * FROM districts')
res = cursor.fetchall()
for district in res:
    districts[district[1]] = district[0]

with open('padres.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        zone = int(row[2][5])
        district = districts.get(row[3])
        if district is None:
            cursor.execute(
                'INSERT INTO districts (name) VALUES (%s)', (row[3],)
            )
            cursor.execute('SELECT LAST_INSERT_ID()')
            districts[row[3]] = cursor.fetchone()[0]
            district = districts[row[3]]
        area = areas.get(row[4])
        if area is None:
            cursor.execute('INSERT INTO areas (name) VALUES (%s)', (row[4],))
            cursor.execute('SELECT LAST_INSERT_ID()')
            areas[row[4]] = cursor.fetchone()[0]
            area = areas[row[4]]
        print(row[0], area, district, zone)
        cursor.execute(
            'REPLACE INTO missionaries VALUES (%s, %s, %s, %s)',
            (row[0], area, district, zone),
        )
mydb.commit()
