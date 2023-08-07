from logger import logger
from flask import Flask
from flasgger import Swagger
from routes import blueprints

SWAGGER_TEMPLATE = {
    "securityDefinitions": {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}}
}

def create_app():
    """Creates Flask application context."""

    app = Flask(__name__)
    Swagger(app, template=SWAGGER_TEMPLATE)

    # TODO: Utilitize this logic in future for nested blueprints.
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app


if __name__ == "__main__":
    app = create_app()

    logger.info("Listing all API routes:")

    for rule in app.url_map.iter_rules():
        logger.info(rule)

    app.run(host="0.0.0.0", port=8000)
