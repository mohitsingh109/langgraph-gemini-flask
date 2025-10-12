from flask import Flask
from dotenv import load_dotenv

from app.db import ensure_table


def create_app() -> Flask:

    load_dotenv() # this is reading the .evn and load it as a env in the project
    app = Flask(__name__)
    ensure_table()
    return app

flask = create_app()

flask.run(debug=False, port=8000)