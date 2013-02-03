var stunable = {
    common : function() {

    }
    ,shop: function(){              
        $('.panel-tab').click(function() {
              if(!$(this).hasClass('active')) {
                  $('.panel-tab').removeClass('active');
                  $(this).addClass('active');
                  $('.panel-inner-content').fadeOut(500, function() {
                      $('.panel-inner-content').html($('.panel-header .active').find('.tab-content').html()).fadeIn(500, function() {
                          initDragDrop();
                          
                              initFancyBox('#add-rack ');
                              initFancyBox('#add-friend ');
                          initFancyBox();

                          fixDragDropIssue();
                      });
                      if($('.friend-search-box').length > 1) {
                          // because there are exactly identical elements so i need to choose the last one (the first one is hidden)
                          // listFilter($('.friend-search-box')[1], $('.friend-list')[1]);
                          getUserlist($('.friend-search-box')[1], $('.search-result'));
                          initFriendDragDrop();
                          hookupFBMessages("{{STATIC_URL}}","{{URL}}");
                      }
                  });
              }
        });

        $('.panel-inner-content').html($('.panel-header .active').find('.tab-content').html()).fadeIn(1000, function() {
                initDragDrop();
                initFancyBox('#add-rack ');
                initFancyBox('#add-friend ');
                initFancyBox();
                hookupFBMessages("{{STATIC_URL}}","{{URL}}");
                fixDragDropIssue();
        });
          
    }
}


    
$(document).ready(function() {
    var pageScrLoader = $('body').attr('data-role');
    console.log('page:',pageScrLoader)
    if ( pageScrLoader && stunable[pageScrLoader] ) {
        return stunable[ pageScrLoader ].apply( this, stunable.common());
    } else if ( !pageScrLoader ) {
        return stunable.common.apply( this );
    }else{
        stunable.common();
    }
    debug( pageScrLoader + ' does not exist' );
});