/**
 * Created by Bobby Eshleman on 8/10/2016.
 *
 * This script gives definition popup functionality.
 *
 * The following html will yield a popup for the word in the <span> element, displaying
 * the definition in the <div id="pop-up"> element.
 *
 * The hovering functionality requires that the data-pk attribute values are equivalent.
 *
 * Example:
 * <body>
 *     I was in the neighborhood and just wanted to say <span id="trigger" data-pk="1">hello</span>!
 *
 *     <div id="pop-up" data-pk="1">
 *          <h3>hello</h3>
 *              <p>
 *                  A wonderful greeting used by all across the land.
 *              </p>
 *      </div>
 * </body>
 *
 *
 *   Based off of code found at: http://creativeindividual.co.uk/2011/02/create-a-pop-up-div-in-jquery/
 */

var get_popup_elem = function(that) {
    var pk = $(that).attr("data-pk");
    var elem_name = 'div#pop-up[data-pk="' + pk + '"]'
    console.log(elem_name);
    return $(elem_name);
};

$(function() {
    var moveLeft = 20;
    var moveDown = 10;

    $('span#trigger').hover(function(e) {
        var elem = get_popup_elem(this);
        elem.show();
    }, function() {
        var elem = get_popup_elem(this);
        elem.hide();
    });

    $('span#trigger').mousemove(function(e) {
        var elem = get_popup_elem(this);
        elem.css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
    });

});
