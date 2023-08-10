from flask import request
from flasgger import swag_from
from jwt.exceptions import InvalidSignatureError
from authorization.token import refresh_token


@swag_from("/apidocs/auth/token.yml")
def token():
    """Endpoint function to request a new access token.

    This endpoint function will read the Authorization header and
    return a new access token if a valid refresh token is provided.

    Returns:
        A 2-length tuple containing response information.
            [0] (dict): The body payload. Access token on success, message on failure.
            [1] (int): The HTTP response code assocaited with the request.

    """

    if request.method == "GET":
        # TODO: Handle missing and invalid Authorization header.
        token = request.headers["Authorization"].split(" ")[1]

        try:
            expired, new_token = refresh_token(token)
        except InvalidSignatureError:
            return {"message": "Invalid token."}, 401

        if expired:
            return {"message": "Token has expired, please log in again."}, 401

        return {"access_token": new_token}, 201
