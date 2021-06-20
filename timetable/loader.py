import copy
import toml

from .feed import Feed
from .model import *


# Load a feed from a file
def load_feed(file):
  # Parse the TOML file
  try:
    data = toml.load(file)
  except toml.TomlDecodeError as err:
    raise FeedDecodeError(f"File {file!r}: {err}")

  # Create a new feed
  feed = Feed()
  feed.name = data.get('feed_name')
  feed.author = data.get('feed_author')
  feed.description = data.get('feed_description')

  # Load the agencies
  for id, agency_data in data['agencies'].items():
    _parse_agency(feed, id, agency_data)

  # Load the nodes
  for id, node_data in data['nodes'].items():
    _parse_node(feed, id, node_data)

  # Load the train types
  for id, train_type_data in data['train_types'].items():
    _parse_train_type(feed, id, train_type_data)

  # Load the train series
  for id, train_series_data in data['train_series'].items():
    _parse_train_series(feed, id, train_series_data)

  # Load the trains
  for id, train_data in data['trains'].items():
    _parse_train(feed, id, train_data)

  # Return the feed
  return feed


# Parse an agency
def _parse_agency(feed, id, data):
  try:
    feed.register_agency(id, **data)
  except (TypeError, ValueError) as err:
    raise FeedDecodeError(f"Agency id {id!r}: {err}")


# Parse a node
def _parse_node(feed, id, data):
  try:
    feed.register_node(id, **data)
  except (TypeError, ValueError) as err:
    raise FeedDecodeError(f"Node id {id!r}: {err}")


# Parse a train type
def _parse_train_type(feed, id, data):
  try:
    feed.register_train_type(id, **data)
  except (TypeError, ValueError) as err:
    raise FeedDecodeError(f"Train type id {id!r}: {err}")


# Parse a train series
def _parse_train_series(feed, id, data):
  try:
    # TODO: Make route required
    if 'route' in data:
      data['route'] = _parse_route(feed, data['route'])
    else:
      data['route'] = Route(feed, [])

    feed.register_train_series(id, **data)
  except (TypeError, ValueError) as err:
    raise FeedDecodeError(f"Train series id {id!r}: {err}")


# Parse a train
def _parse_train(feed, id, data):
  try:
    # If the train has a route, then it is a standalone train
    if 'route' in data:
      # Parse the keys
      data['time'] = LenientTime.parse(data['time'])

      # TODO: Make route required
      if 'route' in data:
        data['route'] = _parse_route(feed, data['route'])
      else:
        data['route'] = Route(feed, [])

    # Otherwise it is a series train
    else:
      # Validate required series keys
      if 'series' not in data:
        raise FeedDecodeError(f"Train id {id!r}: Key 'data' is missing")
      if 'time' not in data:
        raise FeedDecodeError(f"Train id {id!r}: Key 'data' is missing")

      # Validate optional series keys
      if 'begin_at_point' not in data:
        data['begin_at_point'] = None
      if 'end_at_point' not in data:
        data['end_at_point'] = None

      # Parse the series keys
      series = feed.get_train_series(data['series'])

      data['time'] = Time.parse(data['time'])
      data['agency'] = data.get('agency', series.agency)
      data['type'] = data.get('type', series.type)
      data['name'] = data.get('name', series.name)
      data['route'] = _calculate_route(series, data['time'], data['begin_at_point'], data['end_at_point'])

    # Register the train
    feed.register_train(id, **data)
  except (TypeError, ValueError) as err:
    raise FeedDecodeError(f"Train id {id!r}: {err}")


# Parse a route
def _parse_route(feed, datas):
  # Create a list for the points
  points = []

  # Iterate over the items
  for sequence, data in datas.items():
    # Validate required keys
    if 'type' not in data:
      raise FeedDecodeError(f"Point sequence {sequence!r}: Key 'type' is missing")

    # Return the point
    points.append(RoutePoint(feed, sequence, **data))

  # Return a new route with the points
  return Route(feed, points)


# Calculate the route of a series train
def _calculate_route(series, time, begin_at_point, end_at_point):
  # Get the route from the series
  route = copy.deepcopy(series.route)

  # Calculate the begin and end points
  if begin_at_point is not None:
    route = route[begin_at_point:]
  if end_at_point is not None:
    route = route[:end_at_point]

  # Calculate the time
  route = route.apply_time(time)

  # Return the route
  return route


# Class that defines a feed decode error
class FeedDecodeError(Exception):
  # Constructor
  def __init__(self, message):
    super().__init__(message)
