import collections
import copy
import enum
import functools

from .node import Node
from .utils import Time


# Class that defines a route
class Route:
  # Constructor
  def __init__(self, feed, points):
    self.feed = feed
    self.points = points

  # Return the departure point of this route
  @property
  def departure(self):
    return self.points[0] if self.points else None

  # Return the arrival point of this route
  @property
  def arrival(self):
    return self.points[-1] if self.points else None

  # Return the time of this route
  @property
  def time(self):
    return self.departure.departure or self.arrival.arrival

  # Return an item from this route with the specified index
  def __getitem__(self, index):
    if isinstance(index, slice):
      return Route(self.feed, self.points[index])
    else:
      return self.points[index]

  # Return an iterator for this route
  def __iter__(self):
    return iter(self.points)

  # Return the length for this route
  def __len__(self):
    return len(self.points)

  # Return the boolean value for this route
  def __bool__(self):
    return bool(self.points)

  # Strip points in the route
  def _strip_points(self):
    if len(self.points) == 0:
      return
    elif len(self.points) == 1:
      if self.points[0].type != RoutePointType.over:
        self.points[0].type = RoutePointType.end
        self.points[0].departure = None
    else:
      if self.points[0].type != RoutePointType.over:
        self.points[0].type = RoutePointType.begin
        self.points[0].arrival = None
      if self.points[-1].type != RoutePointType.over:
        self.points[-1].type = RoutePointType.end
        self.points[-1].departure = None

  # Return the point with the specified sequence
  def get_point_at_sequence(self, sequence):
    try:
      return next(filter(lambda p: p.sequence == sequence, self.points))
    except StopIteration:
      raise ValueError(f"No points found with sequence {sequence!r}")

  # Return the index of the point with the specified sequence
  def get_index_at_sequence(self, sequence):
    return self.points.index(self.get_point_at_sequence(sequence))

  # Return the route beginning at the specified sequence
  def as_beginning_at_sequence(self, sequence, *, strip_points = True):
    index = self.get_index_at_sequence(sequence)
    route = Route(self.feed, copy.deepcopy(self.points)[index:])
    if strip_points:
      route._strip_points()
    return route

  # Return the route starting at the specified sequence
  def as_ending_at_sequence(self, sequence, *, strip_points = True):
    index = self.get_index_at_sequence(sequence)
    route = Route(self.feed, copy.deepcopy(self.points)[:index+1])
    if strip_points:
      route._strip_points()
    return route

  # Return the point with the specified node
  def get_point_at_node(self, node, *, departures = True, arrivals = True, overs = False):
    try:
      point = next(filter(lambda p: p.node == node, self.points))

      if point.type == RoutePointType.over and not overs:
        raise ValueError(f"Only points without a stop found with node {node!r}")
      if point.type != RoutePointType.end and not departures:
        raise ValueError(f"Only departure points found with node {node!r}")
      if point.type == RoutePointType.end and not arrivals:
        raise ValueError(f"Only arrival points found with node {node!r}")

      return point
    except StopIteration:
      raise ValueError(f"No points found with node {node!r}")

  # Return if the route contains a point with the specified node
  def has_point_at_node(self, node, *, departures = True, arrivals = True, overs = False):
    try:
      self.get_point_at_node(node, departures = departures, arrivals = arrivals, overs = overs)
      return True
    except ValueError:
      return False

  # Return the index of the point with the specified node
  def get_index_at_node(self, node, *, departures = True, arrivals = True, overs = False):
    return self.points.index(self.get_point_at_node(node, departures = departures, arrivals = arrivals, overs = overs))

  # Return the route beginning at the specified node
  def as_beginning_at_node(self, node, *, strip_points = False):
    index = self.get_index_at_node(node)
    route = Route(self.feed, copy.deepcopy(self.points)[index:])
    if strip_points:
      route._strip_points()
    return route

  # Return the route starting at the specified node
  def as_ending_at_node(self, node, *, strip_points = False):
    index = self.get_index_at_node(node)
    route = Route(self.feed, copy.deepcopy(self.points)[index:])
    if strip_points:
      route._strip_points()
    return route

  # Apply a time to all points
  def apply_time(self, time):
    # Mapping function
    def apply(point):
      arrival = time + point.arrival if point.type in [RoutePointType.stop, RoutePointType.end] else None
      departure = time + point.departure if point.type in [RoutePointType.begin, RoutePointType.stop] else None
      return RoutePoint(self.feed, point.sequence, type = point.type, node = point.node, arrival = arrival, departure = departure)

    # Create a new route from the points
    return Route(self.feed, list(map(apply, self.points)))

  # Return if this route equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.points == other.points

  # Return a copy of this route
  def __copy__(self):
    return Route(self.feed, self.points)

  # Return a deep copy of this route
  def __deepcopy__(self, memo):
    return Route(self.feed, copy.deepcopy(self.points, memo))

  # Return the string representation for this route
  def __str__(self):
    buffer = f"{self.departure.departure:%H:%M} {self.departure.node} - {self.arrival.arrival:%H:%M} {self.arrival.node}"
    for point in self.points:
      buffer += f"\n  {point}"
    return buffer

  # Return the JSON representation for this route
  def to_json(self):
    return [p.to_json() for p in self.points]


