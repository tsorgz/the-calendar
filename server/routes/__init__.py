from .auth import bp as auth_bp
from .event import bp as event_bp

blueprints = [
    (auth_bp, "/auth"),
    (event_bp, "/event")
]