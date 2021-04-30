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
CLOUD_KEY = os.environ['CLOUDINARY_KEY']
CLOUD_SECRET = os.environ['CLOUDINARY_SECRET']
AWS_KEY = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

app.jinja_env.undefined = StrictUndefined


# Routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


# Later, remove this route.
@app.route('/users')
def all_users():
    """View all users."""
    
    users = crud.get_users()
    return render_template('all_users.html', users=users)


# View users' public lessons
@app.route('/users/<user_id>')
def show_public_lessons(user_id):
    user = crud.get_user_by_id(user_id)
    pub_lessons = crud.get_public_lessons(user.user_id)

    return render_template('user_profile.html', user=user, lessons=pub_lessons)


@app.route('/lessons')
def all_lessons():
    """View all lessons."""

    lessons = crud.get_all_lessons()
    return render_template('all_lessons.html', lessons=lessons)


@app.route('/lessons/<lesson_id>')
def show_lesson(lesson_id):
    """Show details on a particular lesson."""

    lesson = crud.get_lesson_by_id(lesson_id)
    return render_template('lesson_details.html', lesson=lesson)


@app.route('/login', methods=['POST'])
def verify_user():
    """Authenticate user and display profile page"""

    email = request.form.get('email')
    password = request.form.get('password')

    try: 
        user = crud.get_user_by_email(email)
        user_lessons = crud.get_lessons_by_user(user.user_id)
        
        if password == user.password:
            session['user_id'] = user.user_id
            return render_template('user_profile.html', 
                                    user=user, lessons=user_lessons)
        else:
            flash(f"Wrong password. It should be: {user.password}.")
            return redirect('/')

    except:
        flash("Email not in our system. Try again.")
        return redirect('/')


# If someone types in login url by hand without logging in...
@app.route('/login')
def check_if_user():
    """Check for user, or redirect to homepage and prompt to login. """

    try:
        if session['user']:
            user = session['user']
            lessons = crud.get_lessons_by_user(user.user_id)
            return render_template(f'user_profile.html', 
                                   user=user, lessons=lessons)
    except:
        flash('Please log in first.')
        return redirect('/')


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


@app.route('/search', methods=['GET'])
def search_lessons():
    """Search for lesson by term."""
    
    term = request.args.get('term')
    lessons = crud.get_lesson_by_term(term)

    print(f'lessons = {lessons}')
    return render_template('search.html', term=term, lessons=lessons)
    

@app.route('/post-form-data', methods=['POST'])
def upload_image():
    """Process the cloudinary form."""

    my_file = request.files['my-file'] # note: request arg should match name var on form
    result = cloudinary.uploader.upload(my_file, api_key=CLOUD_KEY, 
                                        api_secret=CLOUD_SECRET,
                                        cloud_name='hackbright')
    img_url = result['secure_url']
    img_url = crud.create_img(result['secure_url'])
    # run a crud function that saves this img_url to the database and returns it. 

    # work out display, e.g. <img src="{{ user.profile_url }}">
    return f'<img src="{img_url}">'


if __name__ == '__main__':
    connect_to_db(app,echo=False)
    app.run(host='0.0.0.0', debug=True)