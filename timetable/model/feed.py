from .agency import Agency
from .node import Node
from .train import Train
from .train_set import TrainSet
from .train_type import TrainType


# Class that defines a feed
class Feed:
  # Constructor
  def __init__(self):
    self.agencies = {}
    self.nodes = {}
    self.train_types = {}
    self.train_sets = {}
    self.trains = {}

  # Register an agency
  def register_agency(self, id, **kwargs):
    if id in self.agencies:
      raise ValueError(f"Duplicate agency id {id!r}")

    agency = Agency(self, id, **kwargs)
    self.agencies[id] = agency

  # Unregister an agency
  def unregister_agency(self, id):
    if agency_id in self.agencies:
      del self.agencies[id]

  # Get all agencies
  def get_agencies(self):
    return list(self.agencies.values())

  # Get an agency with the specified id
  def get_agency(self, id):
    return self.agencies[id]

  # Register a node
  def register_node(self, id, **kwargs):
    if id in self.nodes:
      raise ValueError(f"Duplicate node id {id!r}")

    node = Node(self, id, **kwargs)
    self.nodes[id] = node

  # Unregister a node
  def unregister_node(self, id):
    if id in self.nodes:
      del self.nodes[id]

  # Get all nodes
  def get_nodes(self):
    return self.nodes.values()

  # Get all nodes matching a query
  def query_nodes(self, query):
    return self.query(self.nodes.values(), query, 'name')

  # Get a node with the specified id
  def get_node(self, id):
    return self.nodes[id]

  # Get a node matching a query
  def query_node(self, query):
    try:
      return next(iter(self.query_nodes(query)))
    except StopIteration:
      raise KeyError(query)

  # Register a train type
  def register_train_type(self, id, **kwargs):
    if id in self.train_types:
      raise ValueError(f"Duplicate train type id {id!r}")

    train_type = TrainType(self, id, **kwargs)
    self.train_types[id] = train_type

  # Unregister a train type
  def unregister_train_type(self, id):
    if id in self.train_types:
      del self.train_types[id]

  # Get a train type with the specified id
  def get_train_type(self, id):
    return self.train_types[id]

  # Get all train types as a list
  def get_train_types(self):
    return list(self.train_types.values())

  # Register a train set
  def register_train_set(self, id, **kwargs):
    if id in self.train_sets:
      raise ValueError(f"Duplicate train set id {id!r}")

    train_set = TrainSet(self, id, **kwargs)
    self.train_sets[id] = train_set

  # Unregister a train set
  def unregister_train_set(self, id):
    if id in self.train_sets:
      del self.train_sets[id]

  # Get a train set with the specified id
  def get_train_set(self, id):
    return self.train_sets[id]

  # Get all train sets as a list
  def get_train_sets(self):
    return list(self.train_sets.values())

  # Register a train
  def register_train(self, id, **kwargs):
    if id in self.trains:
      raise ValueError(f"Duplicate train id {id!r}")

    train = Train(self, id, **kwargs)
    self.trains[id] = train

  # Unregister a train
  def unregister_train(self, id):
    if id in self.trains:
      del self.trains[train_id]

  # Get a train with the specified id
  def get_train(self, id):
    return self.trains[id]

  # Get all trains as a list
  def get_trains(self):
    return list(self.trains.values())

  # Query a list of elements
  def query(self, elements, query, *attributes):
    # Get the default attributes
    attributes = attributes or ['name']

    # Get the order of a value
    def order(value):
      if not isinstance(value, str):
        return -1
      return value.lower().find(query.lower())

    # Get the orders of an element
    def orders(element):
      for attribute in attributes:
        try:
          value = getattr(element, attribute)
          yield order(value)
        except AttributeError:
          yield -1

    # Create a list of matched elements
    matched = []
    for element in elements:
      element_orders = tuple(orders(element))
      if -1 in element_orders:
        continue
      matched.append((element_orders, element))

    # Sort the matched elements
    matched = sorted(matched)

    # Return the actual matched elements
    return [element for _, element in matched]

  # Return the internal representation for this feed
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.name!r}>"
