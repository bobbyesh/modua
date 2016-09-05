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
 *     I was in the neighborhood and just wanted to say <span class="token easy" name="hello">hello</span>!
 *
 *     <div class="definition" data-token="hello">
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
    var name = $(that).attr("name");
    var elem_name = 'div.definition[data-token="' + name + '"]'
    return $(elem_name);
};


$(document).ready(function() {
    const moveLeft = 20;
    const moveDown = 10;

    $('span.token').click(function(e){
	    $('div.definition').hide();
            var elem = get_popup_elem(this);
            elem.css('top', e.pageY + moveDown).css('left', e.pageX + moveLeft);
            elem.show();
    });
    
    $('button.ease').on('click', function() {
	    $('div.definition').hide();
    });


});


