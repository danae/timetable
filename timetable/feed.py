from .model import Agency, Station, TrainType, TrainSeries, Train


# Class that defines a timetable feed
class Feed:
  # Constructor
  def __init__(self):
    self.agencies = {}
    self.stations = {}
    self.train_types = {}
    self.train_series = {}
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

  # Register a station
  def register_station(self, id, **kwargs):
    if id in self.stations:
      raise ValueError(f"Duplicate station id {id!r}")

    station = Station(self, id, **kwargs)
    self.stations[id] = station

  # Unregister a station
  def unregister_station(self, id):
    if id in self.stations:
      del self.stations[id]

  # Get a station with the specified id
  def get_station(self, id):
    return self.stations[id]

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

  # Register a train series
  def register_train_series(self, id, **kwargs):
    if id in self.train_series:
      raise ValueError(f"Duplicate train series id {id!r}")

    train_series = TrainSeries(self, id, **kwargs)
    self.train_series[id] = train_series

  # Unregister a train series
  def unregister_train_series(self, id):
    if id in self.train_series:
      del self.train_series[id]

  # Get a train series with the specified id
  def get_train_series(self, id):
    return self.train_series[id]

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

  # Print information about this feed
  def report(self):
    buffer = f"Feed {self.name} by {self.author} contains {len(self.trains)} trains"
    for train in sorted(self.trains.values()):
      buffer += f"\n\n{train.report()}"
    return buffer
