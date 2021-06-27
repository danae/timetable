import math

from .journey import Journey, JourneyTripLeg, JourneyTransferLeg
from ..model import Trip, Transfer


# Class that executes the RAPTOR algorithm on a transit feed
# Adapted from https://www.microsoft.com/en-us/research/wp-content/uploads/2012/01/raptor_alenex.pdf
class RaptorAlgorithm:
  # Constructor
  def __init__(self, feed):
    self.feed = feed

  # Return all possible connections at the specified departure node and time
  def scan(self, departure_node, departure_time):
    # k_arrivals[i][node] denotes the earliest known arrival time at node with up to i trips
    k_arrivals = {}
    k_arrivals[0] = dict.fromkeys(self.feed.get_nodes(), math.inf)
    k_arrivals[0][departure_node] = departure_time

    # best_arrivals[node] denotes the earliest known arrival time at node regardless of which trip
    best_arrivals = dict.fromkeys(self.feed.get_nodes(), math.inf)
    best_arrivals[departure_node] = departure_time

    # k_connections[node][i] denotes the connection from departure_node to node at the i-th trip
    k_connections = {}

    # marked_nodes denotes a set of nodes for which the arrival time is improved at the previous round
    marked_nodes = {departure_node}

    # Iterate over the rounds while there are nodes marked
    k = 0
    while marked_nodes:
      k += 1
      k_arrivals[k] = dict.fromkeys(self.feed.get_nodes(), math.inf)

      # First stage: accumulate routes serving marked stops from previous rounds
      queue = {}
      while marked_nodes:
        node = marked_nodes.pop()
        for route in node.get_routes_with_node():
          if route not in queue or self.is_node_before(route, node, queue[route]):
            queue[route] = node

      # Second stage: examine the routes
      for route, route_node in queue.items():
        trip = None
        start_node = None

        # Iterate over the stops in the route starting at route_node
        for stop in route.stops.beginning_at_node(route_node):
          # Can the arrival time be improved in this round?
          if trip is not None:
            arrival_at_node = trip.stops.get_arrival_at_node(stop.node)

            # Improve the arrival time if it's smaller than the current best
            if arrival_at_node < best_arrivals[stop.node]:
              k_arrivals[k][stop.node] = best_arrivals[stop.node] = arrival_at_node
              if stop.node not in k_connections:
                k_connections[stop.node] = {}
              k_connections[stop.node][k] = trip.beginning_at_node(start_node).ending_at_node(stop.node)
              marked_nodes.add(stop.node)

          # Can we catch an earlier trip at the node?
          if trip is None or ((departure_at_node := trip.stops.get_departure_at_node(stop.node)) is not None and k_arrivals[k - 1][stop.node] <= departure_at_node):
            trip = self.earliest_trip(route, stop.node, k_arrivals[k - 1][stop.node])
            start_node = stop.node

      # Third stage: examine the transfers
      for node in marked_nodes:
        # Iterate over the transfers from the node
        for transfer in node.get_transfers_with_node():
          transfer_node = transfer.end
          transfer_arrival = k_arrivals[k - 1][transfer_node] + transfer.time

          # Can the arrival time be improved in this round?
          if transfer_arrival < k_arrivals[k][transfer_node]:
            k_arrivals[k][transfer_node] = transfer_arrival
            if transfer_node not in k_connections:
              k_connections[transfer_node] = {}
            k_connections[transfer_node][k] = transfer
            marked_nodes.add(transfer_node)

    # Return the connections
    return k_connections

  # Return if a node is before another node in a route
  def is_node_before(self, route, node1, node2):
    index1 = route.stops.get_stop_index_at_node(node1)
    index2 = route.stops.get_stop_index_at_node(node2)
    return index1 < index2

  # Return the earliest possible trip of a route at the specified departure node and time
  def earliest_trip(self, route, departure_node, departure_time):
    earliest_trip = None
    for trip in route.get_trips_with_route():
      departure_at_node = trip.stops.get_departure_at_node(departure_node)
      if departure_at_node is not None and departure_at_node >= departure_time:
        if earliest_trip is None or departure_at_node < earliest_trip.stops.get_departure_at_node(departure_node):
          earliest_trip = trip
    return earliest_trip

  # Return journeys between two nodes that depart after the specified departure time
  def query_depart_after(self, departure_node, arrival_node, departure):
    # Get all connections
    k_connections = self.scan(departure_node, departure)

    # Create a list of journeys
    journeys = []

    # Iterate over the connections from departure_node to arrival_node
    for k in k_connections[arrival_node]:
      # Create a list of legs
      legs = []

      # Set the destination node for this round
      to_node = arrival_node

      # Iterate over the connections
      while k > 0:
        # Get the connection at the k-th trip
        k_connection = k_connections[to_node][k]

        # Append a new leg
        if isinstance(k_connection, Trip):
          from_node = k_connection.departure.node
          legs.insert(0, JourneyTripLeg(from_node, to_node, k_connection))
          to_node = from_node
        elif isinstance(k_connection, Transfer):
          from_node = k_connection.start
          legs.insert(0, JourneyTransferLeg(from_node, to_node, k_connection))
          to_node = from_node

        # Decrease the trip
        k -= 1

      # Append a new journey
      journeys.append(Journey(departure_node, arrival_node, legs))

    # Return the journeys
    return journeys
