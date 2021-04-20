"""Models for educational videos app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

  # lessons = a list of Lesson objects authored by user

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Lesson(db.Model):
    """A lesson."""

    __tablename__ = 'lessons'

    lesson_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    public = db.Column(db.Boolean)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                        nullable=False)

    owner = db.relationship('User', backref = 'lessons')
    # lesson_links = a list of lesson_link association objects

    # Use owner_id even if there's an association table?

    def __repr__(self):
        return f'<Lesson lesson_id={self.lesson_id} title={self.title}>'


class Link(db.Model):
    """A favorite link."""

    __tablename__ = 'links'

    link_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    link_type = db.Column(db.String) # video, worksheet, online lesson, etc
    vid_length = db.Column(db.Float) # if video, length in minutes

    # lesson_links = a list of lesson_link association objects

    def __repr__(self):
        return f'<Link link_id={self.link_id} title={self.title}>'


class Lesson_Link(db.Model):
    """An Lesson-Link association table."""

    __tablename__ = 'lesson_links' 

    ll_assoc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('links.link_id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))

    link = db.relationship('Link', backref='lesson_links')
    lesson = db.relationship('Lesson', backref='lesson_links')

    def __repr__(self):
        return f'<Lesson_Link ll_assoc_id={self.ll_assoc_id}>'


class Tag(db.Model):
    """A category for sorting videos."""

    __tablename__ = 'tags' 
    # Would it make more sense to have the name be the primary key?
    tag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)

    # link = db.relationship('Link', backref='lesson_links')
    # lesson = db.relationship('Lesson', backref='lesson_links')

    def __repr__(self):
        return f'<Tag category={self.category} name={self.name}>'


class Lesson_Tags(db.Model):
    """An Lesson-Tag association table."""

    __tablename__ = 'lesson_tags' 

    ltag_assoc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ### If tag_name becomes primary key, this needs to change. 
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))

    link = db.relationship('Link', backref='lesson_tags')
    lesson = db.relationship('Lesson', backref='lesson_tags')

    def __repr__(self):
        return f'<Lesson_Tag ltag_assoc_id={self.ltag_assoc_id}>'


class User_Lessons(db.Model):
    """An User-Lesson assoc. table that enables favorite lessons feature."""

    __tablename__ = 'user_lessons' 

    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'), 
                          nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                        nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

    

    def __repr__(self):
        return f'<User_Lesson uless_assoc_id={self.ltag_assoc_id}>'
    

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