# Class that defines a point in a route
# Points sort alphabetically by their sequences
@functools.total_ordering
class RoutePoint:
  # Constructor
  def __init__(self, feed, sequence, **kwargs):
    self.feed = feed
    self.sequence = sequence

    # Validate keyword arguments
    if isinstance(kwargs['type'], str):
      try:
        kwargs['type'] = RoutePointType[kwargs['type']]
      except ValueError as err:
        raise ValueError(f"Property 'type': {err}")
    elif not isinstance(kwargs['type'], RoutePointType):
      raise TypeError("Property 'type' is not a valid route point type")

    if isinstance(kwargs['node'], str):
      try:
        kwargs['node'] = self.feed.get_node(kwargs['node'])
      except KeyError as err:
        raise ValueError(f"Property 'node': {kwargs['node']} is not a registered node")
    elif not isinstance(kwargs['node'], Node):
      raise TypeError("Property 'node' is not a valid node")

    kwargs['arrival'] = kwargs.get('arrival') or kwargs.get('a')
    if kwargs['arrival'] is not None:
      if isinstance(kwargs['arrival'], str):
        try:
          kwargs['arrival'] = Time.parse(kwargs['arrival'])
        except ValueError as err:
          raise ValueError(f"Property 'arrival': {err}")
      elif not isinstance(kwargs['arrival'], Time):
        raise TypeError("Property 'arrival' is not a valid time")

    kwargs['departure'] = kwargs.get('departure') or kwargs.get('d')
    if kwargs['departure'] is not None:
      if isinstance(kwargs['departure'], str):
        try:
          kwargs['departure'] = Time.parse(kwargs['departure'])
        except ValueError as err:
          raise ValueError(f"Property 'departure': {err}")
      elif not isinstance(kwargs['departure'], Time):
        raise TypeError("Property 'departure' is not a valid time")

    # Add required properties
    self.type = kwargs['type']
    self.node = kwargs['node']

    # Add optional properties
    self.platform = kwargs.get('platform')  # Defaults to None
    self.arrival = kwargs.get('arrival')  # Defaults to None
    self.departure = kwargs.get('departure')  # Defaults to None

  # Return if this route point equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.sequence == other.sequence

  # Return if this route point is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.sequence < other.sequence

  # Return a copy of this route point
  def __copy__(self):
    return RoutePoint(self.feed, self.sequence,
      type = self.type,
      node = self.node,
      platform = self.platform,
      arrival = self.arrival,
      departure = self.departure,
    )

  # Return a deep copy of this route point
  def __deepcopy__(self, memo):
    return RoutePoint(self.feed, self.sequence,
      type = self.type,
      node = self.node,
      platform = self.platform,
      arrival = copy.deepcopy(self.arrival, memo),
      departure = copy.deepcopy(self.departure, memo),
    )

  # Return the internal representation for this route point
  def __repr__(self):
    return f"{self.__class__.__name__}({self.feed!r}, {self.sequence!r}, type={self.type!r}, node={self.node!r}, platform={self.platform!r}, arrival={self.arrival!r}, departure={self.departure!r})"

  # Return the string representation for this route point
  def __str__(self):
    buffer = ""
    buffer += f"{self.arrival:%H:%M} A  " if self.arrival is not None else (" " * 9)
    buffer += f"{self.departure:%H:%M} D  " if self.departure is not None else (" " * 9)
    buffer += f"{self.node}"
    return buffer

  # Return the JSON representation for this route point
  def to_json(self):
    return collections.OrderedDict(
      sequence = self.sequence,
      type = self.type.name,
      node = self.node.to_json(),
      platform = self.platform,
      arrival = format(self.arrival, "%H:%M") if self.arrival else None,
      departure = format(self.departure, "%H:%M") if self.departure else None,
    )


# Enum that defines the type of a route point
class RoutePointType(enum.Enum):
  over = 0
  begin = 1
  stop = 2
  end = 3
