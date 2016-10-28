// Open external links (http, https) in a new tab/window. Taken from:
//     https://github.com/sphinx-doc/sphinx/issues/1634
$(document).ready(function() {
    $("a[href^='http']").attr('target','_blank');
});
