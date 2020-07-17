#from .app import db


try:
    # Assume we're a sub-module in a package.
    from . import db
except ImportError:
     from app import db


class sentiment_results(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'sentiment_results'
    id = db.Column(db.Integer, primary_key=True   )
    title = db.Column(db.String(64), index=False,unique=True, nullable=False )
    url = db.Column(db.String(64), index=False,unique=True, nullable=False )
    urlToImage    = db.Column(db.String(64), index=False,unique=True, nullable=False )
    publishedAt = db.Column(db.String(64), index=False,unique=True, nullable=False )
    articleSummary    = db.Column(db.String(64), index=False,unique=True, nullable=False )
    articleSentiment    = db.Column(db.String(200), index=False,unique=True, nullable=False )
    category    = db.Column(db.String(64), index=False,unique=True, nullable=False )