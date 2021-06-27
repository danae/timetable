import flask
import timetable


# Create the blueprint
blueprint = flask.Blueprint('nodes', __name__)


# Return all nodes as JSON
@blueprint.route('/nodes.json')
def get_nodes():
  # Get all nodes
  nodes = flask.g.feed.get_nodes()

  # Return the nodes as JSON
  return flask.jsonify([node.to_json() for node in nodes])


# Return all niodes that match a query as JSON
@blueprint.route('/nodes/query.json')
def query_nodes():
  # Get the query
  q = flask.request.args.get('q')

  # Get all nodes the match the query
  nodes = timetable.query(flask.g.feed.get_nodes(), q)

  # Return the nodes as JSON
  return flask.jsonify([node.to_json() for node in nodes])


# Return a node as JSON
@blueprint.route('/nodes/<string:id>.json')
def get_node(id):
  # Get the node
  node = flask.g.feed.get_node(id)
  if node is None:
    flask.abort(404)

  # Return the node as JSON
  return flask.jsonify(node.to_json())


# Return the trains at a node as JSON
@blueprint.route('/nodes/<string:id>/trains.json')
def get_node_trains(id):
  # Get the request parameters
  departures = flask.request.args.get('departures', default = True, type = bool)
  arrivals = flask.request.args.get('arrivals', default = True, type = bool)

  # Get the node
  node = flask.g.feed.get_node(id)
  if node is None:
    flask.abort(404)

  # Get the trains at the node
  trains = sorted(node.get_trains(departures = departures, arrivals = arrivals))

  # Return the trains as JSON
  return flask.jsonify([train.to_json() for train in trains])
