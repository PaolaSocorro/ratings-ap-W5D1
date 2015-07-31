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
    """Show user profile
    all_ratings, joins ratings and movie table together. 
    returns list of all movies and ratings from one user.
    """

    
    this_user = User.query.filter_by(user_id=id).one()
    all_ratings = db.session.query(Rating.user_id, Rating.movie_id, Movie.title, 
                    Rating.score).join(Movie).filter(Rating.user_id==id).all()
   

    age = this_user.age
    zipcode = this_user.zipcode
    print id, age, zipcode, all_ratings

    return render_template("user_profile.html", username=id, age=age, zipcode=zipcode, all_ratings=all_ratings)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    """ Login  
     take email, password from user form
     check if credentials exist in database, by checking if 
     email is in user table.
     if email in table, redirect to their profile
     if not redirect to sign up page.

    """
    # import pdb; pdb.set_trace()
    if request.method == 'POST': #Process form if route gets a POST request
        email = request.form.get("email") # ""
        password = request.form.get("password") # ""

        credentials = (email, password)
        dbemails = db.session.query(User.email).all()

        print email, type(email)
        print "Query Ran"
        print type(dbemails)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('PLEASE SIGN UP!')
            return redirect("/signup")
        else:
            if user.password != password:
                print password
                flash('Incorrect password')
                return redirect("/login")

            session['login_id'] = credentials 
            print "SESSION: ", session
            flash('You were successfully logged in')
            return redirect("/users/%s" % user.user_id) # REDIRECT TO PROFILE PAGE.FIX
        


    else: #TAKE user to login page if route process a  GET request
        return render_template("login_form.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup_form():
    """ Sign Up
        Add email, password,age,zipcode then commit new person to database.
        Find new user, and redirect to their profile page. 
    """

    if request.method == 'POST':
        email = request.form.get("email") 
        password = request.form.get("password")
        age = request.form.get("age")
        zipcode = request.form.get("zipcode")

        person = User(age=age,zipcode=zipcode,email=email,password=password)

        db.session.add(person)
        db.session.commit()
        # new_userid = db.session.query.get(User.user_id.desc()).first()

        print person

    else:
        return render_template("signup.html")

    return redirect("/")



@app.route('/logout')
def log_out():
    """Log out
    redirect to homepage when logged out

    """
    # If enough time: hide login/logout button depending if login/logout 
    if session["login_id"] in session:
        del session['login_id']
        flash('You no cool anymore')
        print "Logged out:" , session

    return redirect("/")



@app.route('/movies')
def list_movies():
    """Show a list of all the movies
        Ordered by title"""

    all_movies = db.session.query(Movie).order_by(Movie.title).all()


    return render_template("movies_list.html",all_movies=all_movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()