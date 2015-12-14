import datetime

from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    # Dummy posts for template testing
    posts = [{
        'title': 'Hello World!',
        'body': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                   Vivamus nec pretium felis. Cras feugiat nunc non ex semper,
                   a vehicula risus convallis. Integer varius dignissim lacus.
                   Mauris auctor, ligula eu laoreet ultrices, enim nibh tempor
                   risus, in hendrerit libero turpis posuere mi.
                   Curabitur condimentum nunc libero, tempor consequat purus mollis.''',
        'author': 'Encrylize',
        'tags': ['testing', 'foo', 'bar'],
        'timestamp': datetime.datetime(2015, 12, 14, 17, 18, 4, 764044)
    },
    {
        'title': 'Hello World! 2',
        'body': '''Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                   Vivamus nec pretium felis. Cras feugiat nunc non ex semper,
                   a vehicula risus convallis. Integer varius dignissim lacus.
                   Mauris auctor, ligula eu laoreet ultrices, enim nibh tempor
                   risus, in hendrerit libero turpis posuere mi.
                   Curabitur condimentum nunc libero, tempor consequat purus mollis.''',
        'author': 'Guido van Rossum',
        'tags': ['testing', 'foo', 'bar'],
        'timestamp': datetime.datetime(2013, 8, 12, 13, 15)
    }]

    return render_template('main/index.html', title='Home', posts=posts)
