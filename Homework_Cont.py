import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)
# Flask Routes

@app.route("/")
def welcome():
    """List of API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"\
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/measurement")
def precip():
    "Return a list of dates with total precipitation"
    # Query all measurements
    results = session.query(Measurement).all()

    # Create a dictionary from the row data and append to a list of all_msr
    all_msr = []
    for result in results:
        msr_dict = {}
        msr_dict["date"] = Measurement.date
        msr_dict["prcp"] = Measurement.prcp
        all_msr.append(msr_dict)

    return jsonify(all_msr)

if __name__ == '__main__':
    app.run(debug=True)