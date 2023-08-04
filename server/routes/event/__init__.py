from flask import Blueprint

from .index import event

bp = Blueprint('event', __name__)

routes = [
    (event, {
        "methods": [
            "POST"
        ]
    }),
]

for route, options in routes:
    bp.add_url_rule(f"/{route.__name__}", route.__name__, route, **options)

