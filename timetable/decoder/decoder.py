# Class that defines a feed decoder
class FeedDecoder:
  # Decode a feed from a file
  def decode(self, file):
    raise NotImplementedError()


# Class that defines a feed decoder error
class FeedDecoderError(Exception):
  # Constructor
  def __init__(self, message):
    super().__init__(message)
