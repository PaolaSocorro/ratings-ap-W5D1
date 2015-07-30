"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

DEBUG_TB_INTERCEPT_REDIRECTS = False

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show a list of users"""

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/<int:id>')
def user_profile(id):
    """Show user profile"""

    all_ratings = db.session.query(User, Movie).join(Movie).all()
    this_user = User.query.filter_by(user_id=id).one()
    age = this_user.age
    zipcode = this_user.zipcode
    print id, age, zipcode

    return render_template("user_profile.html", username=id, age=age, zipcode=zipcode)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """ Login  """

    if request.method == 'POST':
        username = request.form.get("username") # ""
        password = request.form.get("password") # ""

        credentials = (username, password)

        session['login_id'] = credentials
        flash('You were successfully logged in')

        print "LOOK HERE NOW", session
        return redirect("/")

    else:
        return render_template("login_form.html")

@app.route('/logout')
def log_out():
    """Log out"""
    # If enough time: hide login/logout button depending if login/logout 
    if session["login_id"] in session:
        del session['login_id']
        flash('You no cool anymore')
        print "Logged out:" , session

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()