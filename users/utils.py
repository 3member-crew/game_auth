import jwt
import datetime


def create_token(id, username):
    payload = {
            "id": id,
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token