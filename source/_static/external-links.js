// Open external links (http, https) in a new tab/window. Taken from:
//     https://github.com/sphinx-doc/sphinx/issues/1634
// Note: When using target, consider adding rel="noopener noreferrer" to avoid
// exploitation of the window.opener API.
//    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a#attr-target
$(document).ready(function() {
    $("a[href^='http']")
      .attr('target','_blank')
      .attr('rel', 'noopener noreferrer');
});
