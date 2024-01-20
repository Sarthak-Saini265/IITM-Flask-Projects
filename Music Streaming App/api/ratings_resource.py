from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import db, login, songs, ratings
from flask import request



resource_fields = {
    'rating' : fields.Integer
}


class new_rating(Resource):
    @marshal_with(resource_fields)
    def post(self):
        username = request.args.get("username")
        song_id = request.args.get("song_id")
        rating_given = request.args.get("rating_given")
        if request.method == "POST":
            user = login.query.filter_by(username=username).first()
            song = songs.query.filter_by(song_id=song_id).first()
            rating = ratings(user_id=user.user_id, song_id=song_id, rating=rating_given)
            db.session.add(rating)
            db.session.commit()
            return f'Rating - {rating_given} given to Song - {song.name}'
    




