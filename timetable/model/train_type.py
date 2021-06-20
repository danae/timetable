import functools


# Class that defines a train type
# Train types are sorted based on their priorities and names
@functools.total_ordering
class TrainType:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.name = kwargs['name']

    # Add optional properties
    self.abbr = kwargs.get('abbr')
    self.description = kwargs.get('description')
    self.priority = kwargs.get('priority')

  # Return if this train type equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this train type is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.priority, self.name) < (other.priority, other, name)

  # Return the internal representation for this train type
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this train type
  def __str__(self):
    return self.abbr or self.name
