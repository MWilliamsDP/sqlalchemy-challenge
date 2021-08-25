#import dependencies (same as notebook, plus Flask)
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np
import pandas as pd

# Set up Database (same as notebook)
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station
session = Session(engine)

# Set up Flask
app=Flask(__name__)

#Routes
@app.route("/")
def home():
   return (
        f'Welcome to my Climate App<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/end'
        )


@app.route("/api/v1.0/precipitation")
def preciptiation():
    session = Session(engine)
    results =   session.query(Measurement.date, Measurement.prcp).all()
    
    Precipitation = []
    for date, prcp in results:
        new_dict = {}
        new_dict[date] = prcp
        Precipitation.append(new_dict)

    session.close()

    return jsonify(Precipitation)
    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    Stations =   session.query(Station.station, Station.name).all()
    
    session.close()
    return jsonify()

@app.route("/api/v1.0/tobs")
def TOBS():
    session = Session(engine)
    ObsTemps =   session.query(Measurement.tobs, Measurement.date).filter(Measurement.date>= "2016-08-23").all()
    
    session.close()
    return jsonify()

#I'm not entirely sure of how to run these last two
@app.route("/api/v1.0/start")
def start():
    session = Session(engine)
    startDate = dt.datetime.strptime(start, '%Y-%m-%d')
    session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= startDate).all()
    
    session.close()



@app.route("/api/v1.0/end")
def end ():


    session.close()  

if __name__=="__main__":
    app.run(debug=True)