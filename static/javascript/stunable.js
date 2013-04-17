/* * Licensed under the MIT License (LICENSE.txt).
 *
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.

 * Version: 3.0.3-pre
 * 
 * Requires: 1.2.2+
 */

(function($) {

var types = ['DOMMouseScroll', 'mousewheel'];

$.event.special.mousewheel = {
    setup: function() {
        if ( this.addEventListener )
            for ( var i=types.length; i; )
                this.addEventListener( types[--i], handler, false );
        else
            this.onmousewheel = handler;
    },
    
    teardown: function() {
        if ( this.removeEventListener )
            for ( var i=types.length; i; )
                this.removeEventListener( types[--i], handler, false );
        else
            this.onmousewheel = null;
    }
};

$.fn.extend({
    mousewheel: function(fn) {
        return fn ? this.bind("mousewheel", fn) : this.trigger("mousewheel");
    },
    
    unmousewheel: function(fn) {
        return this.unbind("mousewheel", fn);
    }
});


function handler(event) {
    var args = [].slice.call( arguments, 1 ), delta = 0, returnValue = true;
    
    event = $.event.fix(event || window.event);
    event.type = "mousewheel";
    
    if ( event.wheelDelta ) delta = event.wheelDelta/120;
    if ( event.detail     ) delta = -event.detail/3;
    
    // Add event and delta to the front of the arguments
    args.unshift(event, delta);

    return $.event.handle.apply(this, args);
}

})(jQuery);




// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());



function remember( selector ){

    $(selector).each(

        function(){

            //if this item has been cookied, restore it

            var name = $(this).attr('name');

            if( $.cookie( name ) ){

                $(this).val( $.cookie(name) );

            }

            //assign a change function to the item to cookie it

            $(this).change(

                function(){

                    $.cookie(name, $(this).val(), { path: '/', expires: 365 });

                }

            );

        }

    );

}


function cart_item_added(){
    var SI  = setInterval(function(){
        $('#cart-button').toggleClass('drop_item_hover')
    },300)

    setTimeout(function(){
        window.clearInterval(SI);
    },1900)
}

function wishlist_item_added(){

    var SI  = setInterval(function(){

        $('#wish-button').toggleClass('drop_item_hover')
    },300)

    setTimeout(function(){
        window.clearInterval(SI);
    },1900)
}

$.fn.serializeObject = function()
    {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };

function changeError(target, message) {
    target.innerHTML = message;
}



$.fn.extend({
        pschecker: function (options) {
            var settings = $.extend({ minlength: 8, maxlength: 16, onPasswordValidate: null, onPasswordMatch: null }, options);
            return this.each(function () {
                var wrapper = $('.password-container');
                var password = $('.strong-password:eq(0)', wrapper);
                var cPassword = $('.strong-password:eq(1)', wrapper);

                cPassword.removeClass('no-match');
                password.keyup(validatePassword).blur(validatePassword).focus(validatePassword);
                cPassword.keyup(validatePassword).blur(validatePassword).focus(validatePassword);

                function validatePassword() {
                    var pstr = password.val().toString();
                    var meter = $('.meter');
                    meter.html("");
                    //fires password validate event if password meets the min length requirement
                    if (settings.onPasswordValidate != null)
                        settings.onPasswordValidate(pstr.length >= settings.minlength);

                    if (pstr.length < settings.maxlength)
                        meter.removeClass('strong').removeClass('medium').removeClass('weak');
                    if (pstr.length > 0) {
                        var rx = new RegExp(/^(?=(.*[a-z]){1,})(?=(.*[\d]){1,})(?=(.*[\W]){1,})(?!.*\s).{7,30}$/);
                        if (rx.test(pstr)) {
                            meter.addClass('strong');
                            meter.html("Strong");
                        }
                        else {
                            var alpha = containsAlpha(pstr);
                            var number = containsNumeric(pstr);
                            var upper = containsUpperCase(pstr);
                            var special = containsSpecialCharacter(pstr);
                            var result = alpha + number + upper + special;

                            if (result > 2) {
                                meter.addClass('medium');
                                meter.html("Medium");
                            }
                            else {
                                meter.addClass('weak');
                                meter.html("weak");
                            }
                        }
                        if (cPassword.val().toString().length > 0) {
                            if (pstr == cPassword.val().toString()) {
                                cPassword.removeClass('no-match');
                                if (settings.onPasswordMatch != null)
                                    settings.onPasswordMatch(true);
                            }
                            else {
                                cPassword.addClass('no-match');
                                if (settings.onPasswordMatch != null)
                                    settings.onPasswordMatch(false);
                            }
                        }
                        else {
                            cPassword.addClass('no-match');
                            if (settings.onPasswordMatch != null)
                                settings.onPasswordMatch(false);
                        }
                    }
                }

                function containsAlpha(str) {
                    var rx = new RegExp(/[a-z]/);
                    if (rx.test(str)) return 1;
                    return 0;
                }

                function containsNumeric(str) {
                    var rx = new RegExp(/[0-9]/);
                    if (rx.test(str)) return 1;
                    return 0;
                }

                function containsUpperCase(str) {
                    var rx = new RegExp(/[A-Z]/);
                    if (rx.test(str)) return 1;
                    return 0;
                }
                function containsSpecialCharacter(str) {

                    var rx = new RegExp(/[\W]/);
                    if (rx.test(str)) return 1;
                    return 0;
                }


            });
        }
    });
