from flask import Blueprint

from .index import event

bp = Blueprint("event", __name__)

routes = [
    ("", event, {"methods": ["POST"]}),
]

# TODO: Logic repeated in __init__.py files in route, should create utility function for
for path, route, options in routes:
    bp.add_url_rule(
        f"/{path}",
        f"{route.__module__}{route.__name__}".replace(".", "-"),
        route,
        **options,
    )
