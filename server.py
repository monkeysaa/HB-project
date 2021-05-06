"""Server for lessons app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import cloudinary.uploader
import crud
import boto3
import os 

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "SECRET!"

# API INFO
s3 = boto3.resource('s3')
CLIENT = boto3.client('s3')
CLOUD_KEY = os.environ['CLOUDINARY_KEY']
CLOUD_SECRET = os.environ['CLOUDINARY_SECRET']
AWS_KEY = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

app.jinja_env.undefined = StrictUndefined

GRADES = ['Pre-K', 'K', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th',
          '9th', '10th', '11th', '12th']
SUBJECTS = ['Math', 'Writing', 'Reading', 'Science', 'Social Studies', 
            'Arts/Music', 'Foreign Lang.']

# Routes!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


# NAV ROUTES
# MyProfile link in nav_bar
@app.route('/profile')
def display_profile():
    """Display profile if user. Same as /login endpoint above. """
    
    return redirect('/login')


# View all users link in Nav. Later, remove this route.
@app.route('/users')
def all_users():
    """View all users."""
    
    users = crud.get_users()
    return render_template('all_users.html', users=users)


# Direct here from search for lesson by author? 
# Or remove this route and use JS for dynamic display? 
@app.route('/users/<user_id>')
def show_public_lessons(user_id):
    """View all public lessons by a user"""
    user = crud.get_user_by_id(user_id)
    pub_lessons = crud.get_public_lessons(user.user_id)

    return render_template('user_profile.html', user=user, lessons=pub_lessons)


# View public lessons via link in Nav. Later, remove this route.
@app.route('/index')
def all_lessons():
    """View all lessons."""

    lessons_to_display=[]
    lessons = crud.get_all_lessons()
    for lesson in lessons:
        if lesson.public==True:
            lessons_to_display.append(lesson)

    return render_template('index.html', lessons=lessons_to_display)


# LOGIN ROUTES
# Homepage login form
@app.route('/login', methods=['POST'])
def verify_user():
    """Authenticate user and display profile page"""

    email = request.form.get('email')
    password = request.form.get('password')

    try: 
        user = crud.get_user_by_email(email)
        
        if password == user.password:
            session['user_id'] = user.user_id
            # flash(f"User {session['user_id']} logged in!")
            user_lessons = crud.get_lessons_by_user(user.user_id)
            return render_template('user_profile.html', 
                                    user=user, lessons=user_lessons)
        else:
            flash(f"Wrong password. It should be: {user.password}.")
            return redirect('/')

    except:
        flash("Email not in our system. Try again.")
        return redirect('/')


# If /login endpoint typed by hand without logging in
@app.route('/login')
def check_if_user():
    """Check session for user, else redirect to homepage and prompt to login. """

    try:
        if session['user_id']:
            user = crud.get_user_by_id(session['user_id'])
            lessons = crud.get_lessons_by_user(session['user_id'])
            return render_template(f'user_profile.html', 
                                   user=user, lessons=lessons)
    except:
        flash('Please log in first.')
        return redirect('/')


# Sign up & Login for new users, from Homepage
@app.route('/signup', methods=['POST'])
def register_user():
    """Create and log in a new user."""

    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if user email is already in the database
    user = crud.get_user_by_email(email)
    try:
        user = crud.create_user(email, password)
    except:
        flash('Email is already in use. Try again.')
        return redirect('/')

    session['user_id'] = user.user_id

    return render_template('user_profile.html', user=user, lessons=[])


# SEARCH ROUTES
@app.route('/search', methods=['GET'])
def display_search_results():
    """Search for lesson by term."""
    
    lesson_matches = set()
    term = request.args.get('term')
    grade = request.args.get('grade')
    subject = request.args.get('subject')
    user = (request.args.get('user'))
    terms = {term: 'term', grade: 'grade', subject: 'subject', user: 'user'}

    for category in terms:
        if category:
            lessons = crud.process_lesson_search(terms[category], category)
            for lesson in lessons:
                lesson_matches.add(lesson)

    return render_template('search.html', term=term, lessons=lessons)


# LESSON ROUTES
# Details for one lesson
# Later, limit route access to public lessons or author. Else redirect (to where?)
@app.route('/lessons/<lesson_id>') # This should be GET
def show_lesson(lesson_id):
    """Show details on a particular lesson."""

    session['lesson_id'] = lesson_id
    lesson = crud.get_lesson_by_id(lesson_id)

    if lesson.imgUrl==None:
        lesson.imgUrl = 'https://res.cloudinary.com/hackbright/image/upload/v1619906696/zzwwu2rbkbve3eozoihx.png'

    return render_template('lesson_details.html', lesson=lesson)


# Try to combine with above route. For later, maybe turn to RESTful state?
@app.route('/lesson-pic', methods=['POST']) # This should be PUT? 
def upload_lesson_image():
    """Save img to Lessons in the db and display via Cloudinary."""

    my_file = request.files['my-file'] # note: request arg should match name var on form
    result = cloudinary.uploader.upload(my_file, api_key=CLOUD_KEY, 
                                        api_secret=CLOUD_SECRET,
                                        cloud_name='hackbright')
    img_url = result['secure_url']
    img_url = crud.assign_lesson_img(result['secure_url'], session['lesson_id']) 

    lesson = crud.get_lesson_by_id(session['lesson_id'])
    # work out display, e.g. <img src="{{ user.profile_url }}">
    return redirect(f'/lessons/{lesson.lesson_id}')


# Directed here from Create-Lesson link
# Later, not supposed to use internal links to create
@app.route('/create_lesson')
def create_lesson():
    """Create a new lesson and redirect to editable lesson page."""

    new_lesson = crud.create_lesson("Lesson title", session['user_id'])
    session['lesson_id'] = new_lesson.lesson_id

    return redirect(f'/lessons/{new_lesson.lesson_id}')


@app.route('/component', methods=['POST'])
def create_component():
    """Add component to Lessons in the db and display via Cloudinary."""

    my_file = request.files['my-file'] # note: request arg should match name var on form
    
    #Upload to Cloudinary
    # result = cloudinary.uploader.upload(my_file, api_key=CLOUD_KEY, 
    #                                     api_secret=CLOUD_SECRET,
    #                                     cloud_name='hackbright')

    result = CLIENT.upload_file('my_file', 'hackbright-project', 'pdf')
    
    #Create component
    component = crud.create_comp('pdf', 'pdf')
    session['comp_id'] = component.comp_id
    # component.url = result['secure_url']

    #Attach to lesson
    lesson = crud.get_lesson_by_id(session['lesson_id'])
    crud.assign_comp(component, lesson)
    # run a crud function that saves this url to the database and returns it. 

    # work out display, e.g. <img src="{{ user.profile_url }}">
    return redirect(f'/lessons/{lesson.lesson_id}')



@app.route('/edit_less_title', methods=['POST'])
def edit_title():

    pass

if __name__ == '__main__':
    connect_to_db(app,echo=False)
    app.run(host='0.0.0.0', debug=True)