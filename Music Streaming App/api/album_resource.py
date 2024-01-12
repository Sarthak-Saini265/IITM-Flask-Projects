from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, login, songs, albums, album_songs
from flask import request



resource_fields_4 = {
    'name' : fields.String,
    'artist' : fields.String,
    'genre' : fields.String,
    'songs' : fields.List(fields.String),
}

album_post_args = reqparse.RequestParser()
album_post_args.add_argument("name", type=str, help = "Album Name is required", required = True, location='form')
album_post_args.add_argument("artist", type=str, help = "Artist Name is required", required = True, location='form')
album_post_args.add_argument("genre", type=str, help = "Genre is required", required = True, location='form')

class new_album(Resource):
    @marshal_with(resource_fields_4)
    def post(self, username):
        l = []
        user = login.query.filter_by(username=username).first()
        args = album_post_args.parse_args()
        songs_selected = request.form.getlist('songs')
        album = albums(creator_id = user.user_id, name = args['name'], artist = args['artist'], genre = args['genre'])
        db.session.add(album)
        db.session.commit()
        album_id = album.album_id
        print(songs_selected)
        for song in songs_selected:
            song_id = int(song)
            print(f"Processing song_id: {song_id}")
            album_song = album_songs(album_id=album_id, song_id=song_id)
            db.session.add(album_song)
            song_ = songs.query.filter_by(song_id=song_id).first()
            l.append(song_.name)
        album_data = {
            'name': album.name,
            'artist' : album.artist,
            'genre' : album.genre,
            'songs': l
        }
        db.session.commit()
        return album_data
    





