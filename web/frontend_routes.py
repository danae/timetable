import flask
import timetable


# Create the blueprint
blueprint = flask.Blueprint('frontend', __name__)


# Show the index, which redirects to the planner
@blueprint.route('/')
def index():
  # Redirect to the planner
  return flask.redirect(flask.url_for('.planner'))


# Show the planner home
@blueprint.route('/planner')
def planner():
  # Render the home template
  return flask.render_template('planner.html')


# Show the planner details
@blueprint.route('/planner/details')
def planner_details():
  try:
    # Get the request parameters
    from_node = flask.request.args.get('from_node')
    to_node = flask.request.args.get('to_node')
    date = flask.request.args.get('date')
    time = flask.request.args.get('time')
    is_arrival = flask.request.args.get('is_arrival')

    # Validate and resolve the request parameters
    if from_node is None or (from_node := flask.g.feed.get_node_by_name(from_node)) is None:
      raise ValueError('from_node_not_found')
    if to_node is None or (to_node := flask.g.feed.get_node_by_name(to_node)) is None:
      raise ValueError('to_node_not_found')
    time = timetable.Time.fromstring(time)

    # Get the journeys
    journeys_algo = timetable.RaptorAlgorithm(flask.g.feed)
    journeys = journeys_algo.query_depart_after(from_node, to_node, time)

    # Render the details template
    return flask.render_template('planner_details.html', from_node = from_node, to_node = to_node, date = date, time = time, is_arrival = is_arrival, journeys = journeys)
  except ValueError as err:
    # Render the home template with errors
    return flask.render_template('planner.html', error = str(err))


# Show the departures home
@blueprint.route('/departures')
def departures():
  # Render the home template
  return flask.render_template('departures.html')


# Show the departures details
@blueprint.route('/departures/details')
def departures_details():
  try:
    # Get the request parameters
    node = flask.request.args.get('node')

    # Validate and resolve the request parameters
    if node is None or (node := flask.g.feed.get_node_by_name(node)) is None:
      raise ValueError('node_not_found')

    # Get the trips at the node
    trips = sorted([trip.beginning_at_node(node) for trip in node.get_trips_with_node() if trip.arrival_node != node])

    # Render the details template
    return flask.render_template('departures_details.html', node = node, trips = trips)
  except ValueError as err:
    # Render the home template with errors
    return flask.render_template('departures.html', error = str(err))
