

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine('sqlite:///GWDC201805DATA3-Class-Repository-DATA/Homework/09-Adv-Data-Storage-Retrieval (Week 11)/Instructions/Resources/hawaii.sqlite')


Base = automap_base()
Base.prepare(engine,reflect=True)

Base.classes.keys()

session = Session(engine)

Measurement = Base.classes.measurement

Station = Base.classes.station





app = Flask(__name__)

@app.route("/")
def welcome():
    return(
        f" Available Route:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><end>"
        
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    result = session.query(Measurement.prcp).filter(Measurement.date==('2017-08-17')).all()
     
    all_names = list(np.ravel(result))
    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    querys=session.query(Measurement.station).group_by(Measurement.station).all()
    
    return jsonify(querys)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all temperatures on a specific date """
    # Query of temperature
    results = session.query(Measurement.tobs).filter(Measurement.date==('2017-08-17')).all()

    # Convert list of tuples into normal list
    temp = list(np.ravel(results))

    return jsonify(temp)

@app.route("/api/v1.0/start/<start><end>")
def start(start,end):

    if end == " ":
        result= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        return jsonify(result) 

    else:
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        return jsonify(result) 

    

if __name__ == "__main__":
    app.run(debug=True)





