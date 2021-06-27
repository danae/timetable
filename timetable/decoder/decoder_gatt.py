import toml

from .decoder import FeedDecoder, FeedDecoderError
from ..model import Feed, Agency, Node, NodeType, Modality, ModalityType, Route, Trip, Transfer, StopList, Stop, Time


# Class that defines a feed decoder for GATT feeds
class GATTFeedDecoder(FeedDecoder):
  # Decode a feed from a file
  def decode(self, file):
    # Parse the TOML file
    try:
      data = toml.load(file)
    except toml.TomlDecodeError as err:
      raise FeedDecoderError(err)

    # Create a new feed
    feed = Feed(id = data.get('feed_id'), name = data.get('feed_name'), author = data.get('feed_author'))

    # Load the agencies
    for id, agency_data in data.get('agencies', {}).items():
      agency = self.load_agency(feed, id, agency_data)
      feed.agencies[agency.id] = agency

    # Load the nodes
    for id, node_data in data.get('nodes', {}).items():
      node = self.load_node(feed, id, node_data)
      feed.nodes[node.id] = node

    # Load the modalities
    for id, modality_data in data.get('modalities', {}).items():
      modality = self.load_modality(feed, id, modality_data)
      feed.modalities[modality.id] = modality

    # Load the routes
    for id, route_data in data.get('routes', {}).items():
      route = self.load_route(feed, id, route_data)
      feed.routes[route.id] = route

    # Load the trips
    for id, trip_data in data.get('trips', {}).items():
      trip = self.load_trip(feed, id, trip_data)
      feed.trips[trip.id] = trip

    # Load the transfers
    for id, transfer_data in data.get('transfers', {}).items():
      transfer = self.load_transfer(feed, id, transfer_data)
      feed.transfers[transfer.id] = transfer

    # Return the feed
    return feed

  # Load an agency
  @classmethod
  def load_agency(cls, feed, id, data):
    try:
      # Return a new agency based on the data
      return Agency(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in agency {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in agency {id!r}")

  # Load a node
  @classmethod
  def load_node(cls, feed, id, data):
    try:
      # Parse optional properties
      if 'type' in data:
        data['type'] = NodeType[data['type']]

      # Return a new node based on the data
      return Node(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in node {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in node {id!r}")

  # Load a modality
  @classmethod
  def load_modality(cls, feed, id, data):
    try:
      # Parse optional properties
      if 'type' in data:
        data['type'] = ModalityType[data['type']]

      # Return a new modality based on the data
      return Modality(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in modality {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in modality {id!r}")

  # Load a route
  @classmethod
  def load_route(cls, feed, id, data):
    try:
      # Parse required properties
      data['agency'] = feed.get_agency(data['agency'])
      data['modality'] = feed.get_modality(data['modality'])

      # Parse the stops
      data['stops'] = cls.load_route_stops(feed, id, data['stops'])

      # Return a new route based on the data
      return Route(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in route {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in route {id!r}")

  # Load a trip
  @classmethod
  def load_trip(cls, feed, id, data):
    try:
      # Parse required properties
      data['route'] = feed.get_route(data['route'])
      data['time'] = Time.fromstring(data['time'])

      # Parse optional properties
      if 'begin_at' in data:
        data['begin_at'] = feed.get_node(data['begin_at'])
      if 'end_at' in data:
        data['end_at'] = feed.get_node(data['end_at'])
      if 'agency' in data:
        data['agency'] = feed.get_agency(data['agency'])
      if 'modality' in data:
        data['modality'] = feed.get_modality(data['modality'])

      # Parse the stops
      data['stops'] = cls.load_trip_stops(feed, data['route'], data['time'], data.get('begin_at'), data.get('end_at'))

      # Return a new trip based on the data
      return Trip(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in trip {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in trip {id!r}")

  # Load a transfer
  @classmethod
  def load_transfer(cls, feed, id, data):
    try:
      # Parse required properties
      data['begin'] = feed.get_node(data['begin'])
      data['end'] = feed.get_node(data['end'])
      data['duration'] = Time.fromstring(data['duration'])

      # Return a new transfer based on the data
      return Transfer(feed, id, **data)
    except KeyError as err:
      raise FeedDecoderError(f"Missing keyword argument {err} in transfer {id!r}")
    except ValueError as err:
      raise FeedDecoderError(f"{err} in transfer {id!r}")

  # Load a stop list for a route
  @classmethod
  def load_route_stops(cls, feed, route_id, data):
    # Create a new stop list
    stops = StopList(feed)

    # Iterate over the data
    for stop_sequence, stop_data in data.items():
      try:
        # Parse required properties
        stop_data['node'] = feed.get_node(stop_data['node'])

        # Parse optional properties
        if 'a' in stop_data:
          stop_data['a'] = Time.fromstring(stop_data['a'])
        if 'd' in stop_data:
          stop_data['d'] = Time.fromstring(stop_data['d'])

        # Create a new stop
        stop = Stop(feed, stops, stop_sequence, **stop_data)

        # Add the stop to the list
        stops.stops.append(stop)
      except KeyError as err:
        raise FeedDecoderError(f"Missing keyword argument {err} in route {route_id!r}, stop with sequence {stop_sequence!r}")
      except ValueError as err:
        raise FeedDecoderError(f"{err} in route {route_id!r}, stop with sequence {stop_sequence!r}")

    # Return the stop list
    return stops

  # Load a stop list for a trip
  @classmethod
  def load_trip_stops(cls, feed, route, time, begin_at, end_at):
    # Create a new stop list
    stops = StopList(feed)

    # Iterate over the stops in the route
    for stop in route.stops:
      # Create new arrival and departure times
      a = stop.arrival + time if stop.arrival else None
      d = stop.departure + time if stop.departure else None

      # Create a new trip stop
      trip_stop = Stop(feed, stops, stop.sequence, node = stop.node, platform = stop.platform, a = a, d = d, skip = stop.skip)

      # Add the stop to the list
      stops.stops.append(trip_stop)

    # Apply the begin and end stops
    if begin_at is not None or end_at is not None:
      if begin_at is not None:
        stops = stops.beginning_at_node(begin_at)
      if end_at is not None:
        stops = stops.ending_at_node(end_at)

      if len(stops) > 1:
        stops.stops[0].arrival = None
      if len(stops) > 0:
        stops.stops[-1].departure = None

    # Return the stop list
    return stops
