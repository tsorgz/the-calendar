import traceback

from flask import request
from flasgger import swag_from
from db.queries import get_user_login
from authorization.token import Token, generate_token

@swag_from("/server/apidocs/auth/login.yml")
def login():
    """Endpoint function to log in a user.

    This endpoint function will collect the email and password from
    the request and verify if the corresponding user has valid credentials.
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

            uid = get_user_login(email, password)

            if uid:
                access_token = generate_token(uid, mode=Token.ACCESS)
                refresh_token = generate_token(uid, mode=Token.REFRESH)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200

        # TODO: Handle less generically, the user receives the stacktrace on error.
        except Exception:
            return traceback.format_exc(), 500

        return {"message": "Username/password did not match records."}, 401