(jQuery);


/*
  textfill
 @name      jquery.textfill.js
 @author    Russ Painter
 @author    Yu-Jie Lin
 @version   0.3.3
 @date      2013-03-26
 @copyright (c) 2012-2013 Yu-Jie Lin
 @copyright (c) 2009 Russ Painter
 @license   MIT License
 @homepage  https://github.com/jquery-textfill/jquery-textfill
 @example   http://jquery-textfill.github.com/jquery-textfill/Example.htm
*/
(function(g){g.fn.textfill=function(n){function l(c,a,e,h,f,j){function d(a,b){var c=" / ";a>b?c=" > ":a==b&&(c=" = ");return c}b.debug&&console.debug(c+"font: "+a.css("font-size")+", H: "+a.height()+d(a.height(),e)+e+", W: "+a.width()+d(a.width(),h)+h+", minFontPixels: "+f+", maxFontPixels: "+j)}function m(b,a,e,h,f,j,d,k){for(l(b+": ",a,f,j,d,k);d<k-1;){var g=Math.floor((d+k)/2);a.css("font-size",g);if(e.call(a)<=h){if(d=g,e.call(a)==h)break}else k=g;l(b+": ",a,f,j,d,k)}a.css("font-size",k);e.call(a)<=
h&&(d=k,l(b+"* ",a,f,j,d,k));return d}var b=jQuery.extend({debug:!1,maxFontPixels:40,minFontPixels:4,innerTag:"span",widthOnly:!1,callback:null,complete:null,explicitWidth:null,explicitHeight:null},n);this.each(function(){var c=g(b.innerTag+":visible:first",this),a=b.explicitHeight||g(this).height(),e=b.explicitWidth||g(this).width(),h=c.css("font-size");b.debug&&(console.log("Opts: ",b),console.log("Vars: maxHeight: "+a+", maxWidth: "+e));var f=b.minFontPixels,j=0>=b.maxFontPixels?a:b.maxFontPixels,
d=void 0;b.widthOnly||(d=m("H",c,g.fn.height,a,a,e,f,j));f=m("W",c,g.fn.width,e,a,e,f,j);b.widthOnly?c.css("font-size",f):c.css("font-size",Math.min(d,f));b.debug&&console.debug("Final: "+c.css("font-size"));(c.width()>e||c.height()>a)&&c.css("font-size",h);b.callback&&b.callback(this)});b.complete&&b.complete(this);return this}})(jQuery);
// CLEAR TEXT INPUTS OF DEFAULT VALUE ON FOCUS
function clearInput(textField) {
    if(textField.value == textField.defaultValue) {
        textField.value = "";
    }
}

// RESTORE TEXT INPUT DEFAULT VALUE ON BLUR
function restoreInput(textField) {
    if(textField.value == "" || isEmpty(textField.value)) {
        textField.value = textField.defaultValue;
    }
}

function isEmpty(tarString) {
    var blanks = /^\s*$/
    if(blanks.test(tarString)) {
        return true;
    }
    return false;
}

function isDefault(textField) {
    if(textField.value == textField.defaultValue) {
        return true;
    }
    return false;
}

