import toml

from .feed import Feed
from .model import Agency, StationType, Station, TrainType, TrainSeries, Train, PointType, Point
from .utils import LenientTime


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

  # Load the agencies
  for id, agency_data in data['agencies'].items():
    _parse_agency(feed, id, agency_data)

  # Load the stations
  for id, station_data in data['stations'].items():
    _parse_station(feed, id, station_data)

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
  # Validate required keys
  if 'name' not in data:
    raise FeedDecodeError(f"Agency id {id!r}: Key 'name' is missing")

  # Validate optional keys
  if 'abbr' not in data:
    data['abbr'] = None

  # Register the agency
  feed.register_agency(id, **data)


# Parse a station
def _parse_station(feed, id, data):
  # Validate required keys
  if 'name' not in data:
    raise FeedDecodeError(f"Station id {id!r}: Key 'name' is missing")

  # Validate optional keys
  if 'short_name' not in data:
    data['short_name'] = data['name']
  if 'desc' not in data:
    data['desc'] = None
  if 'type' not in data:
    data['type'] = 'station'
  if 'node' not in data:
    data['node'] = False
  if 'train_types' not in data:
    data['train_types'] = []
  if 'on_call' not in data:
    data['on_call'] = False
  if 'x' not in data:
    data['x'] = None
  if 'y' not in data:
    data['y'] = None

  # Parse the keys
  if data['type'] is not None:
    data['type'] = StationType[data['type']]

  # Register the station
  feed.register_station(id, **data)


# Parse a train type
def _parse_train_type(feed, id, data):
  # Validate required keys
  if 'name' not in data:
    raise FeedDecodeError(f"Train type id {id!r}: Key 'name' is missing")

  # Validate optional keys
  if 'abbr' not in data:
    data['abbr'] = None
  if 'desc' not in data:
    data['desc'] = None

  # Register the train type
  feed.register_train_type(id, **data)


# Parse a train series
def _parse_train_series(feed, id, data):
  # Validate required keys
  if 'agency' not in data:
    raise FeedDecodeError(f"Train series id {id!r}: Key 'agency' is missing")
  if 'type' not in data:
    raise FeedDecodeError(f"Train series id {id!r}: Key 'type' is missing")
  if 'name' not in data:
    raise FeedDecodeError(f"Train series id {id!r}: Key 'name' is missing")
  if 'abbr' not in data:
    raise FeedDecodeError(f"Train series id {id!r}: Key 'abbr' is missing")
  if 'route' not in data:
    #raise FeedDecodeError(f"Train series id {id!r}: Key 'route' is missing")
    data['route'] = {}

  # Validate optional keys
  if 'desc' not in data:
    data['desc'] = None

  # Parse the keys
  data['agency'] = feed.get_agency(data['agency'])
  data['type'] = feed.get_train_type(data['type'])
  data['route'] = [_parse_point(feed, id, point_order, point_data) for point_order, point_data in data['route'].items()]

  # Register the train series
  feed.register_train_series(id, **data)


# Parse a train
def _parse_train(feed, id, data):
  # If the train has a route, then it is a standalone train
  if 'route' in data:
    # Validate required keys
    if 'agency' not in data:
      raise FeedDecodeError(f"Train id {id!r}: Key 'agency' is missing")
    if 'type' not in data:
      raise FeedDecodeError(f"Train id {id!r}: Key 'type' is missing")
    if 'name' not in data:
      raise FeedDecodeError(f"Train id {id!r}: Key 'name' is missing")

    # Parse the keys
    data['series'] = None
    data['agency'] = feed.get_agency(data['agency'])
    data['type'] = feed.get_train_type(data['type'])
    data['route'] = [_parse_point(feed, id, point_order, point_data) for point_order, point_data in data['route'].items()]

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
    data['series'] = feed.get_train_series(data['series'])
    data['time'] = LenientTime.parse(data['time'])
    data['agency'] = feed.get_agency(data['agency']) if 'agency' in data else data['series'].agency
    data['type'] = feed.get_train_type(data['type']) if 'type' in data else data['series'].type
    data['name'] = data['name'] if 'name' in data else data['series'].name
    data['route'] = _calculate_route(data['series'], data['time'], data['begin_at_point'], data['end_at_point'])

  # Register the train
  feed.register_train(id, **data)


# Parse a point
def _parse_point(feed, train_id, order, data):
  # Validate required keys
  if 'type' not in data:
    raise FeedDecodeError(f"Point order {order!r}: Key 'name' is missing")

  # Validate optional keys
  if 'a' not in data:
    data['a'] = None
  if 'd' not in data:
    data['d'] = None

  # Parse the keys
  data['type'] = PointType[data['type']]
  data['station'] = feed.get_station(data['station'])
  if data['a'] is not None:
    data['a'] = LenientTime.parse(data['a'])
  if data['d'] is not None:
    data['d'] = LenientTime.parse(data['d'])

  # Return the point
  return Point(order, data['type'], data['station'], data['a'], data['d'])


# Calculate the route of a series train
def _calculate_route(series, time, begin_at_point, end_at_point):
  # Get the route from the series
  route = series.route

  # Calculate the begin and end points
  if begin_at_point is not None:
    begin_point = next(filter(lambda point: point.order == begin_at_point, route), None)
    if begin_point is None:
      raise FeedDecodeError(f"Point order {begin_at_point} is undefined")
    begin_index = route.index(begin_point)
    route = route[begin_index:]

  if end_at_point is not None:
    end_point = next(filter(lambda point: point.order == end_at_point, route), None)
    if end_point is None:
      raise FeedDecodeError(f"Point order {begin_at_point} is undefined")
    end_index = route.index(end_point)
    route = route[:end_index + 1]

  # Create a new route
  actual_route = []
  for i, point in enumerate(route):
    # Create a new point
    actual_a = time + point.arrival if point.type in [PointType.stop, PointType.end] else None
    actual_d = time + point.departure if point.type in [PointType.begin, PointType.stop] else None
    actual_point = Point(point.order, point.type, point.station, actual_a, actual_d)

    # If this is the first point, make the point a begin
    if i == 0 and actual_point.type != PointType.over:
      actual_point.type = PointType.begin
      actual_point.arrival = None

    # If this is the last point, make the point an end
    if i == len(route) - 1 and actual_point.type != PointType.over:
      actual_point.type = PointType.end
      actual_point.departure = None

    # Add the actual point
    actual_route.append(actual_point)

  # Return the actual route
  return actual_route


# Class that defines a feed decode error
class FeedDecodeError(Exception):
  # Constructor
  def __init__(self, message):
    super().__init__(message)
