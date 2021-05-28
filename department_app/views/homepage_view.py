"""
Web application homepage views used, this module defines the following classes:

- `HomepageView`, class that defines homepage views
"""

from flask import render_template
from flask_classy import route, FlaskView


class HomepageView(FlaskView):
    """
    Web application homepage views
    """
    # pylint: disable=no-self-use

    #: base url route for all homepage routes
    route_base = '/'

    @route('/', endpoint='homepage')
    def homepage(self):
        """
        Returns rendered `index.html` template for url route `/` and endpoint
        `homepage`

        :return: rendered `index.html` template
        """
        return render_template('index.html')
