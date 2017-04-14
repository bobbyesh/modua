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
      $('div.definition').hide();

      var definition = $(selector);
      definition.css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
      definition.show();
    });

});

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
    if (!element.hasClass(targetClass)) {
      element.removeClass('ease-0');
      element.removeClass('ease-1');
      element.removeClass('ease-2');
      element.removeClass('ease-3');

      var old_ease = $(selector).attr('data-ease');
      element.addClass(targetClass);

      // The old easiness needs to drop because the user changed the easines of this word
      var old_counter = $('#counter-' + old_ease);
      var old_count = old_counter.html();
      old_count = parseInt(old_count);
      old_count--;
      old_counter.html(old_count.toString());

      // The user set a new easiness for this word, so update the new ease's counter
      var new_counter = $('#counter-' + new_ease);
      var new_count = new_counter.html();
      new_count = parseInt(new_count);
      new_count++;
      new_counter.html(new_count.toString());

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

      request.done(function(msg) {
        console.log('done saving word', msg)
      });

      request.fail(function(error) {
        console.log('failed to save word', error)
      })
    }

    $('div.definition').hide();
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
            console.log(response);
        }).fail(function(error) {
            var $elem = '<li>' + 'Server error, could not save definition' + '</li>';
            ancestor.before($elem);
            console.log(error);
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
            type: 'DELETE',
        }).done(function(response) {
            parent.remove();
            console.log(parent);
        }).fail(function(error) {
            console.log('delete failed', error);
        }).then(function() {
            console.log('then');
        }).always(function() {
            console.log('always');
        });
    });
});
