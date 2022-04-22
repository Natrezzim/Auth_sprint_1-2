from flask import Flask
from flask_migrate import Migrate

from src.app.db.db import init_db
from src.app.db.db_models import *

app = Flask(__name__)
migrate = Migrate(app, db)
init_db(app)


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
