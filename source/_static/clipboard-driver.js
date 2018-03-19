
//Grab all elements with highlight-shell class - these will contain all shell commands
var highlight_shell_elements = document.getElementsByClassName("highlight-shell");

//Loop through elements with highlight-shell class and add clipboard button to each block
for (x = 0; x < highlight_shell_elements.length; x++)
{
  //Create button element
  var clipboard_button = document.createElement("BUTTON");

  //Create span element and add glyphicon glyphicon-copy classes to span element
  //Append span element as child of clipboard button
  //Add clipboard-btn class to the clipboard button element
  var span_element = document.createElement("SPAN");
  span_element.setAttribute('class', 'glyphicon glyphicon-copy');
  span_element.innerHTML = "";
  clipboard_button.appendChild(span_element);
  clipboard_button.setAttribute('class', 'clipboard-btn');

  //Grab pre element
  var pre_elements = highlight_shell_elements[x].getElementsByTagName("pre");

  //Add the data-clipboard-text atribute to the clipboard button
  //Assign the pre elements text content to the data-clipboard-text attribute
  clipboard_button.setAttribute('data-clipboard-text', pre_elements[0].textContent);

  //Style the clipboard button
  //Display block
  //Float right if it is not a "wget" or "curl" block
  clipboard_button.style.display = "block";

  if (!(pre_elements[0].textContent.substring(0,4) == "wget"
       || pre_elements[0].textContent.substring(0,4) == "curl"))
       {
         clipboard_button.style.float = "right";
       }

  //Insert clipboard button as first child of pre element
  pre_elements[0].insertBefore(clipboard_button, pre_elements[0].firstChild);

}

//Initialize the clipboard button framwork
new Clipboard('.clipboard-btn');
