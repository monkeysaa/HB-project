"""CRUD operations."""

from model import *
from flask import session

def create_user(handle, email, pwd):
    """Create and return a new user."""

    new_user = User(handle=handle, email=email, password=pwd)

    db.session.add(new_user)
    db.session.commit()

    return new_user


def create_lesson(title, author_id, description = "", public = False):
    """Create and return a new lesson."""

    new_lesson = Lesson(title=title, description=description, 
                        author_id=author_id, public=public)
    
    db.session.add(new_lesson)
    db.session.commit()

    return new_lesson


def create_comp(name, comp_type, url = None, imgUrl=None, text = None, vid_length = None):
    """Create and return a new lesson."""

    new_component = Comp(name=name, comp_type=comp_type, 
                        url=url, imgUrl=imgUrl, vid_length=vid_length)
    
    db.session.add(new_component)
    db.session.commit()

    return new_component


def create_tag(name, category):
    tag = Tag(name=name, category=category)

    db.session.add(tag)
    db.session.commit()

    return tag


# Assignations
def assign_comp(comp, lesson):
    assoc = Lesson_Comp(lesson=lesson, comp=comp)

    db.session.add(assoc)
    db.session.commit()

    return assoc


def assign_tag_to_lesson(tag, lesson):
    assoc = Lesson_Tag(lesson=lesson, tag=tag)

    db.session.add(assoc)
    db.session.commit()

    return assoc


def assign_lesson_img(imgUrl, lesson_id):
    
    lesson = get_lesson_by_id(lesson_id)
    lesson.imgUrl = imgUrl

    db.session.commit()

    return None


def assign_comp_img(imgUrl, comp_id):
    
    lesson = get_comp_by_id(lesson_id)
    lesson.imgUrl = imgUrl

    db.session.commit()

    return None


def lesson_exists(title, author_id):
    """Check unique lesson within user."""
    
    # Refactor later for efficiency
    lesson = Lesson.query.filter(
        (Lesson.title==title) & (Lesson.author_id==author_id)
        ).first()
    if lesson==None:
        return False
    return True


# Searches
def get_all_lessons():
    """Return all lessons."""

    return Lesson.query.all()


def get_users():
    """Return all users."""

    return User.query.all()


def get_components():
    """Return all components."""

    return Comp.query.all()


def get_comp_by_id(comp_id):
    """Get comps by id."""
    
    return Comp.query.filter(Comp.comp_id==comp_id).one()


def get_comp_faves(user_id):
    """Return all components favorited by this user."""

    return Fave_Comps.query.filter(liker_id == user_id).all()


def get_tag_by_name(name):
    """Return tag by name"""
    
    return Tag.query.filter(Tag.name == name).first()

def get_lessons_by_tag(tag):

    return get_tag_by_name(tag).lessons

# def get_components_by_tag(tag):

#     return get_comp_by_name(tag).comps


def get_public_lessons(user_id):
    """Return lessons marked public"""

    return Lesson.query.filter((Lesson.author_id==user_id) & (Lesson.public==True)).all()


def get_lesson_by_id(lesson_id):
    """Get lessons by ID."""
    
    return Lesson.query.get(lesson_id)


def get_lesson_by_title(title):
    """Get lessons by title."""
    print("Add check for unique title per user and verify with user info.")
    
    return Lesson.query.filter(Lesson.title==title).first()

# USER Search Functions
def get_lessons_by_user(user_id):
     """Return lessons by user"""

     return Lesson.query.filter(Lesson.author_id == user_id).all()


def get_lessons_by_term(term):
    """Basic: Get lessons by search term in title or description."""

    lessons = Lesson.query.filter((Lesson.title.like(f'%{term}%')) | 
    (Lesson.description.like(f'%{term}%'))).all()

    matching_components = Comp.query.filter(
        (Comp.name.like(f'%{term}%')) | 
        (Comp.text.like(f'%{term}%'))).all()

    for comp in matching_components:
        for lesson in comp.lessons:
            if lesson not in lessons:
                lessons.append(lesson)

    return lessons

# better to use a dispatcher vs. if/else?
def process_lesson_search(category, arg):
    
    print(category)
    if category == 'term':
        lessons = get_lessons_by_term(arg)
    elif category == 'subject' or category == 'grade':
        lessons = get_lessons_by_tag(arg)
    elif category == 'user':
        lessons = get_lessons_by_user(int(arg))
    
    return lessons


def get_comp_by_id(comp_id):
    """Get components by ID."""
    
    return Comp.query.get(comp_id)


def get_user_by_id(user_id):
    """Get user by ID."""
    
    return User.query.get(user_id)


def get_user_by_email(email):
    """Get user by email."""
    return User.query.filter(User.email == email).first() 

    
# CREATE FAVE ASSOCIATIONS
# def create fave_comp()
# def create_fave_lesson(lesson_id, liker_id):


# def get(user_id):
#     """Return all lessons favorited by this user."""

#     return Fave_Lessons.query.filter(Fave_Lessons.liker_id == user_id).all()



if __name__ == '__main__':
    from server import app
    connect_to_db(app, echo=False)
