"""Models for educational videos app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True
                        )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

  # lessons = a list of Lesson objects authored by user
  # faves = a list of Favorite objects identified by user

    def __repr__(self):
        return f'<User id={self.user_id} email={self.email}>'


class Lesson(db.Model):
    """A lesson."""

    __tablename__ = 'lessons'

    lesson_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    public = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    author = db.relationship('User', backref = 'lessons')

    # components = a list of Component objects
    # faves = a list of Fave objects 
    # tags = a list of Tag objects

    def __repr__(self):
        return f'<Lesson id={self.lesson_id} title={self.title}>'


class Component(db.Model):
    """A component within a lesson."""

    __tablename__ = 'components'

    compt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    compt_type = db.Column(db.String, nullable=False) # video, worksheet, image, text, etc
    text = db.Column(db.Text)
    name = db.Column(db.String)
    url = db.Column(db.String)
    vid_length = db.Column(db.Float) # if video, length in minutes
    lesson_id = db.Column(db.Integer, 
                          db.ForeignKey('lessons.lesson_id'))

    lesson = db.relationship('Lesson', backref='components')

    # tags = A list of tag objects

    def __repr__(self):
        return f'<Component id={self.compt_id} name={self.name}>'


class Tag(db.Model):
    """A category for sorting videos."""

    __tablename__ = 'tags' 
    # Would it make more sense to have the name be the primary key?
    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)

    lessons = db.relationship('Lesson', secondary='content_tags', viewonly=True)
    components = db.relationship('Component', secondary='content_tags', viewonly=True)

    # content_tags, with ties to both 


    def __repr__(self):
        return f'<Tag {self.category} {self.name}>'


class Content_Tag(db.Model):
    
    __tablename__ = 'content_tags'

    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.tag_id'), 
                       primary_key=True
                       )
    lesson_id = db.Column(db.Integer, 
                          db.ForeignKey('lessons.lesson_id')
                          )
    compt_id = db.Column(db.Integer, db.ForeignKey('components.compt_id'))

    component = db.relationship('Component', backref='tags')
    lesson = db.relationship('Lesson', backref='tags')
    tag = db.relationship('Tag', backref='content_tags')

    def __repr__(self):
        if self.component == None:
            return f'<Assoc {self.tag.name} for {self.lesson.title}>'
        elif self.lesson == None:
            return f'<Assoc {self.tag.name} for {self.component.name}>'
 

class Fave(db.Model):
    """A favorites middle table linking users to liked lessons."""

    __tablename__ = 'faves'

    fave_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))
    liker_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    liker = db.relationship('User', backref='faves')
    lesson = db.relationship('Lesson', backref='faves')

    def __repr__(self):
        return f'<Favorited! {self.liker.email} likes {self.lesson.title}>'
    

def connect_to_db(flask_app, db_uri='postgresql:///lessons', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = False
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    
    connect_to_db(app)  
 

