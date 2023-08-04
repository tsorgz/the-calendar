from flask import Blueprint

from .login import login
from .signup import signup
from .token import token

bp = Blueprint('auth', __name__)

routes = [
    (login.__name__, login, {
        "methods": [
            "POST"
        ]
    }),
    (signup.__name__, signup, {
        "methods": [
            "POST"
        ]
    }),
    (token.__name__, token, {
        "methods": [
            "GET"
        ]
    }),
]

for path, route, options in routes:   
    bp.add_url_rule(f"/{path}", f"{route.__module__}{route.__name__}".replace(".", "-"), route, **options)

