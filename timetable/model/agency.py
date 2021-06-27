import collections
import functools


# Class that defines an agency
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

  # Return the routes that are part of this agency
  def get_routes_with_agency(self):
    return filter(lambda route: route.agency == self, self.feed.get_routes())

  # Return the trips that are part of this agency
  def get_trips_with_agency(self):
    return filter(lambda trip: trip.agency == self, self.feed.get_trips())

  # Return if this agency equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this agency is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.name, self.id) == (other.name, other.id)

  # Return the hash for this agency
  def __hash__(self):
    return hash((self.id))

  # Return the internal representation for this agency
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

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
