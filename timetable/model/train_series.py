import functools

from .agency import Agency
from .route import Route
from .train_type import TrainType


# Class that defines a train series
# Train series sort alphabetically based on their ids
@functools.total_ordering
class TrainSeries:
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

  # Return if this train series equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train series is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.id < other.id

  # Return the internal representation for this train series
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this train series
  def __str__(self):
    return f"{self.agency} - {self.type} - {self.name}"

  # Return a report for this train series
  def report(self):
    buffer = f"Train series {self}"
    for point in self.route:
      buffer += f"\n  {point}"
    return buffer
