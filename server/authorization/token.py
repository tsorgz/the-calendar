import jwt
import os
from datetime import datetime, timedelta

class TokenType:

    def __init__(self, name: str, expiry: timedelta, signature: str, expiry_message: str):
        self.name = name
        self.expiry = expiry
        self.signature = signature
        self.expiry_message = expiry_message


class Token:
    ACCESS = TokenType(
        name='access',
        expiry=timedelta(minutes=30),
        signature=os.getenv("JWT_ACCESS_SECRET_KEY"),
        expiry_message="refresh for new access token"
    )
    REFRESH = TokenType(
        name='refresh',
        expiry=timedelta(days=7),
        signature=os.getenv("JWT_REFRESH_SECRET_KEY"),
        expiry_message="logging in is required"
    )


def generate_token(user_id: str, mode: TokenType = Token.ACCESS):

    utcnow = datetime.utcnow()
    payload = {
        'exp': utcnow + mode.expiry,
        'iat': utcnow,
        'sub': user_id
    }

    return jwt.encode(
        payload,
        mode.signature,
        algorithm="HS256"
    )

def refresh_token(token: str):
    expired = False
    new_token = None

    try:
        payload = jwt.decode(token, Token.REFRESH.signature, algorithms=['HS256'])
        new_token = generate_token(payload['sub'], mode=Token.ACCESS)
    except jwt.ExpiredSignatureError:
        expired = True
    
    return expired, new_token

def verify_token(token: str, mode: TokenType = Token.ACCESS):
    payload = None
    try:
        payload = jwt.decode(token, mode.signature, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False, None, f"Token has expired, {mode.expiry_message}."
    except jwt.InvalidSignatureError:
        return False, None, f"Token is invalid, {mode.expiry_message}."
    return True, payload["sub"], ""
