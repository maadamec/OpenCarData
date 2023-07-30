""" Initialization of database via flask application context """

from flask import Flask
from dbClient.model import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://' \
                                        f'{os.environ["POSTGRES_USER"]}' \
                                        f':{os.environ["POSTGRES_PASSWORD"]}' \
                                        f'@{os.environ["POSTGRES_HOST"]}' \
                                        f':{os.environ["POSTGRES_PORT"]}' \
                                        f'/{os.environ["POSTGRES_DB"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
