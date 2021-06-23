import flask
import os
import sys
import timetable

from .node_routes import node_routes_blueprint
from .train_routes import train_routes_blueprint


# Parse the feed
feed = timetable.load_feed(os.getenv('TIMETABLE'))

# Create and configure the application
app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Register blueprints
app.register_blueprint(node_routes_blueprint)
app.register_blueprint(train_routes_blueprint)

# Create a before request handler
@app.before_request
def load_feed():
  flask.g.feed = feed

# Create the application routes
@app.route('/node/<string:id>')
def show_node(id):
  # Get the node
  try:
    node = flask.g.feed.get_node(id)
  except KeyError as err:
    flask.abort(404)

  # Get the trains at the node
  trains = sorted([train.as_beginning_at_node(node) for train in node.get_trains(arrivals = False)])

  # Render the template
  return flask.render_template('node.html', node = node, trains = trains)

@app.route('/train/<string:id>')
def show_train(id):
  # Get the train
  try:
    train = flask.g.feed.get_train(id)
  except KeyError as err:
    flask.abort(404)

  # Render the template
  return flask.render_template('train.html', train = train)
