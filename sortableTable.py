from flask_table import Table, Col
from flask import url_for, request

class SortableTable(Table):
    id = Col('ID')
    author = Col('AUTHOR')
    opinion = Col('OPINION')
    rating = Col('RATING')
    usefulnes = Col("USEFULNESS")
    upsides = Col('UPSIDES')
    downsides = Col("DOWNSIDES")
    confirmed = Col('CONFIRMED')
    review = Col("REVIEW")
    purchase = Col("PURCHASE")
    text = Col("TEXT")

    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for(request.endpoint, **request.view_args, sort=col_key, direction=direction, _anchor='main-table')