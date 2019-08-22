import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Surf's Up Dude..Come view the stats!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    """Return the JSON representation of your dictionary"""
    # Query all precipitation results
    
    results = session.query(Measurement.date, Measurement.prcp).\
     filter(func.strftime("%Y-%m-%d", Measurement.date) >=dt.date(2016,8,23)).all()
    
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB

    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.name).all()
    station_name = list(np.ravel(results))
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB

    """Return a JSON list of Temperature Observations (tobs) for the previous year"""
    # Query for the dates and temperature observations from a year from the last data point.
    results = session.query(Measurement.date,Measurement.tobs).\
            filter(func.strftime("%Y-%m-%d", Measurement.date) >=dt.date(2016,8,23)).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start_date):
    # Create our session (link) from Python to the DB
  
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    # Query Min, Max Avg for all dates greater than and equal to start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date,end_date):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    def calc_temps(start_date, end_date):

            return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    results = calc_temps(start_date,end_date)
    
    # Query Min, Max Avg for all dates greater than and equal to start date

    return jsonify(results)
    # Create our session (link) from Python to the DB
    
if __name__ == '__main__':
    app.run(debug=True)
