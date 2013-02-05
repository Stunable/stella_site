
  var add_rack_modal_options = {
    afterOpenFunction:init_add_rack_modal,
  }


  var item_modal_options = {
    afterOpenFunction:init_item_modal,
  }

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
      //    //console.log(data)
      //   })

      // })
      if (! logged_in){
        $('#login_box').modal({clickClose: false})

      }

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

        // $(document).on($.modal.AJAX_COMPLETE, function(event, modal) {
        //  //console.log('ajax success')
           
        // });
    }
    ,rack: function(){
      initDrag($('.item'))
      initDrop(); 

    }
    ,cart: function(){

        function updateCartTotals(totals) {
            $("#cart-total").html(totals.total.toFixed(2));
            $("#cart-tax").html(totals.tax.toFixed(2));
            $("#cart-shipping").html(totals.shipping_and_handling.toFixed(2));
            $("#cart-grand-total").html(totals.grand_total.toFixed(2));
        }

        $('#checkout-btn').click(function(e) {
            e.preventDefault();

            if ($(this).hasClass('disabled')){
                return false;
            }
            // alert("Hang in there, we're not quite ready to go there yet.  Soon!")
            // return false;

            var zipcode = $('input[name="zipcode"]').val();
            
            if (valid_shipping_info && zipcode.length > 0)
                window.location.href = '{% url update_cart_info %}';
            
            if (zipcode.length == 0) {
                alert("Please enter zipcode");
            }
                
            if ($('html').hasClass('wait')) {
                alert('Please be patient, shipping and handling cost is being calculated');
            }
        });

        $(".cart-item").on('click', '.cart-remove', function(event) {
            event.preventDefault();
            var item = $(this).closest('.cart-item');
            $.ajax({
                url : $(this).attr('href'),
                type : 'post',
                success : function(data, textStatus, jqXHR) {
                    update_shipping_handling_fee();
                    item.fadeOut();
                    updateCartTotals(data);
                }
            })
        });

        $(".cart-item").on('click', '.cart-change-quantity', function(event) {
            event.preventDefault();
            var url = $(this).attr('href');
            $(this).hide();
            // TODO: JS templating
            $(this).parent().append("<div class='bootstrap' style='margin-top: 5px;'><form class='item-change-form form-horizontal' action='" + url + "' method='post'>" + "<div class='control-group'><input type='text' class='cart-new-quantity' name='quantity'>" + "<input style='margin-left: 5px;' type='submit' class='btn btn-primary' value='submit'></div></form></div>");
        });

        $('form').submit(function(e){
          e.preventDefault()
        })

        function update_shipping_handling_fee(event){
          if (event){
            event.preventDefault()
          }
            
            var zipcode = $('input[name="zipcode"]').val();
            valid_shipping_info = false;                
            if (zipcode.length == 5) {
                $('html').addClass('wait');
                $.ajax({
                    url : "{% url update_zipcode %}",
                    data : {
                        recipient_zipcode : $('input[name="zipcode"]').val(),
                        shipping_method : $('select[name="shipping-method"] option:selected').val()
                    },
                    type : 'post',
                    success : function(data, textStatus, jqXHR) {
                        $('html').removeClass('wait');
                        
                        if(data.success == true) {
                            valid_shipping_info = true;
                            updateCartTotals(data);
                            $('.update-zipcode').hide();
                        } else {
                            alert(data.message);
                        }
                    }
                });
            } else {
                $("#cart-shipping").text('0.00');   
            }
        }

        update_shipping_handling_fee();
        $('input[name="zipcode"]').keyup(update_shipping_handling_fee);

        $('#shipping_option_select').change(update_shipping_handling_fee);



        $(".cart-item").on('submit', '.item-change-form', function(event) {         
            event.preventDefault();
            var url = $(this).attr('action');
            var data = $(this).serialize();
            var quantity_el = $(this).siblings().filter('.cart-item-quantity');
            var size_el = $(this).siblings().filter('.cart-item-size');
            var change_link = $(this).siblings().filter(".cart-change-quantity");
            var form = $(this);
            $.ajax({
                url : url,
                data : data,
                type : 'post',
                success : function(data, textStatus, jqXHR) {
                    update_shipping_handling_fee();
                    updateCartTotals(data);
                    quantity_el.html(data.quantity);
                    size_el.html(data.size);
                    change_link.show();
                    form.remove();
                }
            });
        });
    
      }


}


    
$(document).ready(function() {
    var pageScrLoader = $('body').attr('data-role');
   //console.log('page:',pageScrLoader)
    if ( pageScrLoader && stunable[pageScrLoader] ) {
        return stunable[pageScrLoader].apply( this, stunable.common());
    } else if ( !pageScrLoader ) {
        return stunable.common.apply( this );
    }else{
        stunable.common();
    }
   //console.log( pageScrLoader + ' does not exist' );
});