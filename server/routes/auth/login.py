import traceback

from flask import request
from db.queries import get_user_login
from authorization.token import Token, generate_token

def login():
    if request.method == "POST":

        try:

            payload = request.get_json()

            email = payload["email"]
            password = payload["password"]
            
            uid = get_user_login(email, password)

            if uid:
                access_token = generate_token(uid, mode=Token.ACCESS)
                refresh_token = generate_token(uid, mode=Token.REFRESH)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200

        except Exception as e:
            return traceback.format_exc(), 500

        return {"message": "Username/password did not match records."}, 401