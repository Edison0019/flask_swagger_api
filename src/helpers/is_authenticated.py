from flask import session

def is_user_authenticated(func):
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            return func(*args,**kwargs)
        else:
            return {'response':'please make sure to log in the system'}
    return wrapper