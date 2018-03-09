from flask import Flask

app = Flask(__name__, instance_relative_config=True)


app.config.from_object('config')

#a work around to circular imports
from app import views
