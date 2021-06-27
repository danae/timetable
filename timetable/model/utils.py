import copy
import datetime
import functools
import re


# Class that defines a time with a day offset
@functools.total_ordering
class Time:
  # Constructor
  def __init__(self, seconds):
    self.seconds = seconds

  # Return the time components
  @property
  def day(self):
    return self.seconds // 86400

  @property
  def hour(self):
    return (self.seconds % 86400) // 3600

  @property
  def minute(self):
    return ((self.seconds % 86400) % 3600) // 60

  @property
  def second(self):
    return ((self.seconds % 86400) % 3600) % 60

  # Return if this time equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.seconds == other.seconds

  # Return if this time is less than another object
  def __lt__(self, other):
    if isinstance(other, (int, float)):
        return self.seconds < other
    if not isinstance(other, self.__class__):
      return NotImplemented
    return self.seconds < other.seconds

  # Add two time objects
  def __add__(self, other):
    # TODO: Add a duration type and implement this properly
    if not isinstance(other, self.__class__):
      return NotImplemented
    return Time(self.seconds + other.seconds)

  # Subtract two time objects
  def __sub__(self, other):
    # TODO: Add a duration type and implement this properly
    if not isinstance(other, self.__class__):
      return NotImplemented
    if other.seconds > self.seconds:
      raise ValueError(f"Difference between {self} and {other} is negative")
    return Time(self.seconds - other.seconds)

  # Return a copy of this time
  def __copy__(self):
    return Time(self.seconds)

  # Return the internal representation for this time
  def __repr__(self):
    return f"{self.__class__.__name__}({self.seconds!r})"

  # Return a formatted representation for this time
  def __format__(self, format_spec):
    string = format_spec or '%H:%M:%S'
    string = string.replace('%H', f"{self.hour:02d}")
    string = string.replace('%M', f"{self.minute:02d}")
    string = string.replace('%S', f"{self.second:02d}")
    return string

  # Return the string representation for this time
  def __str__(self):
    return format(self)


  # Return a time from a (day, hour, minute, second) tuple
  @classmethod
  def fromtime(cls, day, hour, minute, second):
    return cls(day * 86400 + hour * 3600 + minute * 60 + second)

  # Return a time from a string
  @classmethod
  def fromstring(cls, string):
    # Match the string
    if not isinstance(string, str):
      raise TypeError(f"Invalid time format type: {type(string)}, must be str")
    if not (match := re.fullmatch('(\d{2})(?:\:(\d{2})(?:\:(\d{2}))?)?', string)):
      raise ValueError(f"Invalid time format value: {string!r}")

    # Get the variables
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    second = int(match.group(3) or 0)

    # Return the time
    return cls.fromtime(0, hour, minute, second)

  # Return the current time
  @classmethod
  def now(cls):
    now = datetime.datetime.now()
    return cls.fromtime(0, now.hour, now.minute, now.second)
