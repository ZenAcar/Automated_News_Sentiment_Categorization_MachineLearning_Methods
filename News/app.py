# import necessary libraries
import os
import sys
import boto3
import json
import os
import psycopg2

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



from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
# # Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    databaseconnection()
    return render_template("index.html")
    

def databaseconnection():
    DATABASE_URL = os.environ['DATABASE_URL']
    print(DATABASE_URL)

@app.route("/test/")
def test():

    results = db.session.query(sentiment_results.title,sentiment_results.url,sentiment_results.articleSentiment,sentiment_results.articleSummary).limit(5).all()
    news_data = []
    for result in results:
        #print ("here")
        #print(result)
        news_data.append({
            'Title':result[0],
            'url':result[1],
            'sentiment':result[2],
            'summary':result[3]

        })
        
    return jsonify(news_data)


    
# @app.route("/census_data/")
# def census_data():
#     results = db.session.query(census.state, census.variable, census.value).order_by(census.state,census.variable).all()
#     census_data = []
#     for result in results:
#         census_data.append({
#             'state': result[0],
#             'year':result[1],
#             'value':result[2]
#         })
   
#     # print(jsonify(census_data))
#     return jsonify(census_data)


  

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run()

