from flask_restful import Resource, reqparse, fields, marshal_with, abort
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
    
    @marshal_with(resource_fields_3)
    def put(self):
        username = request.args.get("username")
        playlist_id = request.args.get("playlist_id")

        if request.method=="PUT":
            user = login.query.filter_by(username=username).first()
            if not user:
                abort(404, message='User does not exist. Could not update')

            playlist = playlists.query.get(playlist_id)
            if not playlist:
                abort(404, message='Song does not exist. Could not update')
            data = request.json
            print(data)
            songs_ids = [int(song_id) for song_id in data.get("songs", [])]
            playlist.name=data["name"]
            db.session.query(playlist_songs).filter_by(playlist_id=playlist_id).delete()

            for song_id in songs_ids:
                new_association = playlist_songs(playlist_id=playlist_id, song_id=song_id)
                db.session.add(new_association)

            db.session.commit()
            playlist_data = {
                'name': playlist.name,
                'songs': data["songs"]
            }
            db.session.commit()
            return playlist_data

    def delete(self):
        playlist_id = request.args.get("playlist_id")
        playlist = playlists.query.filter_by(playlist_id=playlist_id).first()
        print(playlist)
        if not playlist:
            abort('This Playlist does not exist. Could Not Delete')
        db.session.delete(playlist)
        playl_songs = playlist_songs.query.filter_by(playlist_id=playlist_id)
        print(list(playl_songs))
        for song in playl_songs:
            db.session.delete(song)
        db.session.commit()
        return "Playlist Deleted Successfully"
    


