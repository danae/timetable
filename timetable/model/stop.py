import collections
import functools


# Class that defines a list of stops
class StopList:
  # Constructor
  def __init__(self, feed, stops = None):
    self.feed = feed
    self.stops = stops or []

  # Get the nodes that this stop list stops at or passes through
  def get_nodes(self, skips = False):
    return [stop.node for stop in self.stops if not skips or not stop.skip]

  # Return the stop with the specified node
  def get_stop_at_node(self, node, skips = False):
    for stop in self.stops:
      if stop.node == node and (not skips or not stop.skip):
        return stop

    raise ValueError(f"No stops found with node {node!r}")

  # Return the index of the stop with the specified node
  def get_stop_index_at_node(self, node, skips = False):
    return self.stops.index(self.get_stop_at_node(node))

  # Return if the stop list contains a stop with the specified node
  def has_stop_at_node(self, node, skips = False):
    try:
      self.get_stop_at_node(node)
      return True
    except ValueError:
      return False

  # Return the platform at the stop with the specified node
  def get_platform_at_node(self, node):
    try:
      return self.get_stop_at_node(node, True).arrival
    except ValueError:
      return None

  # Return the arrival time at the stop with the specified node
  def get_arrival_at_node(self, node):
    try:
      return self.get_stop_at_node(node, True).arrival
    except ValueError:
      return None

  # Return the departure time at the stop with the specified node
  def get_departure_at_node(self, node):
    try:
      return self.get_stop_at_node(node, True).departure
    except ValueError:
      return None

  # Return if the stop with the specified node is skipped
  def get_skip_at_node(self, node):
    try:
      return self.get_stop_at_node(node, True).skip
    except ValueError:
      return None

  # Return the stop list beginning at the specified node
  def beginning_at_node(self, node):
    if node is None:
      return self

    index = self.get_stop_index_at_node(node)
    return StopList(self.feed, self.stops[index:])

  # Return the stop list starting at the specified node
  def ending_at_node(self, node):
    if node is None:
      return self

    index = self.get_stop_index_at_node(node)
    return StopList(self.feed, self.stops[:index + 1])

  # Return the departure of this stop list
  @property
  def departure(self):
    return self.stops[0] if self.stops else None

  # Return the arrival of this stop list
  @property
  def arrival(self):
    return self.stops[-1] if self.stops else None

  # Return the canonical time of this stop list
  @property
  def canonical_time(self):
    return self.departure.departure or self.arrival.arrival

  # Return an iterator for this stop list
  def __iter__(self):
    return iter(self.stops)

  # Return the length for this stop list
  def __len__(self):
    return len(self.stops)

  # Return the boolean value for this stop list
  def __bool__(self):
    return bool(self.stops)

  # Return if this stop list equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.stops == other.stops

  # Return the string representation for this stop list
  def __str__(self):
    return '\n'.join(str(stop) for stop in self.stops)

  # Return the JSON representation for this stop list
  def to_json(self):
    return [stop.to_json() for stop in self.stops]


# Class that defines a stop
# Stop sort alphabetically by their sequences
@functools.total_ordering
class Stop:
  # Constructor
  def __init__(self, feed, stop_list, sequence, **kwargs):
    self.feed = feed
    self.stop_list = stop_list
    self.sequence = sequence

    # Add required properties
    self.node = kwargs['node']

    # Add optional properties
    self.platform = kwargs.get('platform')  # Defaults to None
    self.arrival = kwargs.get('a')  # Defaults to None
    self.departure = kwargs.get('d')  # Defaults to None
    self.skip = kwargs.get('skip', False)  # Defaults to False

  # Return if this stop equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return (self.stop_list, self.sequence) == (other.stop_list, other.sequence)

  # Return if this stop is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    if self.stop_list != other.stop_list:
      return NotImplemented
    return self.sequence < other.sequence

  # Return the internal representation for this stop
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.sequence}, node={self.node}, platform={self.platform}, arrival={self.arrival}, departure={self.departure}>"

  # Return the string representation for this stop
  def __str__(self):
    buffer = ""
    buffer += f"{self.arrival:%H:%M} A  " if self.arrival is not None else (" " * 9)
    buffer += f"{self.departure:%H:%M} D  " if self.departure is not None else (" " * 9)
    buffer += f"{self.node}"
    buffer += f" (platform {self.platform})" if self.platform is not None else ""
    return buffer

  # Return the JSON representation for this stop
  def to_json(self):
    return collections.OrderedDict(
      sequence = self.sequence,
      node = self.node.to_json(),
      platform = self.platform,
      arrival = format(self.arrival, "%H:%M") if self.arrival else None,
      departure = format(self.departure, "%H:%M") if self.departure else None,
      skip = self.skip,
    )
