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

class upload_put(Resource):
    @marshal_with(resource_fields)
    def post(self):
        data = request.files
        if "txt" in data:
            lyr = data["txt"]
            os.makedirs(current_app.config['UPLOAD_FOLDER_TXT'], exist_ok=True)
            lyr_path = os.path.join(current_app.config['UPLOAD_FOLDER_TXT'], lyr.filename)
            print(lyr_path)
            lyr.save(lyr_path)
        if "file" in data:
            file = data["file"]
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
            print(file_path)
            file.save(file_path)
        return f'Song Uploaded Successfully'
    
