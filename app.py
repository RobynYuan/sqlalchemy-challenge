# 1. Import Flask
import sqlalchemy
from flask import Flask, jsonify
import numpy as np
import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
 
 # set up database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station=Base.classes.station
# Set up Flask
app = Flask(__name__)
# 3. Define static routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2015-08-23/2017-08-23"
    )
@app.route("/api/v1.0/precipitation")

# def precipitation():

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

   #Return a list of record data including the date and precipetation
    date_prcp= session.query(measurement.date,measurement.prcp).all()

    session.close()

    #Convert the query results to a dictionary using date as the key and prcp as the value.
    precipitation = []
    for date, prcp in date_prcp:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
       
        precipitation .append(precipitation_dict)
     #Return the JSON representation of your dictionary.
    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def stations():
# #Return a JSON list of stations from the dataset.
    session = Session(engine)
    # Query all stations
    results = session.query(station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
# ##Query the dates and temperature observations of the most active station for the last year of data.
# #Return a JSON list of temperature observations (TOBS) for the previous year.#
    session = Session(engine)
    # Query all stations
    Temp = session.query(measurement.tobs).filter(measurement.station=='USC00519281').filter(measurement.date>'2016-08-23').all()
    session.close()
    tobs= list(np.ravel(Temp))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start(start=None, end=None):

# #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    session = Session(engine)
        # Query all stations
    Temp_summary = [func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)] 
    Temp = session.query(*Temp_summary).filter(measurement.date >='2016-08-23').all()
    session.close()
    Tem= list(np.ravel(Temp))
    return jsonify(Tem)    
   

# @app.route("/api/v1.0/<start>/<end> ")
@app.route("/api/v1.0/2015-08-23/2017-08-23")
def start_end(start=None, end=None):

# #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    session = Session(engine)
        # Query all stations
    Temp_summary_1 = [func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)] 
    Temp_1= session.query(*Temp_summary_1).filter(measurement.date <'2017-08-23').filter(measurement.date >='2015-08-23').all()
    session.close()
    Tem_1= list(np.ravel(Temp_1))
    return jsonify(Tem_1)

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)




