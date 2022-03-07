from flask_table import Table, Col
from flask import Flask, request, url_for
import pandas as pd

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)


