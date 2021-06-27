import flask
import timetable


# Create the blueprint
blueprint = flask.Blueprint('trip', __name__)


# Return all trips as JSON
@blueprint.route('/trips.json')
def get_trips():
  # Get all trips
  trips = flask.g.feed.get_trips()

  # Return the trips as JSON
  return flask.jsonify([trip.to_json() for trip in trips])


# Return a trip as JSON
@blueprint.route('/trips/<string:id>.json')
def get_trip(id):
  # Get the trips
  try:
    trip = flask.g.feed.get_trip(id)
  except KeyError as err:
    flask.abort(404)

  # Return the trip as JSON
  return flask.jsonify(trip.to_json())
