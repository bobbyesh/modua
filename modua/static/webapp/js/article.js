const NEW = 0;
const HARD = 1;
const EASY = 2;
const KNOWN = 3;


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// Clicking on a word opens up the definition popup
$(document).ready(function() {
    const moveLeft = 20;
    const moveDown = 10;
    $('span.entry').click(function(e){
      var name = $(this).attr('name');
      var selector = 'div.definition[data-word="' + name + '"]';

      // Close all definitions because we only want one open at a time
      $('div.definition').hide();

      var definition = $(selector);
      console.log(selector);
      definition.css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
      definition.show();
    });
});


function updateCounts() {
    var ease = [
        $('[data-ease=0]').length,
        $('[data-ease=1]').length,
        $('[data-ease=2]').length,
        $('[data-ease=3]').length
    ];

    $('#counter-0').html(ease[0]);
    $('#counter-1').html(ease[1]);
    $('#counter-2').html(ease[2]);
    $('#counter-3').html(ease[3]);
    $('#total-count').html(ease[0] + ease[1] + ease[2] + ease[3]);
}

$(document).ready(updateCounts());


// Clicking on an 'ease' button changes the ease rating for the word
$(document).ready(function() {
  var csrftoken = getCookie('csrftoken');
  $('button.easy-button').on('click', function() {
      var id = $(this).attr('id');
      var new_ease = parseInt(id[id.length - 1]);
      var targetClass = 'ease-' + new_ease;
      var word = $(this).parent().attr('data-word');
      var selector = 'span.entry[name="' + word + '"]';
      var element = $(selector);
      // We check if the class isn't already the selected ease-# because we can avoid an ajax call
      if (!element.hasClass(targetClass)) {
          element.removeClass('ease-0');
          element.removeClass('ease-1');
          element.removeClass('ease-2');
          element.removeClass('ease-3');
          element.addClass(targetClass);
          $(selector).attr('data-ease', new_ease);
          // Make ajax to update DB
          var url = window.location.origin + '/api/user/words/' + word + '/';
          var request = $.ajax({
              url: url,
              data: {
                ease: new_ease
              },
              method: 'PATCH',
              dataType: 'json'
          });
        }

        $('div.definition').hide();
        updateCounts();
  });
});

$(document).ready(function() {
    $('.POST-definition-submit').click(function(e) {
        e.preventDefault();
        var definition = $(this).siblings('.POST-definition-text').val();
        var word = $(this).siblings('.POST-definition-text').attr('data-word');
        var pinyin = $(this).siblings('.POST-definition-text').attr('data-pinyin');
        var data = {
            definition: definition,
            pinyin: pinyin,
            word: word
        };
        var url = window.location.origin + '/api/user/definitions/';
        var ancestor = $('#POST-definition-form-' + word).parent();
        var request = $.ajax({
            url: url,
            data: data,
            method: 'POST',
            dataType: 'json'
        }).done(function(response) {
            var id = response.id.toString();
            // TODO: Research template literals and browser compatability to do away with
            //       ugly concatenations, if supported.
            var $elem = $('<li ' + 'data-id="' + id + '"' + '>' +
                            definition +
                           '<button class="glyphicon glyphicon-remove remove"></button>' +
                        '</li>');
            ancestor.before($elem);
        }).fail(function(error) {
            var $elem = '<li>' + 'Server error, could not save definition' + '</li>';
            ancestor.before($elem);
        });
    })
});

$(document).ready(function() {
    $(document).on('click', '.remove', function(e) {
        e.preventDefault();
        var parent = $(this).parent();
        var id = parent.attr('data-id');
        var url = window.location.origin + '/api/user/definitions/' + id + '/';
        var request = $.ajax({
            url: url,
            type: 'DELETE'
        }).done(function(response) {
            parent.remove();
        });
    });
});


$(document).ready(function() {
    $('#button-all-known').on('click', function(e) {
        e.preventDefault();
        $('.entry')
            .removeClass('ease-0')
            .removeClass('ease-1')
            .removeClass('ease-2')
            .addClass('ease-3')
            .attr('data-ease', KNOWN)
            .each(function(idx, word) {
                var text = $(word).text();
                var url = window.location.origin + '/api/user/words/' + text + '/';
                if (validator.isURL(url)) {
                    var request = $.ajax({
                        url: url,
                        data: {
                            ease: KNOWN
                        },
                        method: 'PATCH',
                        dataType: 'json'
                    }).fail(function(error) {
                        console.log('Ease not saved, error:', error);
                    });
                }
            });
        updateCounts();
    });
});
