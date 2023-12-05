from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.app_context().push()



app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///music_streaming_app.sqlite3"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class login(db.Model):
    ID = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(20), unique = True, nullable = False)
    acc_type = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"{self.ID}-{self.username} {self.password} {self.acc_type}"

class songs(db.Model):
    song_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30), unique = False, nullable = False)
    lyrics = db.Column(db.Text, unique = False, nullable = False)
    duration = db.Column(db.String(15), nullable = False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'), nullable=True, default=None)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    mp3 = db.Column(db.String(255), nullable=False, unique=False)

    album = db.relationship('albums', backref=db.backref('songs', lazy=True))

    def __repr__(self):
        return f"{self.song_id}-{self.name} {self.duration} {self.date_created}"   

class albums(db.Model):
    album_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30), unique = False, nullable = False)
    artist = db.Column(db.String(30), unique = False, nullable = False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f"{self.song_id}-{self.name} {self.duration} {self.date_created}"   

# db.create_all()

with open('static/python_questions.txt', 'r') as file:
    lyrics_content = file.read()
# db.session.query(songs).delete()
# db.session.commit()
# add_song = songs(name='Star Sky', lyrics=lyrics_content, duration='05:35', mp3='/uploads/Two Steps From Hell - Star Sky.mp3')
# db.session.add(add_song)
# db.session.commit()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def products():
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
    return render_template('creator_page.html', username=username)

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'lyrics' : fields.String,
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type=str, help = "Name is required", required = True)
task_post_args.add_argument("lyrics", type=str, help = "lyrics are required", required = True)

class Todo(Resource):
    @marshal_with(resource_fields)
    def post(self, song_id):
        args = task_post_args.parse_args()
        task = songs.query.filter_by(song_id=song_id).first()
        if task:
            abort(409, message = "This song Id is taken")
        song = songs(song_id=song_id, name = args["name"], lyrics = args["lyrics"], duration = '03:34', mp3 = '/uploads/snsms.mp3')
        db.session.add(song)
        db.session.commit()
        return song
    



@app.route('/user/<username>')
def user_page(username):
    all_songs = songs.query.all()
    user = login.query.filter_by(username=username, acc_type='General').first()
    if user and user.acc_type == 'General':
        return render_template('user_page.html', username=username, all_songs=all_songs)
    else:
        return 'User not Found'


api.add_resource(Todo, "/song/<int:song_id>")



if __name__ == "__main__":
    app.run(debug=True)


