
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