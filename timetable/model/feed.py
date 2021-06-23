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

  # Get an agency with the specified id
  def get_agency(self, id):
    return self.agencies[id]

  # Get all agencies as a list
  def get_agencies(self):
    return list(self.agencies.values())

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

  # Get a node with the specified id
  def get_node(self, id):
    return self.nodes[id]

  # Get all nodes as a list
  def get_nodes(self):
    return list(self.nodes.values())

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

  # Print information about this feed
  def report(self):
    buffer = f"Feed {self.name} by {self.author} contains {len(self.trains)} trains"
    for train in sorted(self.trains.values()):
      buffer += f"\n\n{train}\n{train.route}"
    return buffer

  # Return the internal representation for this feed
  def __repr__(self):
    return f"<{__name__}.{self.__class__.__name__} {self.name!r}>"