var refclickFunctions = {
    'reload' : function(selection,data){
        window.location.reload();
    },
    'remove' : function(selection,data){
        if($(selection.data('target')).hasClass('isotope-item')){
            $('#container').isotope('remove', $(selection.data('target')))
            return false;
        }else{
            $(selection.data('target')).fadeOut('slow',function(){$(this).remove()})
        }
    },
    'remove_and_close' : function(selection,data){
        $(selection.data('target')).fadeOut('slow');
        $.modal.close();
    },
    'downvote': function(selection,data){
        $(selection.data('target')).removeClass('upvoted').addClass('downvoted')
    },
    'upvote': function(selection,data){
        $(selection.data('target')).removeClass('downvoted').addClass('upvoted')
    },
    'clearvote': function(selection,data){
        $(selection.data('target')).removeClass('downvoted').removeClass('upvoted')
    },
    'add_tab':function(selection,data){
        var el = $(data),
        t = $(selection.data('target'));
        t.append(el.hide().fadeIn().css('display','inline'))
        $(t).animate({scrollLeft:$(t).width()},400);
        window.location = el.find('a').attr('href')
        init_refclicks(el.find('.refclick'));
    }
}


function tabs_find_active(){
    if ($('.stunable-tab.tab.active').length){
    // console.log($('.stunable-tab.tab.active').offset().left)
        $('#tabs-container-container').animate({
             scrollLeft:$('.stunable-tab.tab.active').position().left + 200
        })
    }
    
}

function init_refclicks(selection){
    selection.click(function(e){
        var $t = $(this);
        e.preventDefault()
        url=$(this).data('href')
        $.post(url,function(response){
            if (response.result || response.success){
                if (response.callback){
                    refclickFunctions[response.callback]($t)
                }
            }
            if ($t.data('callback')){
                refclickFunctions[$t.data('callback')]($t)
            }
        },'json')
    })
}


function init_form_errors(context){
    $('.form_errors').modal();

    console.log(context)

    if (context == 'retailers'){
      $('.address_action').click(function(e){
        var t = $(this);
        if (t.data('val')=='suggested'){
          $('.validated_address_form').submit()
        }else{
        $.modal.close();
        }
      })
    }
    
    if (context == 'cart'){
     $('.address_action').click(function(e){
        var t = $(this);
        if (t.data('val')=='suggested'){
            $.modal.close();
            $('#btn-place-an-order').click()
        }else{
            $.modal.close();
        }
      })
    }

    if (context == 'accounts'){
     $('.address_action').click(function(e){
        var t = $(this);
        if (t.data('val')=='suggested'){
            $.modal.close();
            submit_shipping_option_form();
        }else{
            $.modal.close();
        }
      })
    }
}



function init_choiceclicks(selection){
    selection.click(function(e){
        var $t = $(this);
        url=$(this).data('href')
        $.post(url,{id:$(this).data('id'),val:$(this).val(),attr:$(this).data('attr')},function(response){
            if (response.result || response.success){
                if (response.callback){
                    refclickFunctions[response.callback]($t)
                }
            }
        },'json')
    })
}



var ac_cache = {};


$.widget( "custom.catcomplete", $.ui.autocomplete, {
    _renderItem: function( ul, item ) {
        var label_box = item.category != this.currentCategory ? $( '<a class="menu-space">' ).text( item.category ) :  $( '<a class="menu-space">').text( '');
        return $( '<li id="acmenu-'+item.slug+'">' )
            .append( label_box)
            .append( $( "<a>" ).text( item.label ) )
            .appendTo( ul );
    },
    _renderMenu: function( ul, items ) {
      var that = this;
      ul.append('<li>click to create a new tab</li>')
      that.currentCategory = "";
      $.each( items, function( index, item ) {
        if ( item.category != that.currentCategory ) {
          ul.append( "<li class='separator'></li>" );
        }
        that._renderItemData( ul, item ); 
        that.currentCategory = item.category;
      });
    }
  });



//this is for the tag/tab adding functionality
function init_refsubmits(selection){

    $.each(selection,function(){
        var $t = $(this);
        
        selection.autocomplete({
          minLength: 2,
          select: function( event, ui ) {

            $.post($t.data('href')+ui.item.slug,function(response){
                if (response.result || response.success){
                    if (response.callback){
                        refclickFunctions[response.callback]($t,response.data)
                    }
                }
            })
            $(this).val('')
            return false;
          },
          source: function( request, response ) {
            var term = request.term;
            if ( term in ac_cache ) {
              response( ac_cache[ term ] );
              return;
            }
            $.getJSON( $t.data('lookup'), request, function( data, status, xhr ) {
              ac_cache[ term ] = data;
              response( data );
            });
          },
        open: function(){
            $(this).autocomplete('widget').css('z-index', 100);
            return false;
        },

         messages: {
            noResults: '',
            results: function() {}
        }

        })
    })
}



