import collections
import copy
import functools

from .agency import Agency
from .route import Route
from .train_set import TrainSet
from .train_type import TrainType


# Class that defines a train
# Trains sort chronologically based on their times and ids
@functools.total_ordering
class Train:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Validate keyword arguments
    if isinstance(kwargs['agency'], str):
      try:
        kwargs['agency'] = self.feed.get_agency(kwargs['agency'])
      except KeyError as err:
        raise ValueError(f"Property 'agency': {kwargs['agency']} is not a registered agency")
    elif not isinstance(kwargs['agency'], Agency):
      raise TypeError(f"Property 'agency' is not a valid agency")

    if isinstance(kwargs['type'], str):
      try:
        kwargs['type'] = self.feed.get_train_type(kwargs['type'])
      except KeyError as err:
        raise ValueError(f"Property 'type': {kwargs['type']} is not a registered train type")
    elif not isinstance(kwargs['type'], TrainType):
      raise TypeError(f"Property 'type' is not a valid train type")

    if isinstance(kwargs['route'], list):
      kwargs['route'] = Route(kwargs['route'])
    elif not isinstance(kwargs['route'], Route):
      raise TypeError(f"Property 'route' is not a valid route")

    if 'set' in kwargs:
      if isinstance(kwargs['set'], str):
        try:
          kwargs['set'] = self.feed.get_train_set(kwargs['set'])
        except KeyError as err:
          raise ValueError(f"Property 'set': {kwargs['series']} is not a registered train set")
      elif not isinstance(kwargs['set'], TrainSet):
        raise TypeError(f"Property 'set' is not a valid train set")

    # Add required properties
    self.agency = kwargs['agency']
    self.type = kwargs['type']
    self.name = kwargs['name']
    self.route = kwargs['route']

    # Add optional properties
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.description = kwargs.get('description')  # Defaults to None
    self.priority = kwargs.get('priority', self.type.priority)  # Defaults to priority of self.type
    self.color_text = kwargs.get('color_text', 'inherit')  # Defaults to 'inherit'
    self.color_bg = kwargs.get('color_bg', 'inherit')  # Defaults to 'inherit'
    self.set = kwargs.get('set')  # Defaults to None

  # Return the departure point of this train
  @property
  def departure(self):
    return self.route.departure

  # Return the arrival point of this train
  @property
  def arrival(self):
    return self.route.arrival

  # Return the time of this train
  @property
  def time(self):
    return self.route.time

  # Return an item from this train with the specified index
  def __getitem__(self, index):
    if isinstance(index, slice):
      train = copy.copy(self)
      train.route = self.route[index]
      return train
    else:
      return self.route[index]

  # Return an iterator for this train
  def __iter__(self):
    return iter(self.route)

  # Return the length for this train
  def __len__(self):
    return len(self.route)

  # Return the boolean value for this train
  def __bool__(self):
    return bool(self.route)

  # Return the train beginning at the specified node
  def as_beginning_at_node(self, node, *, strip_points = False):
    train = copy.copy(self)
    train.route = train.route.as_beginning_at_node(node, strip_points = strip_points)
    return train

  # Return the train starting at the specified node
  def as_ending_at_node(self, node):
    train = copy.copy(self)
    train.route = train.route.as_ending_at_node(node, strip_points = strip_points)
    return train

  # Return if this train equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.time, self.id) < (other.time, other.id)

  # Return a copy of this train set
  def __copy__(self):
    return Train(self.feed, self.id,
      agency = self.agency,
      type = self.type,
      name = self.name,
      route = self.route,
      abbr = self.abbr,
      description = self.description,
      priority = self.priority,
      color_text = self.color_text,
      color_bg = self.color_bg,
    )

  # Return a deep copy of this train set
  def __deepcopy__(self, memo):
    return Train(self.feed, self.id,
      agency = self.agency,
      type = self.type,
      name = self.name,
      route = copy.deepcopy(self.route, memo),
      abbr = self.abbr,
      description = self.description,
      priority = self.priority,
      color_text = self.color_text,
      color_bg = self.color_bg,
    )

  # Return the internal representation for this train
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this train
  def __str__(self):
    return self.name

  # Return the JSON representation for this train
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      agency = self.agency.to_json(),
      type = self.type.to_json(),
      name = self.name,
      abbr = self.abbr,
      description = self.description,
      color_text = self.color_text,
      color_bg = self.color_bg,
      route = self.route.to_json(),
    )
