# import necessary libraries
import os
import sys
import boto3
import json
import os
import psycopg2
import io
import base64
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

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
    index      = db.Column(db.Integer, primary_key=True)
    author  = db.Column('author',db.String, unique=False,index=False )
    title   = db.Column('title', db.String, unique=False,index=False)
    description = db.Column('description',db.String , unique=False,index=False)
    url     = db.Column('url',db.String, unique=False,index=False )
    urlToImage    = db.Column('urltoimage',db.String,unique=False, index=False )
    publishedAt = db.Column('publishedat',db.DateTime, unique=False,index=False )
    articleSummary    = db.Column('articlesummary',db.String,unique=False, index=False )
    articleSentiment    = db.Column('articlesentiment',db.String, unique=False,index=False)
    category        = db.Column('category',db.String, unique=False,index=False )
    source      = db.Column('source',db.String, unique=False,index=False )


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/machinelearning/")
def ml_model():
    return render_template("ml_model.html")

@app.route("/news_dates/")
def news_dates():
    print ("here")
    results = db.session.query(cast(sentiment_results.publishedAt,Date)).distinct().order_by(func.DATE(sentiment_results.publishedAt)).all()
    news_data = []
    for result in results:
        #print ("here")
        #print(result)
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
    print(f'{adate} {category} {sentiment} {limit}')

    results = db.session.query( sentiment_results.title, 
                                sentiment_results.url,
                                sentiment_results.articleSummary,
                                sentiment_results.source,
                                sentiment_results.description,
                                sentiment_results.articleSentiment
                                ).filter(
                                    sentiment_results.category==category,  
                                    sentiment_results.articleSentiment==sentiment,
                                    func.date(sentiment_results.publishedAt)==func.date(adate)
                                ).limit(int(limit)).all()

    news_data = []
    sentences = ""
    for result in results:
        # print(result[0])
        # print(result[4])
        news_data.append({
            'title':result[0],
            'url':result[1],
            'summary':result[2],
            'source':result[3]
        })
        sentences = sentences + " " + result[4]
    img_str = ""
    if len(sentences) > 0 :
        wordcloud = WordCloud(width = 800, height = 500, 
                    background_color ='white', 
                    stopwords = STOPWORDS, 
                    collocations=False,
                    min_font_size = 10).generate(sentences)

        image = wordcloud.to_image()
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # prepare the response: data
    response_data = {"news": news_data, "image": img_str}
    return jsonify(response_data)
    #return jsonify(news_data)

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True    
    app.run()

