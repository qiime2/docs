$(document).ready(function() {

  $.getJSON('//127.0.0.1:8000/_static/versions.json', function (data) {

    var currentVersion = window.location.pathname.split('/')[1];
    $.each(data, function(key, data) {
      $($('<li/>', {
        "html": $('<a/>', {
          "href": "/" + key + "/" + window.location.pathname.split('/').slice(2).join('/'),
          "text": data.name
        })
      })).appendTo('#version-list');

      if (key === currentVersion) {
        $('#version-div button').html('Version: ' + data.name + ' <span class="caret"></span>');
        if (data.deprecated) {
          $('<div/>', {
            "text": "This document is for an insecure version of QIIME 2 that is no longer supported. Please upgrade to a newer release!",
            "class": "alert alert-warning text-center",
          }).prependTo($('#content'))
        }
      }

    });

  });

});
