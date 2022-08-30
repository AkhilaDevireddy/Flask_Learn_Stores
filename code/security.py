from werkzeug.security import safe_str_cmp
from resources.user import User


def authenticate(username, password):
    user_detail = User.find_by_username(username=username)
    if user_detail and safe_str_cmp(user_detail.password, password):
        return user_detail

def identity(payload):
    target_id = payload['identity']
    user_detail = User.find_by_userid(userid=target_id)
    return user_detail
