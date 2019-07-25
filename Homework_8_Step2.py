# import Flask, others
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into aR new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################

# Create the app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def Home():
    return (
        f"Welcome to the Climate App Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


# Define what to do when a user hits the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of precipitation data including the date and precipitation values."""
    
    # Query precipitation data
    precip_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    # Create a dictionary and append list of precip data
    precipitation = []
    for date, prcp in precip_data:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

# Define what to do when a user hits the stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations and counts in descending order."""
    
    # Query precipitation data
    stations_desc = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    # Create a dictionary and append list of stations data
    stations = []
    for station, count in stations_desc:
        stations_dict = {}
        stations_dict["_station"] = station
        stations_dict["count"] = count
        stations.append(stations_dict)

    return jsonify(stations)

# Define what to do when a user hits the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of stations, dates, temps observed for the past year."""
    
    # Query precipitation data
    tobs_data = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    # Create a dictionary and append list of stations data
    tobs_list = []
    for station, date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

# Define what to do when a user hits the start route
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return tmin, tavg, tmax for all dates greater than or equal to the start date"""
    
    # Query temp data
    temp_data = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), 
                    func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Create a dictionary and append list of temps data
    temps_list = []
    
    for station, date, min, max, avg in temp_data:
        temps_dict = {}
        temps_dict["_station"] = station
        temps_dict["_date"] = date
        temps_dict["min"] = min
        temps_dict["max"] = max
        temps_dict["avg"] = avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)

# Define what to do when a user hits the start/end route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    """Return tmin, tavg, tmax for all dates greater than or equal to the start date and less than or equal to end date"""
    
    # Query temp data
    temp_data = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs), 
                    func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter((Measurement.date >= start) & (Measurement.date <= end)).all()

    # Create a dictionary and append list of temps data
    temps_list = []
    
    for station, date, min, max, avg in temp_data:
        temps_dict = {}
        temps_dict["_station"] = station
        temps_dict["_date"] = date
        temps_dict["min"] = min
        temps_dict["max"] = max
        temps_dict["avg"] = avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)


if __name__ == "__main__":
    app.run(debug=True)