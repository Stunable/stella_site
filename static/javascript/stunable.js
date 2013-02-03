
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


function initDragDrop(selection) {
    if (! selection){
        var selection = $('.drag_item')
    }   
    selection.draggable({
        helper : "clone",
        appendTo : 'body',
        opacity : 0.6,
        cursorAt : {
          top : 200,
          left : 100    
        },
        zIndex: 2700,
        start: function(event, ui) {
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
    });
    var temp = "";
    $('.panel-content').find('.drop_item').droppable({
        accept : ".drag_item",
        hoverClass : "drop_item_hover",
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
        }
    });

    $($('.private-racks')[1]).disableSelection();
    $($('.public-racks')[1]).disableSelection();
}
