"""CRUD operations."""

from model import *

def create_user(e, pwd):
    """Create and return a new user."""

    new_user = User(email=e, password=pwd)

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


def create_comp(name, comp_type, url = None, text = None, vid_length = None):
    """Create and return a new lesson."""

    new_component = Comp(name=name, comp_type=comp_type, 
                        url=url, vid_length=vid_length)
    
    db.session.add(new_component)
    db.session.commit()

    return new_component


# CREATE ASSOCIATIONS
# def lesson_comp()
# def create_lesson_tag()
# def create_comp_tag()
# def create fave_comp()
# def create_fave_lesson(lesson_id, liker_id):
#     """Create a new favorite."""


def get_lessons_by_user(user_id):
     """Return lessons by user"""

     return Lesson.query.filter(Lesson.author_id == user_id).all()


def get_all_lessons():
    """Return all lessons."""

    return Lesson.query.all()


def get_users():
    """Return all users."""

    return User.query.all()


def get_components():
    """Return all components."""

    return Comp.query.all()


def get_lesson_faves(user_id):
    """Return all lessons favorited by this user."""

    return Fave_Lessons.query.filter(Fave_Lessons.liker_id == user_id).all()


def get_comp_faves(user_id):
    """Return all components favorited by this user."""

    return Fave_Comps.query.filter(liker_id == user_id).all()


def get_lesson_by_id(lesson_id):
    """Get lessons by ID."""
    
    return Lesson.query.get(lesson_id)


def get_comp_by_id(comp_id):
    """Get components by ID."""
    
    return Comp.query.get(comp_id)


def get_user_by_id(user_id):
    """Get user by ID."""
    
    return User.query.get(user_id)


def get_user_by_email(email):
    """Get user by email."""
    return User.query.filter(User.email == email).first() 


if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
