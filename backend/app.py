from flask import Flask, jsonify
import psycopg2
from psycopg2 import Error
from datetime import date
from flask_cors import CORS
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib


# Common connection for all functions
conn = None
try:
    print('Connecting to PostgreSQL database...')
    conn = psycopg2.connect(
    host="localhost",
    database="chicago_business_intelligence",
    user="postgres",
    password="root")
    cursor = conn.cursor()
    print('Cursor set...')
except:
    print('Unable to connect to PostgreSQL connection URL...')

app = Flask(__name__)
CORS(app)



@app.route('/buildingPermit', methods=['GET'])
def get_permits_data():
    cursor.execute("SELECT * from buildingpermits")
    data = cursor.fetchall()
    return jsonify(data)


@app.route('/unEmployment', methods=['GET'])
def get_unemp_data():
    cursor.execute('select "areaCode", "areaName", "belowPoverty" from unemployment_data order by "belowPoverty" desc limit 5;')
    top5_poverty = cursor.fetchall()
    cursor.execute('select "areaCode", "areaName", "unempRate" from unemployment_data order by "unempRate" desc limit 5;')
    top5_unemp = cursor.fetchall()
    shape = gpd.read_file('./datasets/Comm20Areas/CommAreas.shp')
    # print(shape)
    ax = shape.boundary.plot(figsize = (10,5))
    matplotlib.use('SVG')
    shape.plot(ax=ax, column="AREA_NUMBE", legend=False, cmap='OrRd')
    plt.savefig("./datasets/results/chicago_map.png")
    return jsonify(top5_poverty,top5_unemp)
    
    
@app.route('/ccvi', methods=['GET'])
def get_ccvi_data():
    cursor.execute("SELECT * from ethnicitycovid19")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/taxiTrips', methods=['GET'])
def get_trips_data():
    cursor.execute("SELECT * from taxitrips")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/covid19', methods=['GET'])
def get_covid19_daily_data():
    cursor.execute("SELECT * from healthhumanservices")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/covid19Zip', methods=['GET'])
def get_covid19_weekly_data():
    cursor.execute("SELECT * from covid19")
    data = cursor.fetchall()
    return jsonify(data)