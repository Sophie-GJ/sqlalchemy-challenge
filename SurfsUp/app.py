# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with = engine)

# Save references to each table
m = base.classes.measurement
s = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#slash indicates landing page/home route

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(func.max(m.date)).first()
    last_date = last_date[0]
    prev_year = dt.datetime.strptime(last_date,'%Y-%m-%d').date() - dt.timedelta(365)

    results = session.query(m.date, m.prcp).filter(m.date >= prev_year).all()

    session.close()

    #need to covert results to a dictionary where the precipitation is the variable
    results_dict  = {}
    for tuple in results:
        results_dict[tuple[0]] = tuple[1]
    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(s.station).all()

    session.close()
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(func.max(m.date)).first()
    last_date = last_date[0]
    prev_year = dt.datetime.strptime(last_date,'%Y-%m-%d').date() - dt.timedelta(365)

    tobs_results = session.query(m.date, m.tobs).filter(m.date >= prev_year).all()

    session.close()
    
    return jsonify(tobs_results)



# LAST LINE OF FILE DON'T PUT ANYTHING AFTER THIS
if __name__ == '__main__':
    app.run(debug=True, port=3001)