import collections
import enum
import functools


# Class that defines a modality
# Modalities are sorted based on their priorities, names and types
@functools.total_ordering
class Modality:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.name = kwargs['name']

    # Add optional properties
    self.abbr = kwargs.get('abbr')  # Defaults to None
    self.type = kwargs.get('type', ModalityType.rail)  # Defaults to ModalityType.rail
    self.priority = kwargs.get('priority', 0)  # Defaults to 0
    self.color_text = kwargs.get('color_text', 'inherit')  # Defaults to 'inherit'
    self.color_bg = kwargs.get('color_bg', 'inherit')  # Defaults to 'inherit'

  # Return the routes that are part of this modality
  def get_routes_with_modality(self):
    return filter(lambda route: route.modality == self, self.feed.get_routes())

  # Return the trips that are part of this modality
  def get_trips_with_modality(self):
    return filter(lambda trip: trip.modality == self, self.feed.get_trips())

  # Return if this modality equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this modality is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.priority, self.name, self.type, self.id) < (other.priority, other.name, other.type, other.id)

  # Return the hash for this modality
  def __hash__(self):
    return hash((self.id))

  # Return the internal representation for this modality
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this modality
  def __str__(self):
    return self.name

  # Return the JSON representation for this modality
  def to_json(self):
    return collections.OrderedDict(
      id = self.id,
      name = self.name,
      abbr = self.abbr,
      type = self.type.name,
      priority = self.priority,
      color_text = self.color_text,
      color_bg = self.color_bg,
    )


# Enum that defines the type of a modality
class ModalityType(enum.Enum):
  tram = 0  # Any light rail or street level system within a metropolitan area.
  subway = 1  # Any underground rail system within a metropolitan area.
  rail = 2  # Used for intercity or long-distance travel.
  bus = 3  # Used for short- and long-distance bus routes.
  ferry = 4  # Used for short- and long-distance boat service.
  cable_tram = 5  # Used for street-level rail cars where the cable runs beneath the vehicle, e.g., cable car in San Francisco.
  aerial_lift = 6  # Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.
  funicular = 7  # Any rail system designed for steep inclines.
  trolleybus = 11  # Electric buses that draw power from overhead wires using poles.
  monorail = 12  # Railway in which the track consists of a single rail or a beam.
