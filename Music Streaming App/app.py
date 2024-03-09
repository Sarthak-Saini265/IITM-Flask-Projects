from flask import Flask, render_template, request, redirect, jsonify
from flask_restful import Api, reqparse, abort
from api.user_resource import new_acc
from api.song_resource import Todo
from api.playlist_resource import create_play
from api.album_resource import new_album
from api.upload_resource import upload_put
from api.ratings_resource import new_rating
from models import db, login, songs, albums, ratings, playlists, playlist_songs, album_songs
import requests

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





@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
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
    return render_template('index_creator.html')

@app.route('/creator/signin', methods=['POST'])
def creator_signin():
    username = request.form['username']
    password = request.form['password']
    user = login.query.filter_by(username=username, acc_type='Creator').first()
    if user:
        if password == user.password:
            return redirect(f'/creator/{username}')
        else:
            return render_template('index_creator.html', trigger_js=True)
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





    
@app.route('/<username>/upload')
def upload(username):
    return render_template('upload_song.html', username=username)


@app.route('/user/<username>')
def user_page(username):
    all_songs = songs.query.all()
    all_playlists = playlists.query.all()
    user = login.query.filter_by(username=username, acc_type='General').first()
    rating = ratings.query.filter_by(user_id=user.user_id).all()
    # print(rating[0].rating)
    if user and user.acc_type == 'General':
        return render_template('user_page.html', username=username, all_songs=all_songs, all_playlists=all_playlists, rating=rating)
    else:
        return 'User not Found'


@app.route('/user/<username>/all_albums')
def all_albums(username):
    all_albums = albums.query.all()
    all_playlists = playlists.query.all()
    return render_template('all_albums.html', username=username, all_albums=all_albums, all_playlists=all_playlists)


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

    return render_template('playlist.html', playlist_songs=playlist_songs, username=username, all_playlists=all_playlists, playlist=playlist)

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

@app.route('/<username>/song/<int:song_id>/update', methods = ['GET', 'POST'])
def update_song(username, song_id):
    song = songs.query.filter_by(song_id=song_id).first()
    return render_template('update_song.html', username=username, song_id=song_id, song=song)

@app.route('/<username>/song/<int:song_id>', methods = ['GET', 'POST'])
def update_song_puter(username, song_id):
    if request.method=="POST":
        form_data = request.form
        file_data = request.files
        print(form_data)
        print(file_data)
        put_data ={}
        for key, value in form_data.items():
            put_data[key] = value
        files = {}
        for key, file in file_data.items():
            files[key] = (file.filename, file)
            put_data[key] = file.filename
            
        if len(files) != 0:
            req = requests.post(f"http://127.0.0.1:5000/files/upload", files=files)
        if req.status_code==200:
            print("Upload Successful")
        response = requests.put(f"http://127.0.0.1:5000/api?username={username}&song_id={song_id}", json=put_data)
        if response.status_code == 200:
            return "Song update Successful"

        return str(response.status_code)


@app.route('/<username>/playlist/<int:playlist_id>/edit')
def update_play(username, playlist_id):
    all_songs = songs.query.all()
    playlist = playlists.query.get(playlist_id)
    playlist_songs = playlist.playlist_songs
    song_ids = []
    for i in playlist_songs:
        song_ids.append(i.song.song_id)
    print(song_ids)
    return render_template('update_playlist.html', username=username, playlist_id=playlist_id, all_songs=all_songs, song_ids=song_ids, playlist=playlist)

@app.route('/<username>/playlist/<int:playlist_id>', methods=['GET', 'POST'])
def update_playlist_puter(username, playlist_id):
    if request.method=="POST":
        put_data = request.form
        print(put_data)
        songs_list = put_data.getlist('songs')

        dic = {
            'name': put_data['name'],
            'songs': songs_list
        }
        print(dic)
        response = requests.put(f"http://127.0.0.1:5000/playlist/update?username={username}&playlist_id={playlist_id}", json=dic)
        if response.status_code == 200:
            return "Playlist update Successful"

        return str(response.status_code)
    
@app.route('/<username>/album/<int:album_id>/edit')
def update_album(username, album_id):
    all_songs = songs.query.all()
    album = albums.query.get(album_id)
    album_songs = album.album_songs
    song_ids = []
    for i in album_songs:
        song_ids.append(i.song.song_id)
    print(song_ids)

    return render_template('update_album.html', all_songs=all_songs, song_ids=song_ids, album_id=album_id, username=username, album=album)

@app.route('/<username>/album/<int:album_id>', methods=['GET', 'POST'])
def update_album_puter(username, album_id):
    if request.method=="POST":
        put_data = request.form
        print(put_data)
        songs_list = put_data.getlist('songs')

        dic = {
            'name': put_data['name'],
            'artist': put_data['artist'],
            'genre': put_data['genre'],
            'songs': songs_list
        }
        print(dic)
        response = requests.put(f"http://127.0.0.1:5000/album/update?username={username}&album_id={album_id}", json=dic)
        if response.status_code == 200:
            return "Album update Successful"

        return str(response.status_code)

@app.route('/<username>/song/<int:song_id>/delete')
def delete_song(username, song_id):
    response = requests.delete(f"http://127.0.0.1:5000/song/delete?username={username}&song_id={song_id}")
    if response.status_code == 200:
            return "Song Deleted Successfully"
    return str(response.status_code)
        
@app.route('/<username>/playlist/<int:playlist_id>/delete')
def delete_playlist(username, playlist_id):
    response = requests.delete(f"http://127.0.0.1:5000/playlist/delete?username={username}&playlist_id={playlist_id}")
    if response.status_code == 200:
            return "Playlist Deleted Successfully"
    return str(response.status_code)

@app.route('/<username>/album/<int:album_id>/delete')
def delete_album(username, album_id):
    response = requests.delete(f"http://127.0.0.1:5000/album/delete?username={username}&album_id={album_id}")
    if response.status_code == 200:
            return "Album Deleted Successfully"
    return str(response.status_code)


@app.route('/<username>/song/<int:song_id>/rating/<int:rating_given>')
def post_rating(username, song_id, rating_given):
    user = login.query.filter_by(username=username).first()
    user_id = user.user_id
    rating  = ratings.query.filter_by(song_id=song_id, user_id=user_id).first()
    if not rating:
        response = requests.post(f"http://127.0.0.1:5000/api/rating?username={username}&song_id={song_id}&rating_given={rating_given}")
        if response.status_code == 200:
            return "Rating Posted Successfully"
        return str(response.status_code)
    else:
        response = requests.put(f"http://127.0.0.1:5000/api/rating?username={username}&song_id={song_id}&rating_given={rating_given}")
        if response.status_code == 200:
                return "Rating Updated Successfully"
        return str(response.status_code)
        






api.add_resource(Todo, "/<username>/song/upload","/api","/song/delete")
api.add_resource(new_acc, "/signup")
api.add_resource(create_play, "/playlist/create/<username>", "/playlist/update", "/playlist/delete")
api.add_resource(new_album, "/album/create/<username>", "/album/update", "/album/delete")
api.add_resource(upload_put, "/files/upload")
api.add_resource(new_rating, "/api/rating")



if __name__ == "__main__":
    app.run(debug=True)


