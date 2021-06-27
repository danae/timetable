// Fetch a URL
async function get(url, query)
{
  url = new URL(url);
  for (key in query)
    url.searchParams.append(key, query[key])

  let response = await fetch(url);
  let response_json = await response.json();
  return response_json;
}

// Create a dropdown with matching station names for an input
function stationInput(input, url)
{
  let inputElm = $(input);

  // Event handler for when the element is provided with input
  inputElm.on('focus input', function() {
    // Get the value
    let value = inputElm.val();

    // Get the dropdown
    let inputDropdownElm = inputElm.data('dropdown');

    // Check if the value is not empty
    if (value !== "")
    {
      // Create the dropdown content
      let inputDropdownMenuElm = undefined;
      let inputDropdownContentElm = undefined;

      // Create a dropdown if not present
      if (inputDropdownElm !== undefined)
      {
        inputDropdownMenuElm = inputDropdownElm.find('.dropdown-menu');
        inputDropdownContentElm = inputDropdownMenuElm.find('.dropdown-content');
      }
      else
      {
        inputDropdownElm = $('<div class="dropdown my-0">')
          .insertAfter(inputElm.parent())
          .hide();
        inputDropdownMenuElm = $('<div class="dropdown-menu">')
          .appendTo(inputDropdownElm);
        inputDropdownContentElm = $('<div class="dropdown-content">')
          .appendTo(inputDropdownMenuElm);

        inputElm.data('dropdown', inputDropdownElm);
      }

      // Function that defines an event handler when a dropdown item is clicked
      function dropdownItemClick()
      {
        let itemElm = $(this);
        let itemNode = itemElm.data('node');

        // Set the value of the input
        inputElm.val(itemNode.name);
      }

      // Get the nodes matching the value
      get(url, {q: value}).then(function(nodes)
      {
        // Clear the dropdown content
        inputDropdownContentElm.empty();

        // Add the nodes to the dropdown content
        for (let node of nodes)
        {
          let item = $('<a class="dropdown-item">')
            .data('node', node)
            .on('click', dropdownItemClick);

          if (node.node)
            item.html(`<b>${node.name}</b>`);
          else
            item.html(node.name);

          item.appendTo(inputDropdownContentElm);
        }

        // Activate the dropdown
        inputDropdownElm.show().addClass('is-active');
      });
    }
    else
    {
      // Hide the dropdown
      if (inputDropdownElm !== undefined)
        inputDropdownElm.removeClass('is-active').hide();
    }
  });

  // Event handler for when the element loses focus
  /*inputElm.on('blur', function() {
    // Get the dropdown
    let inputDropdownElm = inputElm.data('dropdown');

    // Hide the dropdown
    if (inputDropdownElm !== undefined)
      inputDropdownElm.removeClass('is-active').hide();
  });*/
}
