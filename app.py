import logging
import os

from flask import Flask

from api import api
import config
from models import db

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler()])

LOGGER = logging.getLogger()


def create_app():
    LOGGER.info('Starting app in %s environment', config.APP_ENV)
    app = Flask(__name__)
    app.config.from_object('config')
    api.init_app(app)
    # initialize SQLAlchemy
    db.init_app(app)

    # define hello world page

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
