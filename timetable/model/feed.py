# Class that defines a transit feed
class Feed:
  # Constructor
  def __init__(self, **kwargs):
    self.agencies = {}
    self.nodes = {}
    self.modalities = {}
    self.routes = {}
    self.trips = {}
    self.transfers = {}

    # Add optional properties
    self.id = kwargs.get('id')  # Defaults to None
    self.name = kwargs.get('name')  # Defaults to None
    self.author = kwargs.get('author')  # Defaults to None

  # Return all agencies
  def get_agencies(self):
    return list(self.agencies.values())

  # Return an agency with the specified id
  def get_agency(self, id):
    try:
      return self.agencies[id]
    except KeyError:
      raise ValueError(f"Undefined agency with id {id!r}")

  # Return all nodes
  def get_nodes(self):
    return self.nodes.values()

  # Return a node with the specified id
  def get_node(self, id):
    try:
      return self.nodes[id]
    except KeyError:
      raise ValueError(f"Undefined node with id {id!r}")

  # Return a node with the specified name, or a default value if no such node exists
  def get_node_by_name(self, name, default = None):
    return next(filter(lambda node: node.name == name, self.get_nodes()), default)

  # Return all transfers
  def get_transfers(self):
    return self.transfers.values()

  # Return a transfer with the specified id
  def get_transfer(self, id):
    try:
      return self.transfers.get[id]
    except KeyError:
      raise ValueError(f"Undefined transfer with id {id!r}")

  # Return all modalities
  def get_modalities(self):
    return self.modalities.values()

  # Return a modality with the specified id
  def get_modality(self, id):
    try:
      return self.modalities[id]
    except KeyError:
      raise ValueError(f"Undefined modality with id {id!r}")

  # Add a modalitiy with the specified id and data and return it
  def add_modality(self, id, **kwargs):
    if id in self.modalities:
      raise ValueError(f"Duplicate modalitiy id {id!r}")

    modality = Modality(self, id, **kwargs)
    self.modalities[id] = modality
    return modality

  # Return all routes
  def get_routes(self):
    return self.routes.values()

  # Return a route with the specified id
  def get_route(self, id):
    try:
      return self.routes[id]
    except KeyError:
      raise ValueError(f"Undefined route with id {id!r}")

  # Return all trips
  def get_trips(self):
    return self.trips.values()

  # Return a trip with the specified id
  def get_trip(self, id):
    try:
      return self.trips.get[id]
    except KeyError:
      raise ValueError(f"Undefined trip with id {id!r}")
