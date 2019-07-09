from flask_cors import CORS

import config
import logging

from flask import Flask, current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_model():
    model_background = current_app.config['DATA_BACKEND']
    if model_background == 'datastore':
        import models
        model = models

    return model


def init_app(name):
    app = Flask(name)
    CORS(app, supports_credentials=True)

    app.config.from_object(config)
    app.secret_key = '\n\x92\x03\xf4s\xc9\xb8\xfe\x1a\x8a\xe9G\'\xf0Q\x0f\x89\n7\x81\xc0Vz_\xf6\x99:\xc4SR\x9en\xa3(' \
                     '\x0fi\x83\x81aab\xc4\x885\xb5^z\xf1\xee&\xde\x009J\xbfH\xe3\xdf\xe0"\xf5\x8d\xe8@\x10\x8f\xe0' \
                     '\x85\x94\x81%"B(\x01\x01\xa7\xa8M\x1c\xebZ\xcb_\x89\x9a\x10{' \
                     '-\x8f\x93\xc5k\x81\xc5\x13\xf9d\xfe\xbb\xa2\xf8\x88\x13TD;\xd9\x06R]\xc4Ni9DR\x1d\xb0\x14c\xda' \
                     '\x825u\xd6-i '

    with app.app_context():
        model = get_model()
        model.init_app(app)
        from views.auth_api import auth
        from views.stories_api import story, comment, like
        app.register_blueprint(auth)
        app.register_blueprint(story)
        app.register_blueprint(comment)
        app.register_blueprint(like)

    return app
