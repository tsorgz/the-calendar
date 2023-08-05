import os
from db import get_psql_info

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from uuid import uuid4


def create_user(email: str, password: str, first_name: str, last_name: str):
    """Creates user entity in database.

    The function calls for email, first name, last name, and hashed and salted
    password information to be stored for application login.

    Args:
        email (str): The email to be associated with the user
        password (str): The raw password associated with the user
        first_name (str): The first name associated with the user
        last_name (str): The last name assocaited with the user

    Returns:
        The user ID associated with the newly created account

    """

    user_id = str(uuid4())

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=salt, iterations=100000)

    password_hash = kdf.derive(password.encode())

    connection, cursor = get_psql_info()

    sql = "INSERT INTO users (id, email, firstname, lastname, passhash, salt) VALUES (%s, %s, %s, %s, %s, %s)"

    # TODO: We don't have error handling for emails already associated with accounts.

    cursor.execute(sql, (user_id, email, first_name, last_name, password_hash, salt))
    connection.commit()

    cursor.close()
    connection.close()

    return user_id


def get_user_login(email: str, password: str):
    """Retrieves a user entity in database if the password matches.

    The function retrieves the email, password hash, and salt associated
    with the user and returns the user ID if the password matches what is encrypted.

    Args:
        email (str): The email to be associated with the user
        password (str): The raw password to be verified against the database

    Returns:
        The user ID associated with the verified account. Otherwise, nothing.

    """

    connection, cursor = get_psql_info()

    sql = "SELECT id, passhash, salt FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return None

    user_id, password_hash, salt = user

    kdf = PBKDF2HMAC(algorithm=SHA256(), length=32, salt=bytes(salt), iterations=100000)

    try:
        kdf.verify(password.encode(), bytes(password_hash))
        return user_id
    except:
        return None