//this is for the integrated flavor/item/tag search
function init_search(selection){

    $.each(selection,function(){
        var $t = $(this);
        
        selection.catcomplete({
          minLength: 2,
          delay:200,
          focus: function( event, ui ) {
            // event.preventDefault();
            $('.acmenu-active').removeClass('acmenu-active');
            $('#acmenu-'+ui.item.slug).addClass('acmenu-active');

            $(event.target).val(ui.item.label)
            return false;
          },
          select: function( event, ui ) {
            window.location = '/shop/'+ui.item.category+'/'+ui.item.slug+'?a=1'
            $(this).val('')
            return false;
          },
          source: function( request, response ) {
            var term = request.term;
            if ( term in ac_cache ) {
              response( ac_cache[ term ] );
              return;
            }
            $.getJSON( $t.data('lookup'), request, function( data, status, xhr ) {
              ac_cache[ term ] = data;
              response( data );
            });
          },
        open: function(){
            $(this).catcomplete('widget').css('z-index', 100);
            return false;
        },

         messages: {
            noResults: '',
            results: function() {}
        }

        })
    })
}

function reveal_cart(event,data,add){
    var height = '280px'
    
    if (data){
        $('#cart_contents_container').html(data)
    }
    var el = $('#cart_slide');

    if (add){
        height='191px'
        el.addClass('add')
    }else{
        el.removeClass('add')
    }

    el.fadeIn().animate({'height': height}, 400);
    var cart_close = setTimeout(close_cart,4000)
    el.hover(function(e){clearTimeout(cart_close)},function(e){cart_close = setTimeout(close_cart,1000)})//keeps cart out on re-hover, closes on leaving

    $('#cartcount').text($('#cart_items').data('length'))
}

function close_cart(){
    $('#cart_slide').animate({'height': '0px'}, 400).fadeOut();
}

function init_add_rack_modal() {
        $('.confirmation').hide();
        var options = {
            success : close_dialog
        };

        function close_dialog(resp, statusText, xhr, $form) {
            
            if ($(resp).find(".errorlist").length > 0){
                $('.confirmation').text($(resp).find(".errorlist > li").text());
                $('.confirmation').css('color', 'red');
            }else{
                $('.confirmation').text("Created!");
                $('.confirmation').css('color', 'gray');
                setTimeout("parent.$.modal.close()", 500);
                $(resp.result.target).append($(resp.result.html).hide().fadeIn('slow').droppable(DROPPABLE_OPTIONS));
            }
            $('.confirmation').show();
        }

        $('#rack-insert-form').ajaxForm(options);

        $('#btn_create').click(function(e) {
            e.preventDefault();
            if($('#name').attr('value') == 'Enter Rack name here' || $('#name').attr('value') == '') {
                
                $('#bigform-error').stop();
                $('#bigform-error').animate({
                    "opacity" : "1"
                }, "fast", function() {
                    changeError($('#bigform-error')[0], "Please Enter Rack Name");
                    $('.acct .password-field').css('margin-bottom', '0px');
                    $('#bigform-error').css('display', 'inline');
                });
                


            } else {
                $('#rack-insert-form').submit();
            }
        });
        
        $('.spinner').sprite({ fps: 10, no_of_frames: 12 });
    };


// BEGIN USER BASE
function initAddFriend(){
    // unbind the click function just in case
    $('.plus-inline:not(.friend_adder)').unbind("click");
    // when click on the add friend icon
    $('.plus-inline:not(.friend_adder)').click(function(){
        var current_item = $(this).parent().parent();
        var span = $(this).parent().find("span");
        var spinner = $('<div class="spinner" style="float:right;"></div>');
        var plusBtn = $(this);
        plusBtn.hide();         
        spinner.appendTo(plusBtn.parent());
        spinner.sprite({ fps: 10, no_of_frames: 12 });
        
        $.getJSON($(this).attr('href'), function(result){
            // remove the plus icon when invitation is sent
            plusBtn.remove();
            spinner.remove();
            // plusBtn.show();
            
            if(result['result'] == true){
                // notice user
                var temp = $(span).html();
                $(span).html("Request Sent!").delay(3000).fadeOut(500, function() {
                    $(span).html(temp);
                    $(span).fadeIn(500);
                });
            }else{
                alert(result['error']);
            }
        });
        return false;
    });
}

