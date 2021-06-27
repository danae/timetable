import flask
import os
import timetable

from .frontend_routes import blueprint as frontend_blueprint
from .node_routes import blueprint as node_blueprint
from .trip_routes import blueprint as trip_blueprint


# Parse the feed
feed_decoder = timetable.GATTFeedDecoder()
feed = feed_decoder.decode(os.getenv('TIMETABLE'))

# Create and configure the application
app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Register blueprints
app.register_blueprint(frontend_blueprint)
app.register_blueprint(node_blueprint)
app.register_blueprint(trip_blueprint)

# Create a before request handler
@app.before_request
def load_feed():
  flask.g.feed = feed
