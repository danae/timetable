# Query a list of elements
def query(elements, query, *attributes):
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
