"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from u.user into database."""
    user_file = open("seed_data/u.user") #Opens file
    # user_data = user_file.read() #Reads file

    # Iterates over each line in File.
    for line in user_file.readlines():
        # Splits line into list of strings.
        line = line.rstrip()
        user_info = line.split("|")
        person = User(user_id=user_info[0],age=user_info[1],zipcode=user_info[4],email='NULL',password='NULL')

        db.session.add(person)
    db.session.commit()

    print "IT IS DONE"
    user_file.close() #Closes the file. 


def load_movies():
    """Load movies from u.item into database."""
    item_file = open("seed_data/u.item")
    for line in item_file.readlines():
        movie_info = line.split("|")
        date_file = movie_info[2]
        if movie_info[2]=="":
            date_file = "01-Jan-1000"
        date = datetime.strptime(date_file,"%d-%b-%Y")

        title = movie_info[1]
        title = title[:-7]
        movie = Movie(movie_id=movie_info[0],title=title,released_at=date,imdb_url=movie_info[4])

        db.session.add(movie)
    db.session.commit()
    print "MOVIE LOADS DONE"

    item_file.close()

def load_ratings():
    """Load ratings from u.data into database."""
    rating_file = open("seed_data/u.data")
    for line in rating_file.readlines():
        line = line.rstrip()
        rating_info = line.split("\t")
        ratings = Rating(movie_id=rating_info[0],user_id=rating_info[1],score=rating_info[2])
        db.session.add(ratings)
    db.session.commit()

    print "IT IS DONE"
    rating_file.close() #Closes the file. 

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
