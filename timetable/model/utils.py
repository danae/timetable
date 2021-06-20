import datetime
import functools
import re


# Class that defines a time with a day offset
@functools.total_ordering
class Time:
  # Constructor
  def __init__(self, day, hour = 0, minute = 0, second = 0):
    self.day = day
    self.time = datetime.time(hour, minute, second)

  # Return the time components
  @property
  def hour(self):
    return self.time.hour

  @property
  def minute(self):
    return self.time.minute

  @property
  def second(self):
    return self.time.second

  # Return if this time equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return (self.day, self.time) == (other.day, other.time)

  # Return if this time is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.day, self.time) < (other.day, other.time)

  # Add two time objects
  def __add__(self, other):
    # TODO: Define proper duration class for addition and subtraction
    if not isinstance(other, self.__class__):
      return NotImplemented

    seconds_self = self.day * 86400 + self.hour * 3600 + self.minute * 60 + self.second
    seconds_other = other.day * 86400 + other.hour * 3600 + other.minute * 60 + other.second

    second = seconds_self + seconds_other
    day, second = divmod(second, 86400)
    hour, second = divmod(second, 3600)
    minute, second = divmod(second, 60)

    return Time(day, hour, minute, second)

  # Return the internal representation for this time
  def __repr__(self):
    return f"{self.__class__.__name__}({self.day!r}, {self.hour!r}, {self.minute!r}, {self.second!r})"

  # Return a formatted representation for this time
  def __format__(self, format_spec):
    return self.time.__format__(format_spec)

  # Return the string representation for this time
  def __str__(self):
    return self.time.__format__('%H:%M:%S')


  # Return the current time
  @classmethod
  def now(cls):
    now = datetime.datetime.now()
    return cls(0, now.hour, now.minute, now.second)

  # Parse a linient time, i.e. a time where the hours can increase below 0 or above 23
  @classmethod
  def parse(cls, string):
    # Match the string
    if not isinstance(string, str):
      raise TypeError(f"Invalid time format type: {type(string)}, must be str")
    if not (match := re.fullmatch('(\d{2})(?:\:(\d{2})(?:\:(\d{2}))?)?', string)):
      raise ValueError(f"Invalid time format value: {string!r}")

    # Get the variables
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    second = int(match.group(3) or 0)

    # Adjust the variables to days and hours
    day, hour = divmod(hour, 24)

    # Return the time
    return cls(day, hour, minute, second)
