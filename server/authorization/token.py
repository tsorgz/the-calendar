import jwt
import os
from datetime import datetime, timedelta
from logger import logger


class TokenType:
    """Internally used definition for an authorization token.

    Attributes:
        name (str): String representation of the token type for human readability.
        expiry (datetime.timedelta): The amount of time a token is valid before it expires.
        signature (str): The secret access key used to encrypt the token.
        expiry_message (str): The expiry message for the user regarding how to handle an expired token of this type.

    """

    def __init__(
        self, name: str, expiry: timedelta, signature: str, expiry_message: str
    ):
        """Initializes a TokenType

        Args:
            name (str): String representation of the token type for human readability.
            expiry (datetime.timedelta): The amount of time a token is valid before it expires.
            signature (str): The secret access key used to encrypt the token.
            expiry_message (str): The expiry message for the user regarding how to handle an expired token of this type.
        """
        self.name = name
        self.expiry = expiry
        self.signature = signature
        self.expiry_message = expiry_message


class Token:
    """Class used to act as an enum for the types of tokens supported through the application."""

    ACCESS = TokenType(
        name="access",
        expiry=timedelta(minutes=30),
        signature=os.getenv("JWT_ACCESS_SECRET_KEY"),
        expiry_message="refresh for new access token",
    )
    """TokenType representing access tokens, the tokens used to access authorized endpoints."""

    REFRESH = TokenType(
        name="refresh",
        expiry=timedelta(days=7),
        signature=os.getenv("JWT_REFRESH_SECRET_KEY"),
        expiry_message="logging in is required",
    )
    """TokenType representing refresh tokens, the tokens used to refresh expired access tokens."""


def generate_token(user_id: str, mode: TokenType = Token.ACCESS):
    """Generates a token based on the TokenType configuration for a given user.

    Args:
        user_id (str): The user ID we want to set to represent the user of the generated token.
        mode (authorization.token.TokenType): The token configuration we want to generate the token from.

    Returns:
        A generated JWT token in str format. Information about the standard can be found here: https://datatracker.ietf.org/doc/html/rfc7519

    """

    utcnow = datetime.utcnow()
    payload = {"exp": utcnow + mode.expiry, "iat": utcnow, "sub": user_id}

    return jwt.encode(payload, mode.signature, algorithm="HS256")


def refresh_token(token: str):
    """Generates a new access token given a valid, unexpired refresh token.

    Args:
        token (str): The refresh token used to validate whether to create a new access token.

    Returns:
        expired (bool): A boolean indicating whether or not the token has expired.
        new_token (str | NoneType): A generated JWT access token in str format. Information about the standard can be found here: https://datatracker.ietf.org/doc/html/rfc7519

    Raises:
        jwt.InvalidSignatureError: A token passed through contained an invalid signature (i.e.: passing an access token in the token argument).

    """
    expired = False
    new_token = None

    try:
        payload = jwt.decode(token, Token.REFRESH.signature, algorithms=["HS256"])
        new_token = generate_token(payload["sub"], mode=Token.ACCESS)
    except jwt.ExpiredSignatureError:
        expired = True

    return expired, new_token


def verify_token(token: str, mode: TokenType = Token.ACCESS):
    """Verifies a valid token based on the TokenType configuration for a given user.

    Args:
        token (str): The token being validated.
        mode (authorization.token.TokenType): The token configuration we want to validate the token from.

    Returns:
        A tuple of 3-length containing information of the validation.
            [0] (bool): Boolean whether or not the token is valid.
            [1] (str | NoneType): The user ID of the successfully decoded token.
            [2] (str): An associated message generated on error. Empty string on success.

    """
    payload = None
    logger.debug(f"Verifying: {token=}, {mode.signature=}")
    try:
        payload = jwt.decode(token, mode.signature, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return False, None, f"Token has expired, {mode.expiry_message}."
    except jwt.InvalidSignatureError:
        return False, None, f"Token is invalid, {mode.expiry_message}."
    return True, payload["sub"], ""
