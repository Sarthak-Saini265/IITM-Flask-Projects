from flask_restful import Resource, reqparse, fields, marshal_with
from models import db, login, songs,playlists, playlist_songs
from flask import request



resource_fields_3 = {
    'name' : fields.String,
    'songs': fields.List(fields.String),
}

play_post_args = reqparse.RequestParser()
play_post_args.add_argument("name", type=str, help = "Playlist Name is required", required = True, location='form')

class create_play(Resource):
    @marshal_with(resource_fields_3)
    def post(self, username):
        l = []
        user = login.query.filter_by(username=username).first()
        args = play_post_args.parse_args()
        songs_selected = request.form.getlist('songs')
        playlist = playlists(user_id=user.user_id, name = args["name"])
        db.session.add(playlist)
        db.session.commit()
        playlist_id = playlist.playlist_id
        for song in songs_selected:
            song_id = int(song)
            play_songs = playlist_songs(playlist_id=playlist_id, song_id=song_id)
            db.session.add(play_songs)
            song_ = songs.query.filter_by(song_id=song_id).first()
            l.append(song_.name)

        playlist_data = {
            'name': playlist.name,
            'songs': l
        }
        db.session.commit()
        return playlist_data
    


