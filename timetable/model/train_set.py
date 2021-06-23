import collections
import copy
import functools

from .agency import Agency
from .route import Route
from .train_type import TrainType


# Class that defines a train set
# Train sets sort alphabetically based on their ids
@functools.total_ordering
class TrainSet:
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

    if 'series' in kwargs:
      if isinstance(kwargs['series'], str):
        kwargs['series'] = self.feed.get_train_series(kwargs['series'])
      elif not isinstance(kwargs['series'], TrainSeries):
        raise TypeError(f"Property 'series' is not a valid train series")

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

  # Return if this train set equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train set is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.id < other.id

  # Return a copy of this train set
  def __copy__(self):
    return TrainSet(self.feed, self.id,
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
    return TrainSet(self.feed, self.id,
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

  # Return the internal representation for this train set
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this train set
  def __str__(self):
    return f"{self.agency} - {self.type} - {self.name}"

  # Return the JSON representation for this train set
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      agency = self.agency.to_json(),
      type = self.type.to_json(),
      name = self.name,
      abbr = self.abbr,
      description = self.description,
      priority = self.priority,
      color_text = self.color_text,
      color_bg = self.color_bg,
      route = self.route.to_json(),
    )
