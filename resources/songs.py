import models

# This is like a route in an Exprees application
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

# Playhouse is part of PeeWee.  Converts data from DB to a dictionary (in this case).  There are also other options like 'model to list'
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name.  It is used to import this into other files.  Not as straight forward as Node.
song = Blueprint('songs', 'song')

# Get (index route)
@song.route('/', methods=["GET"])
def get_all_songs():
    ## find the song and change each one to a dictionary into a new array
    try:
        # Comprehension list.  select() is a PeeWee reserver word
        songs = [model_to_dict(song) for song in models.Song.select()]
        print(songs)
        # model_to_dict(song) - is a function that will change our Model object (song) to a Dictionary class, - We have to do this because we cannot jsonify something from a "Model" class, so in order to respond to the client we must change our datatype from a Model Class to a Dictionary Class instance
        return jsonify(data=songs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


# Show Route
@song.route('/<id>', methods=["GET"])
# This will ensure only a logged in user can get to this route
@login_required 
def get_one_song(id):
    print(id, 'reserved word?')
    song = models.Song.get_by_id(id)
    print(song.__dict__)
    return jsonify(data=model_to_dict(song), status={"code": 200, "message": "Success"})

# Update Route
@song.route('/<id>', methods=["PUT"])
def update_song(id):
    payload = request.get_json()
    # **payload allows us to update mutiple properites at once
    query = models.Song.update(**payload).where(models.Song.id==id)
    query.execute()
    return jsonify(data=model_to_dict(models.Song.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})


# Post Route (create)
@song.route('/', methods=["POST"])
def create_songs():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    #  PeeWee method to create row
    # ** is like the spread operator (can accept as many args as you want).  It will align everything so it corresponds to the correct field in the DB.  This is an alternative:
    # song = models.Song.create(album=payload['album'], artist=payload["artist"], title=payload["title"])
    song = models.Song.create(**payload)
    ## see the object
    print(song.__dict__)
    ## Look at all the methods
    print(dir(song))
    # Change the model to a dict
    print(model_to_dict(song), 'model to dict')
    song_dict = model_to_dict(song)
    return jsonify(data=song_dict, status={"code": 201, "message": "Success"})

# Delete route
@song.route('/<id>', methods=["Delete"])
def delete_song(id):
    query = models.Song.delete().where(models.Song.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})