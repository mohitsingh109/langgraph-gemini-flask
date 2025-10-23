import os

from flask import Flask
from dotenv import load_dotenv

from app.db import ensure_table


def create_app() -> Flask:

    load_dotenv() # this is reading the .evn and load it as a env in the project
    app = Flask(__name__) # Obj of flask

    # Load from yml or .env or .py .conf
    # us-east-1 (14) ==> jpa.conf, fra.conf, ca01.conf

    #file_name = os.getenv('REGION') + '.conf'

    ensure_table()
    return app

# flask = create_app() # Gas On to prepare food
#
# flask.run(debug=False, port=8000) # We start the application