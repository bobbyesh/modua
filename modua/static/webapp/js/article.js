

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
    var word = $(this).parent().attr('data-word');
    var selector = 'span.entry[name="' + word + '"]';
    $(selector).removeClass('ease-0');
    $(selector).removeClass('ease-1');
    $(selector).removeClass('ease-2');
    $(selector).removeClass('ease-3');
    var old_ease = $(selector).attr('data-ease');
    var targetClass = 'ease-' + new_ease;
    console.log('targetclass', targetClass);
    $(selector).addClass(targetClass);

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

    $('div.definition').hide();

    // Make ajax to update DB

    console.log()
    var url = `http://127.0.0.1:8000/api/words/${word}/`
    console.log(url)
    var request = $.ajax({
      url: url,
      method: 'GET',
      dataType: 'json',
    });

    console.log('here')
    request.done(function(msg) {
      console.log(msg)
    })


    url = `http://127.0.0.1:8000/api/user/words/${word}/`
    console.log(url)
    request = $.ajax({
      url: url,
      method: 'GET',
      dataType: 'json',
    });

    console.log('here')
    request.done(function(msg) {
      console.log(msg)
    })


  });
})
