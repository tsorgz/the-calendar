from flask import request
from jwt.exceptions import InvalidSignatureError
from authorization.token import refresh_token

def token():
    if request.method == "GET":

        token = request.headers["Authorization"].split(" ")[1]
        
        try:
            expired, new_token = refresh_token(token)
        except InvalidSignatureError:
            return {"message": "Invalid token."}, 401
        
        if expired:
            return {"message": "Token has expired, please log in again."}, 401
    
        return {"access_token": new_token}