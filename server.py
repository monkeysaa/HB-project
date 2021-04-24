"""Server for lessons app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
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

if __name__ == '__main__':
    # app.secret_key = "SECRET!" #Do I want this here or on line 12?
    connect_to_db(app,echo=False)
    app.run(host='0.0.0.0', debug=True)