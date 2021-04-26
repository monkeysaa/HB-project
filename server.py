"""Server for lessons app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "SECRET!"

app.jinja_env.undefined = StrictUndefined

# Add routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/users', methods=['POST'])
def register_user():
    """View all users."""

    email = request.form.get('email')
    password = request.form.get('password')
    
    # Check if user email is in the database
    user = crud.get_user_by_email(email)
    if user:
        flash('Email is already in use. Try again.')
        return redirect('/')
        
    else:
        crud.create_user(email, password)
        user = session['user']
        lessons = crud.get_lessons_by_user(user.user_id)
        flash('Account created!') # REMOVABLE?
        return render_template('user_profile.html', user=user, lessons=lessons)


# WAT. NEW USERS HAVE NO LESSONS. FIGURE THIS SHIT OUT.
@app.route('/users/<new_user>')
def new_user(new_user):
    user = crud.get_user_by_id(new_user)
    lessons = crud.get_lessons_by_user(user.user_id)

    return render_template('user_profile.html', user=user, lessons=lessons)


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
# STOLEN FROM MOVIE_DETAILS.
# <!--  <a href="/lessons/{{ lesson.lesson_id }}/rate_movie">
#   Rate this movie!
# </a> 

# <img src="{{ movie.poster_path }}"> -->


@app.route('/users')
def all_users():
    """View all users."""
    
    users = crud.get_users()
    return render_template('all_users.html', users=users)


@app.route('/login', methods=['POST'])
def verify_user():

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    user_lessons = crud.get_lessons_by_user(user.user_id)
    
    if user:
        if password == user.password:
            session['user_id'] = user.user_id
            return render_template('user_profile.html', 
                                    user=user, lessons=user_lessons)
        else:
            flash(f"Wrong password. It should be: {user.password}.")
            return redirect('/')
    else:
        flash("Email not in our system. Try again.")
        return redirect('/')


@app.route('/login')
def check_if_user():
    """Check for user, or redirect to homepage and prompt to login. """
    # In case someone types in this link by hand without logging in.

    try:
        if session['user']:
            user = session['user']
            lessons = crud.get_lessons_by_user(user.user_id)
            return render_template('loginpage.html', user=user, lessons=lessons)
    except:
        flash('Please log in first.')
        return redirect('/')


if __name__ == '__main__':
    # app.secret_key = "SECRET!" #Do I want this here or on line 12?
    connect_to_db(app,echo=False)
    app.run(host='0.0.0.0', debug=True)