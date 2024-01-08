from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class login(db.Model):
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(20), unique = True, nullable = False)
    acc_type = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"{self.user_id}-{self.username} {self.password} {self.acc_type}"

class songs(db.Model):
    song_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30), unique = False, nullable = False)
    lyrics = db.Column(db.Text, unique = False, nullable = False)
    duration = db.Column(db.String(15), nullable = False)
#    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'), nullable=True, default=None)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    path = db.Column(db.String(255), nullable=False, unique=True)

#    album = db.relationship('albums', backref=db.backref('songs', lazy=True))

    def __repr__(self):
        return f"{self.song_id}-{self.name} {self.duration} {self.date_created}"   

class albums(db.Model):
    album_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30), unique = False, nullable = False)
    artist = db.Column(db.String(30), unique = False, nullable = False)
    genre = db.Column(db.String(40), unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f"{self.song_id}-{self.name} {self.duration} {self.date_created}"   
    
class ratings(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'), primary_key=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.user_id}-{self.song_id} {self.rating}"

class playlists(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('login.user_id'))
    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return f"{self.user_id}-{self.playlist_id} {self.name}"

class playlist_songs(db.Model):
    p_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))

    playlist = db.relationship('playlists', backref=db.backref('playlist_songs', cascade='all, delete-orphan'))
    song = db.relationship('songs', backref=db.backref('playlist_songs', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"{self.playlist_id}-{self.song_id}"   
    
class album_songs(db.Model):
    a_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.album_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))     

    album = db.relationship('albums', backref=db.backref('album_songs', cascade='all, delete-orphan'))
    song = db.relationship('songs', backref=db.backref('album_songs', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"{self.album_id}-{self.song_id}"   




