from flask import request
from flasgger import swag_from
import traceback
from db.queries import create_user
from authorization.token import Token, generate_token


@swag_from("/server/apidocs/auth/signup.yml")
def signup():
    """Endpoint function to sign up a user.

    This endpoint function will collect the email, password, first name, and
    last name from the request and creates a user has valid credentials.
    If valid, the user will receive an access and refresh token for further use.

    Returns:
        A 2-length tuple containing response information.
            [0] (dict): The body payload. Refresh and access tokens on success, message on failure.
            [1] (int): The HTTP response code assocaited with the request.

    """

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

            return {"message": f"User already exists with email {email}"}, 409

        # TODO: Handle less generically, user will receive traceback on error.
        except Exception:
            return traceback.format_exc(), 500
