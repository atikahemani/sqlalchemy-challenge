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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurements<br/>"
        f"/api/v1.0/stations<br/>"
    )



#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)
    results=session.query(measurement.date,measurement.prcp).all()
    
    session.close
    
    all_temps=[]
    for date,prcp in results:
        temp_dict={}
        temp_dict["Date"]=date
        temp_dict["Temperature"]=prcp
        all_temps.append(temp_dict)
    return jsonify(all_temps)


@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    results=session.query(Station.station,Station.name).all()
    session.close
    
    stations_list=[]
    for station in results:
        stations_1_dict={}
        stations_1_dict["Station ID"]=station[0]
        stations_1_dict["Station Name"]=station[1]
        stations_list.append(stations_1_dict)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    recent_date=(dt.date(2017, 8 ,23))
    one_year_ago=recent_date-dt.timedelta(days=365)
    session=Session(engine)
    results=session.query(measurement.date,measurement.prcp).\
    filter(measurement.date<=recent_date).filter(measurement.date>=one_year_ago).all()
    
    session.close
    
    temp_previous_year=[]
    for date,prcp in results:
        temp_year={}
        temp_year["Date"]=date
        temp_year["Temperature"]=prcp
        temp_previous_year.append(temp_year)
    return jsonify(temp_previous_year)
    
    

#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.


#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.


#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>")
def start():
    start_date=(dt.date(2017, 6 ,23))
    session=Session(engine)
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    results=session.query(*sel,measurement.date).\
    filter(measurement.date>=start_date).group_by(measurement.tobs).all()
    
                
    session.close
    
    summary_stats=[]
    for tmin, tavg, tmax in results:
        summary_year={}
        summary_year["Min Temp"]=tmin
        summary_year["Max Temp"]=tmax
        summary_year["Avg Temp"]=tavg
        summary_stats.append(summary_year)
    return jsonify(summary_stats)
       
                
         
   
                          
                          




        
if __name__ == '__main__':
    app.run(debug=True)

