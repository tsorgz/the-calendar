from flask import Blueprint

from .login import login
from .signup import signup
from .token import token

bp = Blueprint('auth', __name__)

routes = [
    (login, {
        "methods": [
            "POST"
        ]
    }),
    (signup, {
        "methods": [
            "POST"
        ]
    }),
    (token, {
        "methods": [
            "GET"
        ]
    }),
]

for route, options in routes:
    bp.add_url_rule(f"/{route.__name__}", route.__name__, route, **options)

