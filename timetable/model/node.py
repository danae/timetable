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

    # Validate keyword arguments
    if 'type' in kwargs:
      if isinstance(kwargs['type'], str):
        try:
          kwargs['type'] = NodeType[kwargs['type']]
        except ValueError as err:
          raise ValueError(f"Property 'type': {err}")
      elif not isinstance(kwargs['type'], NodeType):
        raise TypeError("Property 'type' is not a valid node type")

    # Add required properties
    self.name = kwargs['name']

    # Add optional properties
    self.short_name = kwargs.get('short_name', self.name)  # Defaults to self.name
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.description = kwargs.get('description')  # Defaults to None
    self.x = self.lon = kwargs.get('x') or kwargs.get('lon')  # Defaults to None
    self.y = self.lat = kwargs.get('y') or kwargs.get('lat')  # Defaults to None
    self.type = kwargs.get('type', NodeType.station)  # Defaults to NodeType.station
    self.node = kwargs.get('node', False)  # Defaults to False
    self.train_types = kwargs.get('train_types', [])  # Defaults to []
    self.on_call = kwargs.get('on_call', False)  # Defaults to False

  # Return if this node equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this node is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.name, self.type) < (other.name, other.type)

  # Return the internal representation for this node
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this node
  def __str__(self):
    return self.name


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
