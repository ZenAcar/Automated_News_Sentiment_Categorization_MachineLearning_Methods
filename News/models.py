#from .app import db


try:
    # Assume we're a sub-module in a package.
    from .app import db
except ImportError:
     from app import db


