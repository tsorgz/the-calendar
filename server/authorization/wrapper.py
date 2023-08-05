from flask import request
from functools import wraps
from authorization.token import Token, verify_token


def requires_auth(func):
    """Wraps a function requiring user authentication.

    This decorator retrieves the Bearer token from the Authorization header
    from the incoming request. If the access token is invalid or missing, we
    will send a 403 HTTP error code along with a message explaining the failed
    request. Otherwise, we will pass the user ID into the wrapped function and
    return its result.

    Args:
        func (callable): The function to wrap

    Returns:
        A 2-length tuple containing the response to the incoming request.
            [0] (dict): The JSONified body response.
            [1] (int): The HTTP code of the response.

    """

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
