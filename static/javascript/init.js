var stunable = {
    common : function() {

      var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
      $(document).ajaxSend(function(e, xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
      });

      $($('.private-racks')[1]).sortable({
          stop : function(e, ui) {
          }
      });
      $($('.public-racks')[1]).sortable({
          stop : function(e, ui) {
          }
      });

      // $('.click_href').click(function(e){
      //   $.post($(this).data('href'),function(data){
      //     console.log(data)
      //   })

      // })

    }
    ,shop: function(){ 
        setupCustomTabs($('#left-panel'));             
        setupCarousel($('.iosSlider'));

        $('.panel-inner-content').html($('.panel-header .active').find('.tab-content').html()).fadeIn(1000, function() {
                // initDragDrop();

                // hookupFBMessages(static_url,url);
                // fixDragDropIssue();
        });   

        initSwipe($('.iosSlider'))
        initDrop(); 
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
    console.log( pageScrLoader + ' does not exist' );
});