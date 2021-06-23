import flask
import timetable


# Create the blueprint
train_routes_blueprint = flask.Blueprint('trains', __name__)


# Return all trains as JSON
@train_routes_blueprint.route('/trains.json')
def get_trains():
  # Get all trains
  trains = flask.g.feed.get_trains()

  # Return the trains as JSON
  return flask.jsonify([train.to_json() for train in trains])


# Return a train as JSON
@train_routes_blueprint.route('/trains/<string:id>.json')
def get_train(id):
  # Get the train
  try:
    train = flask.g.feed.get_train(id)
  except KeyError as err:
    flask.abort(404)

  # Return the train as JSON
  return flask.jsonify(train.to_json())
