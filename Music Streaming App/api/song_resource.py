from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, songs
from flask import request, current_app
from mutagen.mp3 import MP3
import os
import requests


resource_fields = {
    'name' : fields.String
}

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02d}:{int(seconds):02d}'

class Todo(Resource):
    @marshal_with(resource_fields)
    def post(self, username):
        user = login.query.filter_by(username=username).first()
        lyr = request.files['txt']
        os.makedirs(current_app.config['UPLOAD_FOLDER_TXT'], exist_ok=True)
        lyr_path = os.path.join(current_app.config['UPLOAD_FOLDER_TXT'], lyr.filename)
        print(lyr_path)
        lyr.save(lyr_path)
        with open(f'static/lyrics/{lyr.filename}', 'r', encoding='utf-8') as file_r:
            lyrics_content = file_r.read()
        file = request.files['file']
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
        print(file_path)
        file.save(file_path)
        audio = MP3(file_path)
        duration = audio.info.length
        name = request.form['name']
        creator_id = user.user_id
        song = songs(creator_id = creator_id,name = name, lyrics = lyrics_content, duration = format_duration(duration), path=f'/uploads/{file.filename}')
        db.session.add(song)
        db.session.commit()
        return f'Song Name - {name}\nUploaded Successfully'
    
    @marshal_with(resource_fields)
    def put(self):
        username = request.args.get("username")
        song_id = request.args.get("song_id")
        if  request.method == 'PUT':
            print('Put request fired')
            user = login.query.filter_by(username=username).first()
            if not user:
                abort(404, message='User does not exist. Could not update')

            song = songs.query.filter_by(song_id=song_id, creator_id=user.user_id).first()
            if not song:
                abort(404, message='Song does not exist. Could not update')

            data = request.json
            print(data)
            if "name" in data:
                song.name = data["name"]
            if "txt" in data and data["txt"] != "":
                with open(f'static/lyrics/{data["txt"]}', 'r', encoding='utf-8') as file_r:
                    lyrics_content = file_r.read()
                song.lyrics = lyrics_content
            if "file" in data and data["file"] != "":
                audio = MP3(f'static/uploads/{data["file"]}')
                duration = audio.info.length
                song.duration = format_duration(duration)
                song.path = f'/uploads/{data["file"]}'

            db.session.commit()
        
            updated_data = {
                'message': 'Song updated successfully',
                'song_id': song.song_id,
                'name': song.name,
                'lyrics': song.lyrics,
                'duration': song.duration,
                'path': song.path
            }

        return updated_data
    



