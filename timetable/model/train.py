import functools

from .agency import Agency
from .route import Route
from .train_series import TrainSeries
from .train_type import TrainType


# Class that defines a train
# Trains sort chronologically based on their departure times
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

    if 'series' in kwargs:
      if isinstance(kwargs['series'], str):
        try:
          kwargs['series'] = self.feed.get_train_series(kwargs['series'])
        except KeyError as err:
          raise ValueError(f"Property 'series': {kwargs['series']} is not a registered train series")
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
    self.series = kwargs.get('series')  # Defaults to None

  # Return the departure point of this train
  @property
  def departure(self):
    return self.route.departure

  # Return the arrival point of this train
  @property
  def arrival(self):
    return self.route.arrival

  # Return the points or a range of points with the specified index, sequence or node(s)
  def __getitem__(self, index):
    if isinstance(index, slice):
      return Train(self.feed, self.id, agency = self.agency, type = self.type, name = self.name, route = self.route[index], abbr = self.abbr, description = self.description, series = self.series)
    else:
      return self.route[index]

  # Return if this train equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.departure.departure, self.id) < (other.departure.departure, other.id)

  # Return the internal representation for this train
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this train
  def __str__(self):
    return f"[{self.id}] {self.agency} - {self.type} - {self.name}"
