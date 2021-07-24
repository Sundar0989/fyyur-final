from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.Text())
    facebook_link = db.Column(db.Text())
    genres = db.Column(db.ARRAY(db.String()))
    website = db.Column(db.Text())
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.Text())
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.Text())
    facebook_link = db.Column(db.Text())
    website = db.Column(db.Text())
    seeking_venue = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.Text())
    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True) # added as part of 3 migrate version
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
    

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.