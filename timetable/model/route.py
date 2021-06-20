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

    # TODO: Make route required
    #if not self.points:
    #  raise ValueError("Points cannot be empty")

  # Return the departure point of this route
  @property
  def departure(self):
    return self.points[0]

  # Return the arrival point of this route
  @property
  def arrival(self):
    return self.points[-1]

  # Return the point with the specified sequence
  def get_point_at_sequence(self, sequence):
    try:
      return next(filter(lambda p: p.sequence == sequence, self.points))
    except StopIteration:
      raise ValueError(f"No points found with sequence {sequence!r}")

  # Return the index of the point with the specified sequence
  def get_index_at_sequence(self, sequence):
    return self.points.index(self.get_point_at_sequence(sequence))

  # Return the point with the specified node
  def get_point_at_node(self, node):
    try:
      return next(filter(lambda p: p.node == node, self.points))
    except StopIteration:
      raise ValueError(f"No points found with node {node!r}")

  # Return the index of the point with the specified node
  def get_index_at_node(self, node):
    return self.points.index(self.get_point_at_node(node))

  # Return the points or a range of points with the specified index, sequence or node(s)
  def __getitem__(self, index):
    # Check the type of the index
    if isinstance(index, int):
      # Index is an actual index
      return self.points[index]
    elif isinstance(index, str):
      # Index is a sequence
      return self.get_point_at_sequence(index)
    elif isinstance(index, Node):
      # Index is a node
      return self.get_point_at_node(index)
    elif isinstance(index, slice):
      # Check if the step parameter is not weird
      if index.step is not None and index.step != 1:
        raise TypeError("Slices must have a step of 1")

      # Check if the start and stop parameters are both None
      if index.start is None and index.stop is None:
        return Route(self.feed, copy.deepcopy(self.points))

      # Check the type of the slice indices
      if (isinstance(index.start, int) or index.start is None) and (isinstance(index.stop, int) or index.stop is None):
        # Index is a slice of actual indices
        start_index = index.start
        end_index = index.stop
      elif (isinstance(index.start, str) or index.start is None) and (isinstance(index.stop, str) or index.stop is None):
        # Index is a slice of sequences
        start_index = self.get_index_at_sequence(index.start) if index.start is not None else None
        end_index = self.get_index_at_sequence(index.stop) + 1 if index.stop is not None else None
      elif (isinstance(index.start, None) or index.start is None) and (isinstance(index.stop, None) or index.stop is None):
        # Index is a slice of nodes
        start_index = self.get_index_at_node(index.start) if index.start is not None else None
        end_index = self.get_index_at_node(index.stop) + 1 if index.stop is not None else None
      else:
        # Invalid slice index type
        raise TypeError("Slice indices must be both an int, a string or a node")

      # Create a new route using the start and end indices
      route = Route(self.feed, copy.deepcopy(self.points)[start_index:end_index])

      # Make the departure point a begin
      if route.departure.type != RoutePointType.over:
        route.departure.type = RoutePointType.begin
        route.departure.arrival = None

      # Make the arrival point an end
      if route.arrival.type != RoutePointType.over:
        route.arrival.type = RoutePointType.end
        route.arrival.departure = None

      # Return the route
      return route
    else:
      # Invalid index type
      raise TypeError("Index must be an int, a string or a node")

  # Apply a time to all points
  def apply_time(self, time):
    # Mapping function
    def apply(point):
      #print(f"{point!r}")
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

  # Return the string representation for this route
  def __str__(self):
    buffer = f"{self.departure.departure:%H:%M} {self.departure.node} - {self.arrival.arrival:%H:%M} {self.arrival.node}"
    for point in self.points:
      buffer += f"\n  {point}"
    return buffer

  # Return a deep copy of this route
  def __deepcopy__(self, memo):
    points = copy.deepcopy(self.points, memo)

    return Route(self.feed, self.points)


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

  # Return a deep copy of this route point
  def __deepcopy__(self, memo):
    arrival = copy.deepcopy(self.arrival, memo)
    departure = copy.deepcopy(self.departure, memo)

    return RoutePoint(self.feed, self.sequence, type = self.type, node = self.node, platform = self.platform, arrival = arrival, departure = departure)


# Enum that defines the type of a route point
class RoutePointType(enum.Enum):
  over = 0
  begin = 1
  stop = 2
  end = 3
