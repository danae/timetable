import collections
import enum
import functools


# Class that defines a node
# Nodes sort aplhabetically based on their names and types
@functools.total_ordering
class Node:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add requiredproperties
    self.name = kwargs['name']

    # Add optional properties
    self.short_name = kwargs.get('short_name', self.name)  # Defaults to self.name
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.type = kwargs.get('type', NodeType.station)  # Defaults to NodeType.station
    self.x = kwargs.get('x') or kwargs.get('lon')  # Defaults to None
    self.y = kwargs.get('y') or kwargs.get('lat')  # Defaults to None
    self.node = kwargs.get('node', False)  # Defaults to False
    self.modalities = kwargs.get('modalities', [])  # Defaults to []
    self.remarks = kwargs.get('remarks', {})  # Defaults to {}
    self.services = kwargs.get('services', {})  # Defaults to {}

  # Return the routes that have a stop at this node
  def get_routes_with_node(self, skips = False):
    return filter(lambda route: route.stops.has_stop_at_node(self, skips), self.feed.get_routes())

  # Return the trips that have a stop at this node
  def get_trips_with_node(self, skips = False):
    return filter(lambda trip: trip.stops.has_stop_at_node(self, skips), self.feed.get_trips())

  # Return the transfers at this node
  def get_transfers_with_node(self):
    return []

  # Return if this node equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this node is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.name, self.type, self.id) < (other.name, other.type, other.id)

  # Return the hash for this node
  def __hash__(self):
    return hash((self.id))

  # Return the internal representation for this node
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this node
  def __str__(self):
    return self.name

  # Return the JSON representation for this node
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      name = self.name,
      short_name = self.short_name,
      abbr = self.abbr,
      description = self.description,
      type = self.type.name,
      x = self.x,
      y = self.y,
      node = self.node,
      modalities = self.modalities,
      remarks = self.remarks,
      services = self.services,
    )


# Enum that defines the type of a node
class NodeType(enum.Enum):
  unspecified = 0
  station = 1
  split = 2
  over = 3
  cross = 4
  fork = 5
  bridge = 6
  border = 7
