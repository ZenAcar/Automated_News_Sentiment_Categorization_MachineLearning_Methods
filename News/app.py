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
from sqlalchemy import cast, Date
from sqlalchemy.sql import func
from sqlalchemy import desc


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
    author = db.Column(db.String(64), index=False )
    title = db.Column(db.String(64), index=False)
    description = db.Column(db.String(64) , index=False)
    url = db.Column(db.String(64), index=False )
    urlToImage    = db.Column(db.String(64), index=False )
    publishedAt = db.Column(db.DateTime, index=False )
    articleSummary    = db.Column(db.String(200), index=False )
    articleSentiment    = db.Column(db.String(64), index=False)
    category    = db.Column(db.String(64), index=False )
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

    results = db.session.query(sentiment_results.title,publishedAt.url,sentiment_results.articleSentiment,sentiment_results.articleSummary).limit(5).all()
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

@app.route("/news_dates/")
def news_dates():
    print ("here")
    results = db.session.query(cast(sentiment_results.publishedAt,Date)).distinct().order_by(func.DATE(sentiment_results.publishedAt)).all()
    news_data = []
    for result in results:
        #print ("here")
        print(result)
        news_data.append({
            'date':result[0].strftime('%Y/%m/%d')
        })
        news_data.reverse()
    return jsonify(news_data)

@app.route("/news_data/")
def news_data():
    adate = request.args.get('date', None)
    category  = request.args.get('category', None)
    sentiment  = request.args.get('sentiment', None)
    limit  = request.args.get('limit', None)

    print(f'{adate} {category} {sentiment}')

    # print(db.session.query(sentiment_results.articleSummary, sentiment_results.url).filter(sentiment_results.category==category,                                sentiment_results.articleSentiment==sentiment,                                sentiment_results.publishedAt==adate))
    results = db.session.query(sentiment_results.articleSummary, sentiment_results.url).filter(sentiment_results.category==category).limit(limit).all()
                                # sentiment_results.articleSentiment==sentiment,
                                #sentiment_results.publishedAt==adate).all()
    news_data = []
    for result in results:
        print(result)
        news_data.append({
            'summary':result[0],
            'url':result[0]
        })
        
    return jsonify(news_data)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run()

