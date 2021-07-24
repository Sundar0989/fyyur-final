#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from typing import DefaultDict
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from sqlalchemy.sql.functions import coalesce
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case
import logging
from logging import Formatter, FileHandler, NullHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import array_agg
import os 
from collections import OrderedDict, defaultdict
from models import *
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

# db.create_all()


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  venues = Venue.query.with_entities(Venue.id, Venue.city, Venue.state, Venue.name).order_by(Venue.id).all() # get the data from venues
  upcoming_shows = Venue.query.outerjoin(Show) \
                  .with_entities(Venue.id, func.sum(case([(Show.start_time>datetime.now(), 1)], else_=0)).label('num_upcoming_shows')) \
                  .group_by(Venue.id).order_by(Venue.id).all() # aggregate show by venues
  list_output = [list(a) + [b[1]] for a, b in zip(venues, upcoming_shows)] # combine both the lists based on venue id

  # create the data list
  d = defaultdict(list) 
  for i in list_output:
    d[(i[1], i[2])].append({"id":i[0], "name": i[3], "num_upcoming_shows": i[4]})
  data = [{'city': city, 'state':state, 'venues': venues} for (city, state), venues in d.items()]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  venue_search = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike("%" + search_term + "%")).order_by(Venue.id).all()
  upcoming_shows = Venue.query.outerjoin(Show).filter(Venue.name.ilike("%" + search_term + "%")) \
                  .with_entities(Venue.id, func.sum(case([(Show.start_time>datetime.now(), 1)], else_=0)).label('num_upcoming_shows')) \
                  .group_by(Venue.id).order_by(Venue.id).all()
  list_output = [list(a) + [b[1]] for a, b in zip(venue_search, upcoming_shows)] # combine both the lists based on venue id
  names = ['id', 'name', 'num_upcoming_shows']
  data = [dict(zip(names, i)) for i in list_output]
  response = {
    "count" : len(data),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue_search = Venue.query.filter(Venue.id == venue_id).all()[0]
  shows = Show.query.join(Artist).with_entities(Show.artist_id, Artist.name, Artist.image_link, Show.start_time).filter(Show.venue_id == venue_id)
  pa_shows = shows.filter(Show.start_time<datetime.now()).all()
  up_shows = shows.filter(Show.start_time>datetime.now()).all()

  def find_show_and_counts(sub_shows):

    if len(sub_shows) > 0:
      shows_count = len(sub_shows)
      filter_shows = []
      for i in sub_shows:
        f_show = {
          "artist_id": i.artist_id,
          "artist_name": i.name,
          "artist_image_link": i.image_link,
          "start_time": str(i.start_time)
        }
        filter_shows.append(f_show)
    else:
      shows_count = 0
      filter_shows = []
    return shows_count, filter_shows

  past_shows_count, past_shows = find_show_and_counts(pa_shows)
  upcoming_shows_count, upcoming_shows = find_show_and_counts(up_shows)

  data = {
    'id': venue_id,
    'name': venue_search.name,
    'genres': venue_search.genres,
    'address': venue_search.address,
    'city': venue_search.city,
    'state': venue_search.state,
    'phone': venue_search.phone,
    'website': venue_search.website,
    'facebook_link': venue_search.facebook_link,
    'seeking_talent': venue_search.seeking_talent,
    'seeking_description': venue_search.seeking_description,
    'image_link': venue_search.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': past_shows_count,
    'upcoming_shows_count': upcoming_shows_count
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  try:
    data = {
    'name' : request.form['name'], 
    'city' : request.form['city'], 
    'state' : request.form['state'], 
    'address' : request.form['address'], 
    'phone' : request.form['phone'], 
    'image_link' : request.form['image_link'], 
    'facebook_link' : request.form['facebook_link'], 
    'genres' : request.form.getlist('genres'), 
    'website' : request.form['website_link'], 
    'seeking_talent' : True if 'seeking_talent' in request.form else False,
    'seeking_description' : request.form['seeking_description']
  }
    venue = Venue(**data)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')
  else:
    flash('Venue ' + venue_id + ' was successfully deleted')
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.id).all()
  names = ['id', 'name']
  data = [dict(zip(names, i)) for i in artists]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  artist_search = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike("%" + search_term + "%")).order_by(Artist.id).all()
  upcoming_shows = Artist.query.outerjoin(Show).filter(Artist.name.ilike("%" + search_term + "%")) \
                  .with_entities(Artist.id, func.sum(case([(Show.start_time>datetime.now(), 1)], else_=0)).label('num_upcoming_shows')) \
                  .group_by(Artist.id).order_by(Artist.id).all()
  list_output = [list(a) + [b[1]] for a, b in zip(artist_search, upcoming_shows)] # combine both the lists based on venue id
  names = ['id', 'name', 'num_upcoming_shows']
  data = [dict(zip(names, i)) for i in list_output]
  response = {
    "count" : len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist_search = Artist.query.filter(Artist.id == artist_id).all()[0]
  shows = Show.query.join(Venue).with_entities(Show.venue_id, Venue.name, Venue.image_link, Show.start_time).filter(Show.artist_id == artist_id)
  pa_shows = shows.filter(Show.start_time<datetime.now()).all()
  up_shows = shows.filter(Show.start_time>datetime.now()).all()

  def find_show_and_counts(sub_shows):

    if len(sub_shows) > 0:
      shows_count = len(sub_shows)
      filter_shows = []
      for i in sub_shows:
        f_show = {
          "venue_id": i.venue_id,
          "venue_name": i.name,
          "venue_image_link": i.image_link,
          "start_time": str(i.start_time)
        }
        filter_shows.append(f_show)
    else:
      shows_count = 0
      filter_shows = []
    return shows_count, filter_shows

  past_shows_count, past_shows = find_show_and_counts(pa_shows)
  upcoming_shows_count, upcoming_shows = find_show_and_counts(up_shows)

  data = {
  'id': artist_search.id,
  'name': artist_search.name,
  'city': artist_search.city,
  'state': artist_search.state,
  'phone': artist_search.phone,
  'genres': artist_search.genres,
  'image_link': artist_search.image_link,
  'facebook_link': artist_search.facebook_link,
  'website': artist_search.website,
  'seeking_venue': artist_search.seeking_venue,
  'seeking_description': artist_search.seeking_description,
  'past_shows': past_shows,
  'upcoming_shows': upcoming_shows,
  'past_shows_count': past_shows_count,
  'upcoming_shows_count': upcoming_shows_count
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.image_link.data = artist.image_link
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  artist = Artist.query.get(artist_id)
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website_link']
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']
    db.session.merge(artist)
    db.session.commit()
    print(artist.__dict__)
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  form.genres.data = venue.genres
  form.website_link.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = request.form.getlist('genres')
    venue.website = request.form['website_link']
    venue.seeking_talent = True if 'seeking_talent' in request.form else False
    venue.seeking_description = request.form['seeking_description']
    db.session.merge(venue)
    db.session.commit()
    print(venue.__dict__)
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  try:
    data = {
    'name' : request.form['name'], 
    'city' : request.form['city'], 
    'state' : request.form['state'], 
    'phone' : request.form['phone'], 
    'genres' : request.form.getlist('genres'), 
    'image_link' : request.form['image_link'], 
    'facebook_link' : request.form['facebook_link'], 
    'website' : request.form['website_link'], 
    'seeking_venue' : True if 'seeking_venue' in request.form else False, 
    'seeking_description' : request.form['seeking_description']
  }
    artist = Artist(**data)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  shows_data = Show.query.join(Venue).join(Artist) \
                  .with_entities(Show.venue_id, Venue.name, Show.artist_id, Artist.name, Artist.image_link, Show.start_time).all() # Shows
  names = ['venue_id', 'venue_name', 'artist_id', 'artist_name', 'artist_image_link', 'start_time']
  data = [dict(zip(names, i)) for i in shows_data]
  for i in data:
    i['start_time'] = str(i['start_time'])

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  try:
    data = {
    'artist_id' : request.form['artist_id'], 
    'venue_id' : request.form['venue_id'], 
    'start_time' : request.form['start_time']
  }
    show = Show(**data)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  
  # error handling
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

