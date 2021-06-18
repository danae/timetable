import functools
import re


# Class that defines a lenient time
@functools.total_ordering
class LenientTime:
  # Constructor
  def __init__(self, hours, minutes, seconds = 0):
    self.hours = hours
    self.minutes = minutes
    self.seconds = seconds

  # Return if this time is equal to another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return (self.hours, self.minutes, self.seconds) == (other.hours, other.minutes, other.seconds)

  # Return if this time is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.hours, self.minutes, self.seconds) < (other.hours, other.minutes, other.seconds)

  # Add two lenient times
  def __add__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented

    hours = self.hours + other.hours
    minutes = self.minutes + other.minutes
    seconds = self.seconds + other.seconds

    while seconds >= 60:
      seconds -= 60
      minutes += 1

    while minutes >= 60:
      minutes -= 60
      hours += 1

    return LenientTime(hours, minutes, seconds)

  # Return a formatted representation of the time
  def __format__(self, format_spec):
    string = format_spec
    string = string.replace('%H', f"{self.hours % 24:02d}")
    string = string.replace('%M', f"{self.minutes:02d}")
    string = string.replace('%S', f"{self.seconds:02d}")
    return string

  # Return the string representation of the time
  def __str__(self):
    return self.__format__('%H:%M:%S')

  # Create a time from a string
  @classmethod
  def parse(cls, string):
    if not (match := re.fullmatch('(\d{2}):(\d{2})(?:(\d{2}))?', string)):
      raise ValueError(f"Invalid time format: {string}")

    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = int(match.group(3) or 0)
    return cls(hours, minutes, seconds)
