import os
from db import get_psql_info

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from uuid import uuid4

def create_user(email: str, password: str, first_name: str, last_name: str):

    user_id = str(uuid4())

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )

    password_hash = kdf.derive(password.encode())

    connection, cursor = get_psql_info()

    sql = "INSERT INTO users (id, email, firstname, lastname, passhash, salt) VALUES (%s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, (user_id, email, first_name, last_name, password_hash, salt))
    connection.commit()

    cursor.close()
    connection.close()

    return user_id

def get_user_login(email: str, password: str):

    connection, cursor = get_psql_info()

    sql = "SELECT id, passhash, salt FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if not user:
        return None

    user_id, password_hash, salt = user

    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=bytes(salt),
        iterations=100000
    )

    try:
        kdf.verify(password.encode(), bytes(password_hash))
        return user_id
    except:
        import traceback
        return None

