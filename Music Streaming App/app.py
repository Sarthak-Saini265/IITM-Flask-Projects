from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from mutagen.mp3 import MP3
from models import db, login, songs, albums, ratings, playlists, playlist_songs, album_songs
import os


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///music_streaming_app.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER_TXT = 'static/lyrics'
app.config['UPLOAD_FOLDER_TXT'] = UPLOAD_FOLDER_TXT
app.app_context().push()





# db.create_all()
# song = songs.query.filter_by(song_id=1).first()
# db.session.delete(song)
# album = albums.query.filter_by(album_id=1).first()
# db.session.delete(album)
# db.session.query(albums).delete()
# db.session.query(album_songs).delete()
# db.session.commit()
# db.session.query(songs).delete()
# db.session.commit()
# add_song = songs(name='Star Sky', lyrics=lyrics_content, duration='05:35', mp3='/uploads/Two Steps From Hell - Star Sky.mp3')
# db.session.add(add_song)
# db.session.commit()
# dele = songs.query.filter_by(song_id=3).first()
# db.session.delete(dele)
# db.session.commit()


resource_fields_2 = {
    'username' : fields.String,
    'password' : fields.String,
}

acc_post_args = reqparse.RequestParser()
acc_post_args.add_argument("username", type=str, help = "Username is required", required = True, location='form')
acc_post_args.add_argument("password", type=str, help = "Password is required", required = True, location='form')


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    # add = login(username=username, password=password, acc_type='General')
    # db.session.add(add)
    # db.session.commit()
    user = login.query.filter_by(username=username).first()
    if user:
        if password == user.password:
            return redirect(f'/user/{username}')
        else:
            return render_template('index.html', trigger_js=True)
    else:
        return render_template('index.html', trigger_js_2=True)
    
@app.route('/create_account')
def create_account():
    return render_template('user_sign_up.html')

class new_acc(Resource):
    @marshal_with(resource_fields_2)
    def post(self):
        args = acc_post_args.parse_args()
        new = login(username = args["username"], password = args["password"], acc_type = 'General')
        db.session.add(new)
        db.session.commit()
        return new
    


# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     password = request.form['password']
#     try:
#         add = login(username=username, password=password, acc_type='General')
#         db.session.add(add)
#         db.session.commit()
#         return redirect(f'/user/{username}')
#     except:
#         return render_template('user_sign_up.html', trigger_js=True)


    
@app.route('/creator')
def creator():
    return render_template('creator_login.html')

@app.route('/creator/signin', methods=['POST'])
def creator_signin():
    username = request.form['username']
    password = request.form['password']
    user = login.query.filter_by(username=username, acc_type='Creator').first()
    if user:
        if password == user.password:
            return redirect(f'/creator/{username}')
        else:
            return render_template('creator_login.html', trigger_js=True)
    else:
        add = login(username=username, password=password, acc_type='Creator')
        db.session.add(add)
        db.session.commit()
        return redirect(f'/creator/{username}')
    
@app.route('/creator/<username>')
def creator_page(username):
    user = login.query.filter_by(username=username).first()
    uploaded_songs = songs.query.filter_by(creator_id=user.user_id)
    print(uploaded_songs)
    return render_template('creator_page.html', username=username, uploaded_songs=uploaded_songs)

resource_fields = {
    'name' : fields.String
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type=str, help = "Name is required", required = True)

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'

class Todo(Resource):
    @marshal_with(resource_fields)
    def post(self, username):
        user = login.query.filter_by(username=username).first()
        lyr = request.files['txt']
        os.makedirs(app.config['UPLOAD_FOLDER_TXT'], exist_ok=True)
        lyr_path = os.path.join(app.config['UPLOAD_FOLDER_TXT'], lyr.filename)
        print(lyr_path)
        lyr.save(lyr_path)
        with open(f'static/lyrics/{lyr.filename}', 'r', encoding='utf-8') as file_r:
            lyrics_content = file_r.read()
        file = request.files['file']
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(file_path)
        file.save(file_path)
        audio = MP3(file_path)
        duration = audio.info.length
        name = request.form['name']
        creator_id = user.user_id
        # print('njndjkasnsknasdkwmswk')
        song = songs(creator_id = creator_id,name = name, lyrics = lyrics_content, duration = format_duration(duration), path=f'/uploads/{file.filename}')
        db.session.add(song)
        db.session.commit()
        return f'Song Name - {name}\nUploaded Successfully'

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

    
@app.route('/<username>/upload')
def upload(username):
    return render_template('upload_song.html', username=username)


@app.route('/user/<username>')
def user_page(username):
    all_songs = songs.query.all()
    all_playlists = playlists.query.all()
    user = login.query.filter_by(username=username, acc_type='General').first()
    if user and user.acc_type == 'General':
        return render_template('user_page.html', username=username, all_songs=all_songs, all_playlists=all_playlists)
    else:
        return 'User not Found'

@app.route('/user/<username>/new_playlist')
def create_playlist(username):
    all_songs = songs.query.all()
    return render_template('create_playlist.html', username=username, all_songs=all_songs)

@app.route('/user/<username>/playlist/<int:playlist_id>')
def get_songs_by_playlist(username, playlist_id):
    all_playlists = playlists.query.all()
    playlist = playlists.query.get(playlist_id)

    if not playlist:
        return abort('error: Playlist not found'), 404

    playlist_songs = playlist.playlist_songs

    return render_template('playlist.html', playlist_songs=playlist_songs, username=username, all_playlists=all_playlists)

@app.route('/<username>/albums')
def page(username):
    user = login.query.filter_by(username=username).first()
    all_albums = albums.query.filter_by(creator_id=user.user_id)
    return render_template('manage_albums.html', username=username, all_albums=all_albums)

@app.route('/<username>/create_album')
def page_2(username):
    user = login.query.filter_by(username=username).first()
    uploaded_songs = songs.query.filter_by(creator_id=user.user_id)
    return render_template('create_album.html', username=username, uploaded_songs=uploaded_songs)

@app.route('/creator/<username>/album/<int:album_id>')
def get_songs_by_album(username, album_id):
    album = albums.query.get(album_id)

    if not album:
        return abort('error: Album not found'), 404
    album_name = album.name
    album_songs = album.album_songs

    return render_template('album.html', album_songs=album_songs, username=username, album_name=album_name)

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






api.add_resource(Todo, "/<username>/song/upload")
api.add_resource(new_acc, "/signup")
api.add_resource(create_play, "/playlist/create/<username>")
api.add_resource(new_album, "/album/create/<username>")


if __name__ == "__main__":
    app.run(debug=True)


