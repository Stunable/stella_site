
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
    'remove' : function(selection){
        $(selection.data('target')).fadeOut('slow')
    },
    'downvote': function(selection){
        $(selection.data('target')).removeClass('upvoted').addClass('downvoted')
    },
    'upvote': function(selection){
        $(selection.data('target')).removeClass('downvoted').addClass('upvoted')
    },
    'clearvote': function(selection){
        $(selection.data('target')).removeClass('downvoted').removeClass('upvoted')
    },
}


function init_refclicks(selection){
    selection.click(function(e){
        var $t = $(this);
        e.preventDefault()
        url=$(this).data('href')
        $.post(url,function(response){
            console.log(response)
            if (response.result || response.success){
                if (response.callback){
                    console.log(response.callback)
                    refclickFunctions[response.callback]($t)
                }
            }
        },'json')
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


    el.animate({'height': height}, 400);
    var cart_close = setTimeout(close_cart,4000)
    el.hover(function(e){clearTimeout(cart_close)},function(e){cart_close = setTimeout(close_cart,1000)})//keeps cart out on re-hover, closes on leaving
}

function close_cart(){
    $('#cart_slide').animate({'height': '0px'}, 400);
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
        helper : "clone",
        appendTo : 'body',
        opacity : .8,
        cursorAt : {
          top : 73,
          left : 145    
        },
        zIndex: 2700,
        // snap: ".drop_item",
        start: function(event, ui) {
           //console.log(ui.helper)
            $(ui.helper[0]).addClass("black");

           //console.log('dragging',this)
            if ($('.iosSlider').data('touchCarousel')){
                $('.iosSlider').data('touchCarousel').freeze();
            }

            prevs = $(this).parent().parent().prevAll();            
            $(prevs).each(function(){
                if(!$(this).hasClass('prev')){
                    $(this).addClass('prev');
                }
            });
            next = $(this).parent().parent().next();
            if(!$(next).hasClass('nxt')){
                $(next).addClass('nxt');
            }
            
            //$('.iosSlider').css('overflow','visible');
            $('#prev').off('hover');
            $('#next').off('hover');
        },
        stop: function(event, ui){
            // slideNum = calcSlide();
             if ($('.iosSlider').data('touchCarousel')){
                $('.iosSlider').data('touchCarousel').unfreeze();
            }
            
            $('.prev').each(function(){
                $(this).removeClass('prev');
            });
            $('.nxt').each(function(){
                $(this).removeClass('nxt');
            });
            $('.iosSlider').css('overflow','hidden');
            $('#prev').on('hover');
            $('#next').on('hover');
        }
    }

var DROPPABLE_OPTIONS = {
        // accept : ".drag_item",

        hoverClass : "drop_item_hover",
        activeClass: "drop_item_here",
        drop : function(event, ui) {
            var temp="";
            // find the next ul which have the 'nxt' class and remove it
            $('.nxt').each(function(){
                $(this).removeClass('nxt');
            });
            // var item_id = $(ui.draggable).find("a").attr('data-value');
            // var item_id = $(ui.draggable).find('h4').find('a').attr('data-value');
            var item_id = $(ui.draggable).find('a').attr('data-value');
            var rack_id = $(this).find('span').attr('data-value');
            var droppable = $(this).find('span');
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
            ////console.log(ui)
        }
    }


function initDrag(selection) {
    // console.log(selection)
    $(selection).draggable(DRAGGABLE_OPTIONS)
    $($('.private-racks')[1]).disableSelection();
    $($('.public-racks')[1]).disableSelection();
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

function setupCarousel(selection){
    selection.touchCarousel({
        itemsPerMove: 3,              // The number of items to move per arrow click.
        
        snapToItems: true,           // Snap to items, based on itemsPerMove.
        pagingNav: false,             // Enable paging nav. Overrides snapToItems.
                                      // Snap to first item of every group, based on itemsPerMove. 
                                      
        pagingNavControls: false,      // Paging controls (bullets).
        
        scrollSpeed:1,
        
        autoplay:false,               // Autoplay enabled.
        autoplayDelay:100,            // Delay between transitions.
        autoplayStopAtAction:true,    // Stop autoplay forever when user clicks arrow or does any other action.
        
        scrollbar: true,              // Scrollbar enabled.
        scrollbarAutoHide: false,     // Scrollbar autohide.
        scrollbarTheme: "light",       // Scrollbar color. Can be "light" or "dark".    
        
        transitionSpeed: 600,         // Carousel transition speed (next/prev arrows, slideshow).       
        
        directionNav:true,            // Direction (arrow) navigation (true or false).
        directionNavAutoHide:false,   // Direction (arrow) navigation auto hide on hover. 
                                      // On touch devices arrows are always displayed.
        
        loopItems: false,             // Loop items (don't disable arrows on last slide and allow autoplay to loop).
        
        keyboardNav: true,           // Keyboard arrows navigation.
        dragUsingMouse:true,          // Enable drag using mouse.   
        
        
        scrollToLast: true,          // Last item ends at start of carousel wrapper.    
        
        
        itemFallbackWidth: 500,       // Default width of the item in pixels. (used if impossible to get item width).
        
        baseMouseFriction: 0.0012,    // Container friction on desktop (higher friction - slower speed).
        baseTouchFriction: 0.0008,    // Container friction on mobile.
        lockAxis: true,               // Allow dragging only on one direction.
        useWebkit3d: false,           // Enable WebKit 3d transform on desktop devices. 
                                      // (on touch devices this option is turned on).
                                      // Use it if you have only images, 3d transform makes text blurry.
                                               
        
        onAnimStart: null,            // Callback, triggers before deceleration or transition animation.
        onAnimComplete: function(){

            number_of_slides = this.numItems;
            currentSlideNum = this.getCurrentId();
            var slider = this;
            if (number_of_slides - currentSlideNum <= 6){
                $.ajax({
                    url: '?page=' + slider._next_page + '&item_per_page=' + 6,
                    success: function(data) {
                        var items = $(data).find('.item')
                        $('.touchcarousel-container').append(items);
                        slider.addItems(items);
                        slider._next_page = parseInt($(data).attr('data-nextpage'))
                        ////console.log(slider)
                        initDrag(items);
                        fixDragDropIssue();
                    }
                    ,dataType:'html'
                });
            }
        },         // Callback, triggers after deceleration or transition animation.
        
        onDragStart:null,             // Callback, triggers on drag start.
        onDragRelease: null           // Callback, triggers on drag complete.
    }); 

    initDrag(selection.find('.item'))
}

function initSwipe(selection){
               
    // initDesktopSwipe();
    if($('.iosSlider').length){
        sliderInstance = $('.iosSlider').data('touchCarousel');
        sliderInstance.swipeStart = new Date();
        function handle(delta) {
            if (Math.abs(delta)>.02){
                //var c = sliderInstance._getXPos();
                if (delta > 0){
                    //sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");  
                    sliderInstance.prev()

                }else{
                    sliderInstance.next()
                    //sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");  
                }
            }
        }

        function wheel(event){
            var delta = 0;
            //if (!event) event = window.event;
            if (event.originalEvent.wheelDelta) {
                delta = event.originalEvent.wheelDelta/120; 
            } else if (event.originalEvent.detail) {
                delta = -event.originalEvent.detail/3;
            }
            //console.log(delta)
            var now = new Date()
            if (!sliderInstance._isAnimating && now - sliderInstance.swipeStart > (sliderInstance.settings.transitionSpeed*1.5)){
                handle(delta);
                sliderInstance.swipeStart = now;
            }

            if (event.preventDefault)
                event.preventDefault();
            event.originalEvent.returnValue = false;
        }

        if (selection){
            $(selection).on( "mousewheel DOMMouseScroll", wheel);
        }

        $('.iosSlider').css('overflow','hidden');
    }
}


function setupRackIt(){
    // prevent more binds when close fancy box
    $('.rack-icon').unbind("click");
    $('.rack-icon').click(function(event){
        event.preventDefault();
        var href = $(this).attr('href');
        var item_id = $(this).attr('data-value');
        var containers = $('.private-racks').find('li span');
        if (containers.length > 0){
            rack_id = $(containers[0]).attr('data-value');
        }else{
            rack_id = "myrack";
        }
        
        var link = href + 'item_id=' + item_id +'&rack=' + rack_id;
        $.get(link, function(result){
            if(result['result'] == 'ok'){
                alert("Item Added!");
                if(result['new_rack_id']){
                    // add a new rack name My Rack into the left-nav by using javascript
                    $('.private-racks').html('<li class="drop_item ui-droppable">'+
                                            '<span data-value="'+ result['new_rack_id'] +'"><a href="/racks/detail/' + result['new_rack_id'] + '">' +
                                            'My Rack</a></span></li>');
                    initDragDrop();
                    fixDragDropIssue();
                }
                // check if fancy box is opened
                if($('#fu').length > 0){
                    parent.$.fancybox.close();
                }
            }else{
                alert(result['Error']);
            }
        });
    });
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

function initTouch()
{
   document.addEventListener("touchstart", touchHandler, true);
   document.addEventListener("touchmove", touchHandler, true);
   document.addEventListener("touchend", touchHandler, true);
   document.addEventListener("touchcancel", touchHandler, true);    
}