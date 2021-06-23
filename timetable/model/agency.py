import collections
import copy
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
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.description = kwargs.get('description')  # Defaults to None

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

  # Return a copy of this agency
  def __copy__(self):
    return Agency(self.feed, self.id,
      name = self.name,
      abbr = self.abbr,
      description = self.description,
    )

  # Return a deep copy of this agency
  def __deepcopy__(self, memo):
    return copy.copy(self)

  # Return the internal representation for this agency
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this agency
  def __str__(self):
    return self.abbr or self.name

  # Return the JSON representation for this agency
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      name = self.name,
      abbr = self.abbr,
      description = self.description,
    )
