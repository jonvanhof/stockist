import sources
import objects
import parse
# import auth.sqlalchemy_psql as auth
# import mdl.sqlalchemy_psql as mdl
# import ds.sqlalchemy_psql as ds

from flask import Flask
from flask_cors import CORS

stockist = Flask(__name__)
CORS(stockist)


@stockist.route("/")
def root():
	return "Freshest stock found here."
