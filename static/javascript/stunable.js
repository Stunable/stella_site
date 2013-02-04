
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
        console.log(e)
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
            console.log(ui.helper)
            $(ui.helper[0]).addClass("black");

            console.log('dragging',this)
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
            console.log(ui)
        }
    }


function initDrag(selection) {
    $(selection).draggable(DRAGGABLE_OPTIONS)
    $($('.private-racks')[1]).disableSelection();
    $($('.public-racks')[1]).disableSelection();
}

function initDrop(){
    console.log($('.drop_item'))
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


function hookupFBMessages(STATIC_URL,URL){
    $('.friend_adder').click(function(e){
        e.preventDefault();
        publish = {
          'method': 'feed'
          ,'link': URL
          ,'description': 'Hi, Check out Stunable'
          ,'name':"Stunable Invite"
          ,'to':$(this).attr('data-value')
          ,'picture':URL+STATIC_URL+'/images/logo_small.jpg'
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
                          
                           // initFancyBox('#add-rack ');
                           //    initFancyBox('#add-friend ');
                          // initFancyBox();

                          // fixDragDropIssue();
                      });
                      if($('.friend-search-box').length > 1) {
                          // because there are exactly identical elements so i need to choose the last one (the first one is hidden)
                          // listFilter($('.friend-search-box')[1], $('.friend-list')[1]);
                          getUserlist($('.friend-search-box')[1], $('.search-result'));
                          initFriendDragDrop();
                          initDrop()
                          // hookupFBMessages(static_url,url);
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
                        // console.log(slider)
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
