from flask import request
from functools import wraps
from authorization.token import Token, verify_token

def requires_auth(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        
        token_header = request.headers.get("Authorization")

        if not token_header:
            return {"message": "Token missing."}, 403
        
        token = token_header.split(" ")[1]
        is_valid, uid, message = verify_token(token, mode=Token.ACCESS)

        if is_valid:
            return func(uid, *args, **kwargs)
        
        return {"message": message}, 403
    
    return decorator
