from logger import logger
from flask import Flask
from routes import blueprints


def create_app():
    app = Flask(__name__)

    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    return app


if __name__ == "__main__":
    app = create_app()

    logger.info("Listing all API routes:")

    for rule in app.url_map.iter_rules():
        logger.info(rule)

    app.run(host="0.0.0.0", port=8000)
