import bcrypt

salt = bcrypt.gensalt()

def password_hashing(password):
    """Bcrypt password hashing"""

    hashed_password = bcrypt.hashpw(password, salt)

    # add function to add salt to user_id db

    return hashed_password



def hashed_password_check(username, password):
    """Check that hashed password in database matches password inputted"""

    user = model.db.session.query(model.User).filter(model.User.user_name==username).first()

    hashed_password = user.user_password

    if bcrypt.checkpw(password, hashed_password):
        return True

    else:
        return False
