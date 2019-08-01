from init import init_app
import logging
from flask import redirect, url_for

app = init_app(__name__)


@app.route('/')
def hello():
    return redirect(url_for('authentication.profile'))


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == "__main__":
    app.run(debug=True)
