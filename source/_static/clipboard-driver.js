// Grab all elements with highlight-shell class - these will contain all shell commands
var highlightShellElements = document.getElementsByClassName("highlight-shell");

// Loop through elements with highlight-shell class and add clipboard button to each block
for (x = 0; x < highlightShellElements.length; x++)
{
  // Create button element
  var clipboardButton = document.createElement("button");

  // Create span element and add glyphicon glyphicon-copy classes to span element
  // Append span element as child of clipboard button
  // Add clipboard-btn class to the clipboard button element
  // Add alt and title attribute to the clipboard button
  var spanElement = document.createElement("span");
  spanElement.setAttribute("class", "glyphicon glyphicon-copy");
  spanElement.innerHTML = "";
  clipboardButton.appendChild(spanElement);
  clipboardButton.setAttribute("class", "btn btn-default clipboard-btn");
  clipboardButton.setAttribute("title", "Click to copy the command block below");

  // Grab pre element
  var preElements = highlightShellElements[x].getElementsByTagName("pre");

  // Add the data-clipboard-text atribute to the clipboard button
  // Assign the pre elements text content to the data-clipboard-text attribute
  clipboardButton.setAttribute("data-clipboard-text", $.trim(preElements[0].textContent));

  // Get the command block root "div" element
  // insert the clipboardButton node as the first child of the command block root
  var commandBlockRoot = preElements[0].parentElement.parentElement;
  commandBlockRoot.insertBefore(clipboardButton, commandBlockRoot.firstChild);
}

// Initialize the clipboard button framework
new Clipboard('.clipboard-btn');
