from flask import request
import traceback
from db.queries import create_user
from authorization.token import Token, generate_token

def signup():

    if request.method == "POST":

        try:

            payload = request.get_json()

            email = payload["email"]
            password = payload["password"]
            first_name = payload["first_name"]
            last_name = payload["last_name"]

            uid = create_user(email, password, first_name, last_name)

            if uid:
                access_token = generate_token(uid, mode=Token.ACCESS)
                refresh_token = generate_token(uid, mode=Token.REFRESH)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 201

        except Exception as e:
            return traceback.format_exc(), 500

        return {"message": "success"}, 201