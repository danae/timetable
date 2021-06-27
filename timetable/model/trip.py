import collections
import copy
import functools


# Class that defines a trip
# Trips sort chronologically based on their canonical times and numbers
@functools.total_ordering
class Trip:
  # Constructor
  def __init__(self, feed, id, **kwargs):
    self.feed = feed
    self.id = id

    # Add required properties
    self.route = kwargs['route']
    self.stops = kwargs['stops']

    # Add optional properties
    self.agency = kwargs.get('agency', self.route.agency)  # Defaults to agency of the route
    self.modality = kwargs.get('modality', self.route.modality)  # Defaults to modality of the route
    self.name = kwargs.get('name', self.route.name)  # Defaults to name of the route
    self.abbr = kwargs.get('abbr', self.route.abbr)  # Defaults to abbr of the route
    self.number = kwargs.get('number', self.route.number)  # Defaults to number of the route
    self.priority = kwargs.get('priority', self.route.priority)  # Defaults to priority of the route
    self.remarks = kwargs.get('remarks', self.route.remarks)  # Defaults to remarks of the route
    self.services = kwargs.get('services', self.route.services)  # Defaults to services of the route
    self.color_text = kwargs.get('color_text', self.route.color_text)  # Defaults to color_text of the route
    self.color_bg = kwargs.get('color_bg', self.route.color_bg)  # Defaults to color_bg of the route

  # Return the nodes that this trip stops at or passes through
  def get_nodes(self, skips = False):
    return self.stops.get_nodes(skips)

  # Return the departure point of this trip
  @property
  def departure(self):
    return self.stops.departure

  # Return the departure node of this trip
  @property
  def departure_node(self):
    return self.departure.node

  # Return the departure time of this trip
  @property
  def departure_time(self):
    return self.departure.departure

  # Return the arrival point of this trip
  @property
  def arrival(self):
    return self.stops.arrival

  # Return the arrival node of this trip
  @property
  def arrival_node(self):
    return self.arrival.node

  # Return the arrival time of this trip
  @property
  def arrival_time(self):
    return self.arrival.arrival

  # Return the canonical time of this trip
  @property
  def canonical_time(self):
    return self.departure_time or self.arrival_time

  # Return the duration of this trip
  @property
  def duration(self):
    return self.arrival_time - self.departure_time

  # Return the nodes of this trip
  @property
  def nodes(self):
    return [stop.node for stop in self.stops]

  # Return the trip beginning at the specified node
  def beginning_at_node(self, node):
    trip = copy.copy(self)
    trip.stops = trip.stops.beginning_at_node(node)
    return trip

  # Return the trip starting at the specified node
  def ending_at_node(self, node):
    trip = copy.copy(self)
    trip.stops = trip.stops.ending_at_node(node)
    return trip

  # Return if this trip equals another object
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.id == other.id

  # Return if this trip is less than another object
  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return NotImplemented
    return (self.canonical_time, self.number, self.id) < (other.canonical_time, other.number, other.id)

  # Return the hash for this trip
  def __hash__(self):
    return hash((self.id))

  # Return the internal representation for this trip
  def __repr__(self):
    return f"<{self.__class__.__name__} {self.id!r}>"

  # Return the string representation for this trip
  def __str__(self):
    return self.name

  # Return the JSON representation for this trip
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
