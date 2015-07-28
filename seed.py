"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""
    user_file = open("seed_data/u.user") #Opens file
    # user_data = user_file.read() #Reads file

    # Iterates over each line in File.
    for line in user_file.readlines():
        # user_info =
        # Splits line into list of strings.
        line.rstrip("\n")
        user_info = line.split("|")
        # second for loop Iterates over each item in list.
        # Adds each item to database.
        # import pdb; pdb.set_trace()
        person = User(user_id=user_info[0],age=user_info[1],zipcode=user_info[4],email='NULL',password='NULL')

        db.session.add(person)
        db.session.commit()
        # for item in user_info: 
        #     import pdb; pdb.set_trace()
        #     person = User(user_id=item,age=item,zipcode=item,email='NULL',password='NULL')

        #     db.session.add(person)
        #     db.session.commit()
        # declare variable for user. see sample
#  >>> juanita = User(user_id=5, email="juanita@gmail.com",
# ...     password="abc123", age=42, zipcode="94103")
# >>> db.session.add(juanita)
# >>> db.session.commit()
        # commit
    # Moves on to next line. does the same thing in the second for loop
    # for each line.
    print "IT IS DONE"
    user_file.close() #Closes the file. 
# Check database to make sure this part works.
# run seed.py

def load_movies():
    """Load movies from u.item into database."""


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
