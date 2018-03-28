import bcrypt
import model
from flask import session

# salt = bcrypt.gensalt() # do I need this...?

def password_hashing(password):
    """Bcrypt password hashing"""

    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    return hashed_password
    #THANKSTAL

def hashed_password_check(username, password):
    """Check that hashed password in database matches password inputted"""

    user = model.db.session.query(model.User).filter(model.User.user_name==username).first()

    hashed_password = user.user_password


    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True

    else:
        return False
