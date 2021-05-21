from flask import render_template
from flask_classy import route, FlaskView


class HomepageView(FlaskView):
    route_base = '/'

    @route('/', endpoint='homepage')
    def homepage(self):
        return render_template('index.html')
