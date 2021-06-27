# Class that defines a journey
class Journey:
  # Constructor
  def __init__(self, from_node, to_node, legs):
    self.from_node = from_node
    self.to_node = to_node
    self.legs = legs

  # Get the departure time of this journey
  @property
  def departure_time(self):
    return self.legs[0].departure_time

  # Get the arrival time of this journey
  @property
  def arrival_time(self):
    return self.legs[-1].arrival_time

  # Get the duration of this journey
  @property
  def duration(self):
    return self.arrival_time - self.departure_time

  # Get the number of transfers in this journey
  @property
  def transfers(self):
    return len(self.legs) - 1

  # Return the string representation of this journey
  def __str__(self):
    buffer = f"Journey from {self.from_node} to {self.to_node}"
    buffer += f"\n  Duration: {self.duration:%H:%M}"
    buffer += f"\n  Transfers: {self.transfers}"

    last_leg = None
    for leg in self.legs:
      if last_leg is None:
        last_leg = leg
      else:
        buffer += f"\n\n{leg.departure_time - last_leg.arrival_time:%H:%M} transfer time"
      buffer += f"\n\n{leg}"
    return buffer


# Class that defines a journey leg that encapsulates a trip
class JourneyTripLeg:
  # Constructor
  def __init__(self, from_node, to_node, trip):
    self.from_node = from_node
    self.to_node = to_node
    self.trip = trip

  # Get the departure time of this leg
  @property
  def departure_time(self):
    return self.trip.departure_time

  # Get the arrival time of this leg
  @property
  def arrival_time(self):
    return self.trip.arrival_time

  # Get the duration of this leg
  @property
  def duration(self):
    return self.trip.duration

  # Return the string representation of this leg
  def __str__(self):
    buffer = f"{self.trip} ({self.duration:%H:%M})"
    for i, stop in enumerate(self.trip.stops):
      if i == 0:
        buffer += f"\n  {stop.departure:%H:%M} D  {stop.node}"
      else:
        buffer += f"\n  {stop.arrival:%H:%M}    {stop.node}"
      buffer += f" (platform {stop.platform})" if stop.platform is not None else ""
    return buffer


# Class that defines a journey leg that encapsulates a transfer
class JourneyTransferLeg:
  # Constructor
  def __init__(self, from_node, to_node, transfer):
    self.from_node = from_node
    self.to_node = to_node
    self.transfer = transfer

  # Get the duration of this leg
  @property
  def duration(self):
    return self.transfer.duration

  # Return the string representation of this leg
  def __str__(self):
    return f"{self.transfer} ({self.duration:%H:%M})"
