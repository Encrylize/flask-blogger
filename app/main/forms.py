from flask_wtf import Form
from wtforms.fields import StringField


class SearchForm(Form):
    search_field = StringField('Search')
