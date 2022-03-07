from flask_table import Table, Col
from flask import Flask, request, url_for
import pandas as pd

"""
A example for creating a Table that is sortable by its header
"""

app = Flask(__name__)


class SortableTable(Table):
    id = Col('ID')
    name = Col('Name')
    description = Col('Description')
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('index', sort=col_key, direction=direction)


@app.route('/')
def index():
    df = pd.DataFrame([
        (1, 'G', 'zzzzz'),
        (2, 'U', 'aaaaa'),
        (3, 'I', 'bbbbb')], columns=["id", "name", "description"])

    sort = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    df = df.sort_values(by=[sort], ascending=reverse)
    output_dict = df.to_dict(orient='records')

    table = SortableTable(output_dict,
                          sort_by=sort,
                          sort_reverse=reverse)
    return table.__html__()


if __name__ == '__main__':
    app.run(debug=True)