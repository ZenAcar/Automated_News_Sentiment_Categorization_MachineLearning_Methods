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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('AWS_DATABASE_URL', '')
# # Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class sentiment_results(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'sentiment_results'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(64), index=False,unique=True, nullable=False )
    title = db.Column(db.String(64), index=False,unique=True, nullable=False )
    description = db.Column(db.String(64), index=False,unique=True, nullable=False )
    url = db.Column(db.String(64), index=False,unique=True, nullable=False )
    urlToImage    = db.Column(db.String(64), index=False,unique=True, nullable=False )
    publishedAt = db.Column(db.DateTime, index=False,unique=True, nullable=False )
    articleSummary    = db.Column(db.String(200), index=False,unique=True, nullable=False )
    articleSentiment    = db.Column(db.String(64), index=False,unique=True, nullable=False )
    category    = db.Column(db.String(64), index=False,unique=True, nullable=False )
# # from .models import census
# try:
#     # Assume we're a sub-module in a package.
#     from .models import *
#     #from .models import *
# except ImportError:
#     print("why are we hree?")
#     from models import *


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

