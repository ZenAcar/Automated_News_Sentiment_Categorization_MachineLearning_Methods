# import necessary libraries
import os
import boto3
import json
from flask import (
    Flask,
    render_template,
    jsonify,
    request,send_file,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

import sys
print(sys.path)

#################################################
# Database Setup
#################################################

secret_name = "proj/3/db"
region_name = "us-east-2"
access_key = "AKIA2U5PXWUPEETMAONL"
secret_key = "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"

session = boto3.session.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)
client = session.client('secretsmanager')
secret_value = client.get_secret_value(SecretId=secret_name)
def get_connection(secret_value):
  return json.loads(secret_value['SecretString'])
connection = get_connection(secret_value)
# Postgres credentials
jdbcHostname = connection['host']
jdbcPort = connection['port']
jdbcDatabase = "postgres"
dialect = "postgresql"
jdbcUsername = connection['username']
jdbcPassword = connection['password']
jdbcUrl = f"jdbc:{dialect}://{jdbcHostname}:{jdbcPort}/{jdbcDatabase}"
connectionProperties = {
  "user" : jdbcUsername,
  "password" : jdbcPassword,
  "driver" : "org.postgresql.Driver" 
}



from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///static/assets/data/us_unemployment.db"

# # Remove tracking modifications
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# from .models import census
try:
    # Assume we're a sub-module in a package.
    from .models import *
    #from .models import *
except ImportError:
     from models import *


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/census_data/")
def census_data():
    results = db.session.query(census.state, census.variable, census.value).order_by(census.state,census.variable).all()
    census_data = []
    for result in results:
        census_data.append({
            'state': result[0],
            'year':result[1],
            'value':result[2]
        })
   
    # print(jsonify(census_data))
    return jsonify(census_data)


# @app.route("/api/states")
# def states_json():
#     print("hello")
#     return send_file('/static/js/us-states.geojson',mimetype='application/json')    

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run()

