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


(function($) {
    $.fn.textfill = function(maxFontSize) {
        maxFontSize = parseInt(maxFontSize, 10);
        return this.each(function(){
            var ourText = $("span", this),
                parent = ourText.parent(),
                maxHeight = parent.height(),
                maxWidth = parent.width(),
                fontSize = parseInt(ourText.css("fontSize"), 10),
                multiplier = maxWidth/ourText.width(),
                newSize = (fontSize*(multiplier-0.1));
                console.log('mw',maxWidth)
                // console.log('h',maxHeight)
                // console.log(newSize)
                console.log('pw',ourText.width())
                console.log(multiplier)
            ourText.css(
                "fontSize", 
                (maxFontSize > 0 && newSize > maxFontSize) ? 
                    maxFontSize : 
                    newSize
            );
        });
    };
})(jQuery);
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
        $('#tabs-container').animate({
             scrollLeft:$('.stunable-tab.tab.active').position().left - 220
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

function init_refsubmits(selection){
    var $t = selection;
    
    selection.autocomplete({
      minLength: 2,
      select: function( event, ui ) {

        $.post(selection.data('href')+ui.item.slug,function(response){
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
        $.getJSON( "/lookups/tagging/tag", request, function( data, status, xhr ) {
          ac_cache[ term ] = data;
          response( data );
        });
      }
      
    });
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

function setupCustomTabs(selection){
    $(selection).find('.panel-tab').click(function() {
          var t = $(this)
              if(!t.hasClass('active')) {
                  $('.panel-tab.active').removeClass('active');
                  t.addClass('active');
                  $('.panel-inner-content').fadeOut(500, function() {
                      $('.panel-inner-content').html(t.find('.tab-content').html()).fadeIn(500, function() {
                          initDrop();
                          initFriendDragDrop()
                           // initFancyBox('#add-rack ');
                           //    initFancyBox('#add-friend ');
                          // initFancyBox();

                          // fixDragDropIssue();
                      });
                      if($('.friend-search-box').length > 1) {
                          console.log('friend search')
                          // because there are exactly identical elements so i need to choose the last one (the first one is hidden)
                          listFilter($('.friend-search-box')[1], $('.friend-list')[1]);
                          getUserlist($('.friend-search-box')[1], $('.search-result'));
                          initFriendDragDrop()
                          hookupFBMessages(root_url);
                      }
                  });
              }
        });

    $('.panel-inner-content').html($('.panel-header .active').find('.tab-content').html()).fadeIn(1000, function() {
                

                // hookupFBMessages(static_url,url);
                // fixDragDropIssue();
    });   
}

// function setupCarousel(selection){
//     selection.touchCarousel({
//         itemsPerMove: 2,              // The number of items to move per arrow click.
        
//         snapToItems: true,           // Snap to items, based on itemsPerMove.
//         pagingNav: false,             // Enable paging nav. Overrides snapToItems.
//                                       // Snap to first item of every group, based on itemsPerMove. 
                                      
//         pagingNavControls: false,      // Paging controls (bullets).
        
//         scrollSpeed:1,
        
//         autoplay:false,               // Autoplay enabled.
//         autoplayDelay:100,            // Delay between transitions.
//         autoplayStopAtAction:true,    // Stop autoplay forever when user clicks arrow or does any other action.
        
//         scrollbar: true,              // Scrollbar enabled.
//         scrollbarAutoHide: false,     // Scrollbar autohide.
//         scrollbarTheme: "light",       // Scrollbar color. Can be "light" or "dark".    
        
//         transitionSpeed: 600,         // Carousel transition speed (next/prev arrows, slideshow).       
        
//         directionNav:true,            // Direction (arrow) navigation (true or false).
//         directionNavAutoHide:false,   // Direction (arrow) navigation auto hide on hover. 
//                                       // On touch devices arrows are always displayed.
        
//         loopItems: false,             // Loop items (don't disable arrows on last slide and allow autoplay to loop).
        
//         keyboardNav: true,           // Keyboard arrows navigation.
//         dragUsingMouse:true,          // Enable drag using mouse.   
        
        
//         scrollToLast: true,          // Last item ends at start of carousel wrapper.    
        
        
//         itemFallbackWidth: 500,       // Default width of the item in pixels. (used if impossible to get item width).
        
//         baseMouseFriction: 0.5112,    // Container friction on desktop (higher friction - slower speed).
//         baseTouchFriction: 0.0008,    // Container friction on mobile.
//         lockAxis: true,               // Allow dragging only on one direction.
//         useWebkit3d: false,           // Enable WebKit 3d transform on desktop devices. 
//                                       // (on touch devices this option is turned on).
//                                       // Use it if you have only images, 3d transform makes text blurry.
                                               
        
//         onAnimStart: null,            // Callback, triggers before deceleration or transition animation.
//         onAnimComplete: function(){

//             number_of_slides = this.numItems;
//             currentSlideNum = this.getCurrentId();
//             var slider = this;
//             if (number_of_slides - currentSlideNum <= 6){
//                 $.ajax({
//                     url: '?page=' + slider._next_page + '&item_per_page=' + 6,
//                     success: function(data) {
//                         var items = $(data).find('.item')
//                         $('.touchcarousel-container').append(items);
//                         slider.addItems(items);
//                         slider._next_page = parseInt($(data).attr('data-nextpage'))
//                         ////console.log(slider)
//                         initDrag(items);
//                         fixDragDropIssue();

//                         $(items).find('img').load(function(){
//                             $(this).hide().show().css('border','3px solid white').css('border-radius','10px');
//                             console.log(this)
//                         })
//                     }
//                     ,dataType:'html'
//                 });
//             }
//         },         // Callback, triggers after deceleration or transition animation.
        
//         onDragStart:null,             // Callback, triggers on drag start.
//         onDragRelease: null           // Callback, triggers on drag complete.
//     }); 

//     initDrag(selection.find('.item'))
// }


// function initSwipe(selection){
               
//     // initDesktopSwipe();
//     if($('.iosSlider').length){
//         sliderInstance = $('.iosSlider').data('touchCarousel');
//         sliderInstance.swipeStart = new Date();
//         function handle(delta) {
//             if (Math.abs(delta)>.02){
//                 //var c = sliderInstance._getXPos();
//                 if (delta > 0){
//                     //sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");  
//                     sliderInstance.prev()

//                 }else{
//                     sliderInstance.next()
//                     //sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");  
//                 }
//             }
//         }

//         function wheel(event){
//             var delta = 0;
//             //if (!event) event = window.event;
//             if (event.originalEvent.wheelDelta) {
//                 delta = event.originalEvent.wheelDelta/120; 
//             } else if (event.originalEvent.detail) {
//                 delta = -event.originalEvent.detail/3;
//             }
//             //console.log(delta)
//             var now = new Date()
//             if (!sliderInstance._isAnimating && now - sliderInstance.swipeStart > (sliderInstance.settings.transitionSpeed*1.5)){
//                 handle(delta);
//                 sliderInstance.swipeStart = now;
//             }

//             if (event.preventDefault)
//                 event.preventDefault();
//             event.originalEvent.returnValue = false;
//         }

//         if (selection){
//             $(selection).on( "mousewheel DOMMouseScroll", wheel);
//         }

//         $('.iosSlider').css('overflow','hidden');
//     }
// }





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