function listFilter(input, list) {
    $(input).change(function() {
        var filter = $(this).val();
        // get the value of the input, which we filter on
        if(filter) {
            $(list).find("span:not(:contains(" + filter + "))").parent().parent().slideUp();
            $(list).find("span:contains(" + filter + ")").parent().parent().slideDown();
        } else {
            $(list).find("li").slideDown();
        }
    }).keyup(function() {
        // fire the above change event after every letter
        $(this).change();
    }).keydown(function(e){
       //console.log(e)
    });
}




function getUserlist(input, list){
    var oldFilter = "";
    var original_friends=$('#result-list').clone()
    var form = $(input).parent();
    var href = $(form).attr('action');

    $(input).change(function(){
        // from the jquery document, the change event is fired 
        // only if the input loses focus, so we need to compare
        // the old and new value of the input box after it loses
        // focus, so we can decide to init the plus icon or just ignor 
        var filter = $(this).val();
        if (filter != oldFilter && filter != ""){
            var link = href + '?q=' + filter;           
            $.get(link, function(returnValue){
                console.log(returnValue)
                $('#result-list').children().remove();
                $.each(list, function(){
                    $(this).html(returnValue);
                });
                
                initFriendDragDrop();
                initAddFriend();
                initDragDrop();
                fixDragDropIssue()
                hookupFBMessages("{{STATIC_URL}}","{{URL}}");
                oldFilter = filter;
            });
        }else{
            $('#result-list').append(original_friends.children())
        }
        // else ignore it for god sake
    }).keydown(function(e){
        if (e.which == 13){
            return false;
        }
    }).keyup(function() {
        // fire the above change event after every letter
        $(this).change();
    })


}

// END USER BASE

var DRAGGABLE_OPTIONS = {
        helper: function () {
            return $(this).clone().removeAttr('style').removeClass('isotope-item').addClass('drag-helper').appendTo('body');
        },
        // appendTo : 'body',
        // opacity : .8,
        cursorAt : {
          top : 73,
          left : 60    
        },
        zIndex: 2700,
        // snap: ".drop_item",
        start: function(event, ui) {
           // console.log(ui)
           $('.drag_item').unbind('hover')
           $('.drop_item').addClass('drop_item_here')
       
        },
        stop: function(event, ui){

        $('.drag_item').hover(function(){
              $('.drop_item').toggleClass('drop_item_here')
         })
          
        }   
    }

var DROPPABLE_OPTIONS = {
        // accept : ".drag_item",

        hoverClass : "drop_item_hover",
        activeClass: "drop_item_here",
        drop : function(event, ui) {
          
            $.post('/racks/add_item/?item_id=' + item_id + '&rack=' + rack_id, function(returnData) {
                if (temp != "Item Added!"){
                    temp = $(droppable).html();
                }
               //console.log(returnData)                
                var text;
                if(returnData['result'] == 'ok') {
                    text = "Item Added!";
                } else {
                    text = "Error!";
                }
                $(droppable).html("Item Added!").css({'color':'#F05C68'}).delay(1000).fadeOut(500, function() {
                    $(droppable).html(temp);
                    $(droppable).fadeIn(500);
                });
            });
            return false;
            // alert("You have dragged " + item_name + " into " + rack_name);
        },
        over: function(e, ui){
            // $(ui.helper).addClass('tiny')
        }
    }


function initDrag(selection) {
    // console.log(selection)
    $(selection).draggable(DRAGGABLE_OPTIONS)
    $($('.private-racks')[1]).disableSelection();
    $($('.public-racks')[1]).disableSelection();
    fixDragDropIssue()
}

function initDrop(){
    ////console.log($('.drop_item'))
    $('.drop_item').droppable(DROPPABLE_OPTIONS);
}

function fixDragDropIssue(){
    var item_per_page = $($('.item_per_page')[0]).val();
    if(item_per_page == 6){
        $('.drag_item').draggable("option", "cursorAt", {left: 70, top: 70});
    }else if (item_per_page == 9){
        $('.drag_item').draggable("option", "cursorAt", {left: 60, top: 50});
    }
}


