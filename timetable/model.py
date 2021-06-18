import enum
import functools


# Class that defines an agency
# Agencies sort alphabetically based on their names
@functools.total_ordering
class Agency:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.name = kwargs['name']

    # Add optional properties
    self.abbr = kwargs.get('abbr')
    self.desc = kwargs.get('desc')

  # Return if this agency equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this agency is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.name == other.name

  # Return the string representation for this agency
  def __str__(self):
    return self.abbr or self.name


# Enum that defines the type of a station
class StationType(enum.Enum):
  unspecified = 0
  station = 1
  split = 2
  over = 3
  cross = 4
  fork = 5
  bridge = 6
  border = 7


# Class that defines a station
# Stations sort aplhabetically based on their names
@functools.total_ordering
class Station:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.name = kwargs['name']

    # Add optional properties
    self.short_name = kwargs.get('short_name')
    self.desc = kwargs.get('desc')
    self.type = kwargs.get('type')
    self.node = kwargs.get('node', False)
    self.train_types = kwargs.get('train_types', [])
    self.on_call = kwargs.get('on_call', False)
    self.x = kwargs.get('x')
    self.y = kwargs.get('y')

  # Return if this station equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this station is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.name < other.name

  # Return the string representation for this station
  def __str__(self):
    return self.name


# Class that defines a train type
class TrainType:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.name = kwargs['name']
    self.abbr = kwargs['abbr']

    # Add optional properties
    self.desc = kwargs.get('desc')

  # Return if this train type equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return the string representation for this train type
  def __str__(self):
    return self.abbr or self.name


# Class that defines a train series
# Train series sort alphabetically based on their ids
@functools.total_ordering
class TrainSeries:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Validate keyword arguments
    if not isinstance(kwargs['agency'], Agency):
      raise TypeError(f"Property 'agency' is not a valid agency")
    if not isinstance(kwargs['type'], TrainType):
      raise TypeError(f"Property 'type' is not a valid train type")

    # Add required properties
    self.agency = kwargs['agency']
    self.type = kwargs['type']
    self.name = kwargs['name']
    self.route = kwargs.get('route', [])

    # Add optional properties
    self.abbr = kwargs.get('abbr')
    self.desc = kwargs.get('desc')

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

  # Return the string representation for this train series
  def __str__(self):
    return f"{self.agency} - {self.type} - {self.name}"

  # Return a report for this train series
  def report(self):
    buffer = f"Train series {self}"
    for point in self.route:
      buffer += f"\n  {point}"
    return buffer


# Class that defines a train
# Trains sort chronologically based on their departure times
@functools.total_ordering
class Train:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Validate keyword arguments
    if not isinstance(kwargs['agency'], Agency):
      raise TypeError(f"Property 'agency' is not a valid agency")
    if not isinstance(kwargs['type'], TrainType):
      raise TypeError(f"Property 'type' is not a valid train type")
    if 'series' in kwargs and not isinstance(kwargs['series'], TrainSeries):
      raise TypeError(f"Property 'series' is not a valid train series")

    # Add required properties
    self.agency = kwargs['agency']
    self.type = kwargs['type']
    self.name = kwargs['name']
    self.route = kwargs['route']

    # Add optional properties
    self.abbr = kwargs.get('abbr')
    self.desc = kwargs.get('desc')
    self.series = kwargs.get('series')

  # Return the departure point of this train
  @property
  def departure_point(self):
    return self.route[0]

  # Return the departure time of this train
  @property
  def departure(self):
    return self.departure_point.departure

  # Return the arrival point of this train
  @property
  def arrival_point(self):
    return self.route[-1]

  # Return the arrival time of this train
  @property
  def arrival(self):
    return self.arrival_point.arrival

  # Return if this train equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.departure, self.id) < (other.departure, other.id)

  # Return the string representation for this train type
  def __str__(self):
    return f"{self.agency} - {self.type} - {self.name}"

  # Return a report for this train series
  def report(self):
    buffer = f"Train {self}"
    for point in self.route:
      buffer += f"\n  {point}"
    return buffer


# Enum that defines the type of a point
class PointType(enum.Enum):
  over = 0
  begin = 1
  stop = 2
  end = 3


# Class that defines a point in a train itinerary
# Points sort alphabetically by their orders
@functools.total_ordering
class Point:
  # Constructor
  def __init__(self, order, type, station, arrival = None, departure = None):
    self.order = order
    self.type = type
    self.station = station
    self.arrival = arrival
    self.departure = departure

  # Return if this point equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.order == other.order

  # Return if this point is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.order < other.order

  # Return the string representation of this stop
  def __str__(self):
    buffer = ""
    buffer += f"{self.arrival:%H:%M} A  " if self.arrival is not None else (" " * 9)
    buffer += f"{self.departure:%H:%M} D  " if self.departure is not None else (" " * 9)
    buffer += f"{self.station}"
    return buffer
