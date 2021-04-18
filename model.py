"""Models for educational videos app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

  # lessons = a list of Lesson objects
  # videos = a list of Video objects

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Lesson(db.Model):
    """A lesson."""

    __tablename__ = 'lessons'

    lesson_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'))
    # How should I handle tags? 

    user = db.relationship('User', backref='lessons')
    video = db.relationship('Video', backref='lessons')
  # lessonVids = a list of lessonVid association objects


    def __repr__(self):
        return f'<Lesson lesson_id={self.lesson_id} title={self.title}>'


class Video(db.Model):
    """A favorite video."""

    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    link = db.Column(db.String, nullable=False)
    title = db.Column(db.String)
    length = db.Column(db.Float)
    notes = db.Column(db.Text)

    user = db.relationship('User', backref='activities')

    # lessons = a list of Lesson objects
    # lessonVids = a list of lessonVid association objects


    def __repr__(self):
        return f'<Video video_id={self.video_id} title={self.title}>'


class LessonVid(db.Model):
    """An Lesson-Video association table."""

    __tablename__ = 'LessonVids' 

    lessonVid_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))

    video = db.relationship('Video', backref='lessonVids')
    lesson = db.relationship('Lesson', backref='lessonVids')

    def __repr__(self):
        return f'<VidActivity vidAct_id={self.vidAct_id}>'
    

def connect_to_db(flask_app, db_uri='postgresql:///edvid', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    
    connect_to_db(app)  


# N.B. - Figure out how to add in subject & grade once framework works.  
# how do I store in a way that's searchable and filter-able?
# subject = db.Column(db.String)
# grade_level = db.Column(db.String)