function hookupFBMessages(URL){
    $('.friend_adder').click(function(e){
        e.preventDefault();
        publish = {
          'method': 'feed'
          ,'link': URL
          ,'description': 'Hi, Check out Stunable'
          ,'name':"Stunable Invite"
          ,'to':$(this).attr('data-value')
          ,'picture':URL+'static/images/logo_small.jpg'
        }
        FB.ui(publish);
        $('.spinner').hide()
        return false;
    })
}


function initFriendDragDrop() { 
 
    var temp = "";
    
    $('.panel-content').find('.share_item').droppable({
        accept : ".drag_item",
        hoverClass : "drop_item_hover",
        drop : function(event, ui) {
            var item_id = $(ui.draggable).find('a').attr('data-value');
            // var rack_id = $(this).find('span').attr('data-value');
            var admirer_id = $(this).find('a').attr('data-value');
            var admirer_type = $(this).find('a').attr('data-type');
            var droppable = $(this).find('a');

            $('#reduced_item_id').val(item_id);
            $('#reduced_admirer_id').val(admirer_id);
            $('#reduced_admirer_type').val(admirer_type)
            $('#reduced_admirer_name').val($(this).find('a').attr('data-name'));
            
            if (admirer_type!='facebook'){
                $.fancybox({
                    'speedIn' : 1000,
                    'speedOut' : 500,
                    'overlayShow' : true,
                    'overlayOpacity' : 0.85,
                    'titleShow' : false,
                    'overlayColor' : '#000',
                    'transitionIn' : 'elastic',
                    'transitionOut' : 'elastic',
                    'easingIn' : 'easeOutBack',
                    'easingOut' : 'easeInBack',
                     'href' : '#send_to_admirer_reduced_form',
                     'onStart' : function() {
                        $('#loading2').hide();
                        $('#send_to_admirer_reduced_form').css('opacity', '0').show().delay(200).animate({
                                opacity : 1
                            }, 800);
                            $('#send_item_confirmation_reduced').hide();
                     },
                     'onCleanup' : function() {
                        $('#reduced_item_id').val("");
                        $('#reduced_admirer_id').val("");
                        $('#reduced_message').val("");
                        $('#reduced_admirer_type').val("")
                    },
                    'onClosed': function(){
                        $('#send_to_admirer_reduced_form').css('opacity', '0').css('display','none');
                    }
                  });
                  
                  $('#send_it_to_admirer_reduced').click(function(){
                        $('#loading2').css('display', 'inline');
                        $.get('/racks/sent_to_admirer/?'+ $('#reduced_send_to_admirer_form').serialize(), function(data) {
                            $('#loading2').css('display', 'none');
                            $("#send_item_confirmation_reduced").css('opacity','1').text(data.result == 'ok' ? "Sent" : "Error").show();
                            
                            if(data.result != 'ok') {
                                // do nothing here
                            } else {
                                // close fancy box after 2 second on success
                                setTimeout("parent.$.fancybox.close()", 2000);
                            }
                        },'json');
                  });
            }else{
                $.get('/racks/sent_to_admirer/?'+ $('#reduced_send_to_admirer_form').serialize(), function(data) {
                    FB.ui(data)
                })
            }}
        });
}

function touchHandler(event){
    //alert($(event.target).attr('class'))
  if($(event.target).hasClass('touchable') || $(event.target).parent().hasClass('touchable')){
     //alert(event.target)
     $('.iosSlider').data('touchCarousel').freeze()
      var touches = event.changedTouches,
          first = touches[0],
          type = "";

           switch(event.type)
      {
          case "touchstart": type = "mousedown"; $('.iosSlider').data('touchCarousel').freeze(); break;
          case "touchmove":  type="mousemove"; break;        
          case "touchend":   type="mouseup"; $('.iosSlider').data('touchCarousel').unfreeze(); break;
          default: return;
      }
      var simulatedEvent = document.createEvent("MouseEvent");
      simulatedEvent.initMouseEvent(type, true, true, window, 1,
                                first.screenX, first.screenY,
                                first.clientX, first.clientY, false,
                                false, false, false, 0/*left*/, null);

      first.target.dispatchEvent(simulatedEvent);
      event.preventDefault();
      //event.stopPropagation();
  }
}

