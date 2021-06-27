from .utils import Time


# Class that defines a transfer
class Transfer:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.begin = kwargs['begin']
    self.end = kwargs['end']
    self.duration = kwargs.get('duration', Time(0))  # Defaults to 0

  # Return if this transfer equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return (self.stop_list, self.sequence) == (other.stop_list, other.sequence)

  # Return if this transfer is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    if self.stop_list != other.stop_list:
      return NotImplemented
    return self.sequence < other.sequence

  # Return the internal representation for this stop
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this stop
  def __str__(self):
    return f"Transfer between {self.begin} and {self.end}"

  # Return the JSON representation for this stop
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      begin = self.begin,
      end = self.end,
      duration = self.duration,
    )
