import collections
import functools


# Class that defines a route
# Routes sort alphabetically based on their numbers
@functools.total_ordering
class Route:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.agency = kwargs['agency']
    self.modality = kwargs['modality']
    self.name = kwargs['name']
    self.stops = kwargs['stops']

    # Add optional properties
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.number = kwargs.get('number')  # Defaults to None
    self.remarks = kwargs.get('remarks', {})  # Defaults to {}
    self.services = kwargs.get('services', {})  # Defaults to {}
    self.priority = kwargs.get('priority', self.modality.priority)  # Defaults to priority of the modality
    self.color_text = kwargs.get('color_text', self.modality.color_text)  # Defaults to color_text of the modality
    self.color_bg = kwargs.get('color_bg', self.modality.color_bg)  # Defaults to color_bg of the modality

  # Return the trips that are part of this route
  def get_trips_with_route(self):
    return filter(lambda trip: trip.route == self, self.feed.get_trips())

  # Return the nodes that this route stops at or passes through
  def get_nodes(self, skips = False):
    return self.stops.get_nodes(skips)

  # Return if this route equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this route is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.number, self.id) < (other.number, other.id)

  # Return the hash for this route
  def __hash__(self):
    return hash((self.id))

  # Return the internal representation for this route
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this route
  def __str__(self):
    return self.name

  # Return the JSON representation for this route
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      agency = self.agency.to_json(),
      modality = self.modality.to_json(),
      name = self.name,
      abbr = self.abbr,
      number = self.number,
      remarks = self.remarks,
      services = self.services,
      priority = self.priority,
      color_text = self.color_text,
      color_bg = self.color_bg,
      stops = self.stops.to_json(),
    )