function initRackEvents(){
    $('.editable').hide();

      $('.edit').click(function(event) {
          event.preventDefault();
          if($(this).html() == 'Edit') {
              $(this).html("Close");
          } else {
              $(this).html("Edit");
          }

          var stc = $(this).parent().parent().find('.static');
          var editable = $(this).parent().parent().find('.editable');

          if($(stc).css('display') == 'none') {
              $(stc).css('display', '');
              $(editable).css('display', 'none');
          } else {
              $(stc).css('display', 'none');
              $(editable).css('display', '');
          }
      });
      
      $('.editable').submit(function(event){
          event.preventDefault();
          var href = $(this).attr('action');
          var new_name = $($(this).find('input:text')[0]).val();
          var editable = $(this);
          $.post(href, $(editable).serialize(), function(returnData){
              if(returnData['success'] == true){
                  window.location.reload();
              }else{
                  console.log("There are some errors!");
              }
          });
      });
      
      $('.steal-rack-link').click(function(e){
          e.preventDefault();
          $.ajax({
              url : $(this).attr('href'),
              type : 'post',
              success : function(data, textStatus, jqXHR) {
                  if (data.success == true) {
                      $('.update-zipcode').hide();
                      new_item = $('<li class="drop_item ui-droppable"><span data-value="' + data.created_rack.id +  '"><a href="' + data.created_rack.url +'">' + data.created_rack.name +'</a></span></li>');
                      new_item.hide();
                      $('.public-racks').append(new_item);
                      new_item.fadeIn('slow');
                  } else {
                      alert(data.message);
                  }
              }
          });
      });
}

function pop_modal(text){
 $('<div class="info_modal">'+text+'</div>').modal()
}

function initTouch()
{
   document.addEventListener("touchstart", touchHandler, true);
   document.addEventListener("touchmove", touchHandler, true);
   document.addEventListener("touchend", touchHandler, true);
   document.addEventListener("touchcancel", touchHandler, true);    
}


// FROM RETAILERS

  function hide_form_errors()
    {
        $('.errorlist').remove();
    }

    function process_form_errors(json, form)
    {
        hide_form_errors();
        //form.clearForm();
        errors = json.errors;
    
        if (errors.__all__ != undefined)
            form.append(errors.__all__);

        prefix = form.find(":hidden[name='prefix']").val();

        prefix == undefined ? prefix = '' : prefix = prefix + '-';
        for (field in errors) {
            // console.log('#id_' + prefix + field);
            $('#id_' + prefix + field).after(errors[field]);
        }
    }



var PAYMENT_FORM_VALIDATE_OPTIONS = {
          submitHandler:function(form) {
            
            var d = $(form).serializeObject();


            var data ={
              "client_id":WEPAY_CLIENT_ID,
              "user_name":d.firstname+' '+d.lastname,
              "email":USER_EMAIL,
              "cc_number":$('#id_acct').val(),
              "cvv":$('#id_cvv2').val(),
              "expiration_month":$('#id_expdate_0').val(),
              "expiration_year":$('#id_expdate_1').val(),
              "address":
                {
                  "address1":d.street,
                  "city":d.city,
                  "state":d.state,
                  "country":d.countrycode,
                  "zip":d.zip
                }
            }

            var response = WePay.credit_card.create( data, function(data) {
              if (data.error) {

                pop_modal('There is a problem with your credit card information: <div class="form_error">'+ data.error_description+'</div>')

                // handle error response
              } else {
                $('#wepay_id').val(data.credit_card_id)
                $('#wepay_state').val(data.state)
                
                $.post($('#wepay_info').attr('action'),$('#wepay_info').serialize(),function(result){
                  if(result.success){
                    $('#payment-choice-form').html(result.html);
                    $('#payment-choice-form').fadeIn();
                    $('#payment-form').fadeOut();
                    $('.btn-place-an-order').click();
                  }
                },'json')

              }
            } );

            if (response.error) {
              alert(response.error_description)
              // handle error response
            }
              },
              rules: {
                firstname: "required",    // simple rule, converted to {required:true}
                lastname: "required",
                street: "required",
                city: "required",
                state: "required",
                countrycode: "required",
                zip: "required",
                acct: "required",
                expdate_0: "required",
                expdate_1: "required",
                cvv2: "required"
              },
              messages: {
                
              }
        }

function submit_shipping_option_form(){
    var form = $('#shipping-form');
    $.post(form.attr('action'),form.serialize(),function(result){
      if(result.success){
        $('#shipping-choice-form').html(result.html);
        $('#shipping-choice-form').fadeIn();

        form.fadeOut();
        $('.btn-place-an-order').click();

      }else{
        // we had errors validating the shipping address form
        form.html(result.html)
        init_form_errors($('body').attr('data-role'));
      }
    },'json')

    return false;
}

