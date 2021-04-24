"""CRUD operations."""

from model import db, User, Lesson, Component, Tag, Content_Tag, Fave, connect_to_db

def create_user(e, password):
    """Create and return a new user."""

    new_user = User(email=e, password=passcode)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def create_lesson(title, description, author_id, public = False):
    """Create and return a new lesson."""

    new_lesson = Lesson(title=title, description=description, 
                        author_id=author_id, public=public)
    
    db.session.add(new_lesson)
    db.session.commit()

    return new_lesson


def get_lessons():
    """Return all lessons."""

    return Lesson.query.all()


def get_users():
    """Return all users."""

    return User.query.all()


def get_lesson_by_id(lesson_id):
    """Get lessons by ID."""
    
    return Lesson.query.get(lesson_id)


def get_user_by_id(user_id):
    """Get user by ID."""
    
    return User.query.get(user_id)

def get_user_by_email(email):
    """Get user by email."""
    return User.query.filter(User.email == email).first() 


if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
