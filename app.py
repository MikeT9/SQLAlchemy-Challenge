import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation"""
    # Query by date and prcp
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        date_prcp.append(prcp_dict)

    return jsonify(date_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations

    results = session.query(Station.id, Station.station, Station.name, Station.elevation, Station.latitude, Station.longitude).all()

    # Convert list of tuples into normal list
    station = list(np.ravel(results))
    
    return jsonify(station)

    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    # Query by 12 months of time in tobs
    
    current_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()  

    one_ya = dt.datetime.strptime(current_date[0], '%Y-%m-%d')- dt.timedelta(days=365).strftime('%Y-%m-%d')    

    station_activity = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()  

    sel= [Measurement.date, Measurement.tobs]   

    results = session.query(*sel).filter(Measurement.date>=one_ya).filter(Measurement.station == station_activity).all()

    session.close()

    tobs = list(np.ravel(results))
    
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date >= start).all()

    # Convert list of tuples into normal list
    start_t = list(np.ravel(results))
    
    return jsonify(start_t)

    session.close()

@app.route("/api/v1.0/<start>/<end>")
def range(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all stations

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Convert list of tuples into normal list
    range_t = list(np.ravel(results))
    
    return jsonify(range_t)

    session.close()

if __name__ == '__main__':
    app.run(debug=True)

# I hope this works I didnt have time to test. I want to credit Erin O'brien for significant help aiding me on the code. I am snowballing and reaching out for assistance.