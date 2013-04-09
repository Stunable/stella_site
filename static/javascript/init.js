
var stunable = {

    common : function() {



      var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
      $(document).ajaxSend(function(e, xhr, settings) {
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
      });


      init_form_errors();

      $('.login-check').click(function(e){
        e.preventDefault();
          var dest = $(this).data('href')
          $.post('/accounts/check_login',function(data){
              console.log(data)
              if (data.result){
                window.location = dest;
              }else{
                var box = $('#login_box').clone()
                box.find('.login-href-button').each(function(){
                 var orig =  $(this).attr('href');
                 $(this).attr('href',orig+'?go='+dest);
                })
               box.modal({})   
                // $('<div style="height:400px;width:400px" class="info_modal">Your Upload is in progress.  When this goes away, that means it\'s done!</div>').modal({clickClose: false,escapeClose:false,showClose:false})
              }
          })
          return false
      })

            

      init_refclicks($('.refclick'))
      init_choiceclicks($('.choiceclick'))
      init_refsubmits($('.refsubmit'))

      $('.arbitrary_modal').click(function(e){
        console.log( $($(this).data('target')))
        $($(this).data('target')).modal()
      })

      init_form_errors($('body').attr('data-role'));

        $('.left-panel>ul>li').click(function(e){
          e.stopPropagation();  
          $('.left-panel>ul>li.active').removeClass('active');
          $(this).addClass('active');
          if ($(this).find('a').length){
            window.location = $(this).find('a').attr('href');

          }
          // return false;
        })

        $('#nav-handle').toggle(
            function(){
              $('#page-content').animate({'left':'20px'},400)
            },
            function(){
              $('#page-content').animate({'left': '220px'},400)
            }
        )

     
        $('.click-toggle').toggle(function(e){
          e.stopPropagation();
          $($(this).data('target')).fadeIn()

        },function(){
          $($(this).data('target')).fadeOut()

        })

      
        $('.click-show').click(function(e){
          e.preventDefault();
          var t = $($(this).data('target'))
          if (t.is(':visible')){
            t.hide();
          }else{
 
            $($(this).data('target')).show().focus();
          }
        })

        tabs_find_active()
      

        $('.hover_help').hover(
          function(){
            $($(this).data('target')).fadeIn();
          },function(){
            $($(this).data('target')).fadeOut();
        })

    }
    ,shop: function(){    

      // var add_function = function(items){
      //       // $('#container').isotope('insert', items)
      //       $('#container').append(items)
      // }


      // if (navigator.userAgent.toLowerCase().indexOf("iphone") == -1){ 
          window.onload = function(){
            // console.log('not iphone')
            $('#container').isotope(isotope_options[$('.scrollbox').data('type')])
            // initDrag($('.item'))
            // initDrop(); 
            // fixDragDropIssue()     
        }
        add_function = function(items){
            $('#container').isotope('insert', items)
        }

      // }     

      
        $('.scrollbox').damonscroll({
          orientation: $('.scrollbox').data('orient'),
          target_element: $('#container'),
                // $('#container').append(items)
          add_function: add_function

        })

        var isotope_options = {

          'carousel':{
           layoutMode: 'cellsByColumn',
            cellsByRow: {
              columnWidth: 100,
              rowHeight: 100
              // animationEngine : 'css'
            }},

          'list':{

          }

        }





        // $('.drag_item').hover(function(){
        //   $('.drop_item').toggleClass('drop_item_here')
        // })

    }
    ,racks: function(){
      // console.log('racks setup')
      // initDrop(); 
      // initDrag($('.item'))
      initRackEvents();    

    }
    ,cart: function(){

        zipcode = [];
        function updateCartTotals(totals) {
            $("#cart-total").html(totals.total.toFixed(2));
            $("#cart-tax").html(totals.tax.toFixed(2));
            $("#cart-shipping").html(totals.shipping_and_handling.toFixed(2));
            $("#cart-grand-total").html(totals.grand_total.toFixed(2));
        }

        $('#checkout-btn').click(function(e) {
            e.preventDefault();
        });

       

        $(".cart-item").on('click', '.cart-change-quantity', function(event) {
            event.preventDefault();
            var url = $(this).attr('href');
            $(this).hide();
            // TODO: JS templating
            $(this).parent().append("<div class='bootstrap' style='margin-top: 5px;'><form class='item-change-form form-horizontal' action='" + url + "' method='post'>" + "<div class='control-group'><input type='text' class='cart-new-quantity' name='quantity'>" + "<input style='margin-left: 5px;' type='submit' class='btn btn-primary' value='submit'></div></form></div>");
        });


        $('.clear_choice_on_change').find('input').focus(function(e){
          $($(this).closest('form').data('choicetarget')).find("input:checked").attr('checked',false)
        })

        $('#payment-form').validate(PAYMENT_FORM_VALIDATE_OPTIONS)
            

        $('.btn-place-an-order').click(function(e){
          e.preventDefault();

          var shipping_choice = $('#shipping-choice-form').find("input:checked" )
          var payment_choice = $('#payment-choice-form').find("input:checked" )


          if(!shipping_choice.length){
            submit_shipping_option_form()
          }

          if(!payment_choice.length){
              $('#payment-form').submit()             
          }

          if (shipping_choice.length && payment_choice.length){
             $('<div class="info_modal"><div class="bootstrap">Ready to place your order. Are you sure?<div style="float:right;margin:8px"><a id="place_order_for_real_btn" class="btn" href="">Yes.</a></div></div></div>').modal(

              {
                afterOpenFunction:function(){
                    console.log('order place post open')
                    $('#place_order_for_real_btn').click(function (e){
                          $('<div class="info_modal"><div>We are placing your order.  Please Wait a moment.</div><img src="/static/images/loading.gif"> </div>').modal({clickClose: false,escapeClose:false,showClose:false})
                          $.post('/cart/order_placed',
                              $.extend($('#shipping-choice-form').serializeObject(),$('#payment-choice-form').serializeObject()),
                                function(data){
                                  if (data.success){
                                    window.location = data.redirect;
                                  }else{
                                    pop_modal('<div>Sorry, An error occured:</div><div>'+data.error+'</div>');
                                  }

                                }                
                            )
                        return false;
                        })
                      }
                })
       

            }
          })


        

    },
      retailers:function(){
        $('#select_all').click(function(e){
          $('.ship_check').attr('checked',$(this).attr('checked')==='checked');
        })
          function hide_form_errors() {
            $('.errorlist').remove();
          }

          function process_form_errors(json, form) {
            hide_form_errors();
            //form.clearForm();
            errors = json.errors;

            if(errors.__all__ != undefined)
              form.append(errors.__all__);
            prefix = form.find(":hidden[name='prefix']").val(); prefix == undefined ? prefix = '' : prefix = prefix + '-';
            
            for(field in errors) {
              $('#id_' + prefix + field).after(errors[field]);
            }
          }

          inventory_option_counter = 1;
        var term_doc = $('#terms-and-cons-modal');
        $('#terms-label').css('color', 'black');

        $('#terms-input').change(function(){
            $('#terms-continue-btn').attr('href', $(this).data('href')).removeClass('disabled').click(function(e){
                if (!$('#terms-input').is(':checked')) {
                    e.preventDefault();
                } 
            });
        })

           $('select[name=image]').ImageSelect(); 
           $('select[name=featured_image]').ImageSelect(); 
           
           $('.imageselector').ImageSelect();

           $('.deetsclick').click(function(){
            $(this).closest('.product_row').toggleClass('nodeets')
           })

           $('.select_all').click(function () {
               $($(this).data('target')).attr('checked', this.checked);
           });

           $('.delete-link').click(function(){
                $(this).closest('td').find('.item_selector').attr('checked','checked');
                
                $('#action_select').val('delete');
                $('.action_submit').submit();
                return false;
           })

           $('.click_to_expand').click(function(e){
              $(this).parent().toggleClass('collapsed')
              return false
           })



           $('#id_uploaded_zip').click(function(e){
              $('.submit_holder  input').attr('disabled',false);
              $(this).css('color','grey');
            
            $('.long_process_submit_form').submit(function(){
             $('<div class="info_modal">Your Upload is in progress.  When this goes away, that means it\'s done!</div>').modal({clickClose: false,escapeClose:false,showClose:false})
              // sleep(3000)
            })
           })

           try{
           if (updates_in_progress){
            setTimeout("location.reload(true);",5000);
            setInterval(function(){
              $('#progress_box').append('. ').fadeIn('slow')
            },200)
           }}catch(err){}

              for( i = 0; i < parseInt($('#id_types-INITIAL_FORMS').val()); i++) {
                inventory_option_counter++;
                // $('#tbl-' + inventory_option_counter).show();
              }
              if (inventory_option_counter == 1){
                $('#add-more-option').hide()
                $('#tbl-1').show()
              }
              
              
              $('.add-color-popup-btn .plus-icon').click(function() {
                $('.fixed-popup').remove();
                $(this).parent().append('<div class="fixed-popup">' + $('.add-color-dlg').html() + '<div>');
                $('.fixed-popup').show('fast');
                $('.fixed-popup input[type="text"]').focus();
                
                $('.add-color-form').ajaxForm({
                  url : this.action,
                  // dataType : 'json',
                  success : function(json) {
                    if (json.success) {
                      $('.color-select select').append(new Option(json.name, json.id));
                      $('.fixed-popup .alert-message').text('Updated')
                      $('.fixed-popup').delay(3000).hide('fast');
                    } else {
                      $('.fixed-popup .alert-message').text(json.errors.__all__[0]);            
                    }
                  }
                });
                
                $('.fixed-popup .btn-cancel').click(function() {
                  $('.fixed-popup').hide('fast');
                });
              });
              
              $('.add-size-popup-btn .plus-icon').click(function() {
                console.log('efwefwef')
                $('.fixed-popup').remove();
                $(this).parent().append('<div class="fixed-popup">' + $('.add-size-dlg').html() + '<div>');
                $('.fixed-popup').show('fast');
                $('.fixed-popup input[type="text"]').focus();
                
                $('.add-size-form').ajaxForm({
                  url : this.action,
                  // dataType : 'json',
                  success : function(json) {
                    if (json.success) {
                      $('.size-select select').append(new Option(json.name, json.id));
                      $('.fixed-popup .alert-message').text('Updated')
                      $('.fixed-popup').delay(3000).hide('fast');
                    } else {
                      $('.fixed-popup .alert-message').text(json.message);            
                    }
                  }
                });
                
                $('.fixed-popup .btn-cancel').click(function() {
                  $('.fixed-popup').hide('fast');
                });

              });

              $('.onsale_check').find('input').click(function(e){
                if ($(this).is(':checked')){
                  $(this).closest('table').find('.sale_price_field').show()
                }else{
                  $(this).closest('table').find('.sale_price_field').hide()
                }
              })

              $('#add-more-option').click(function() {
                $('#tbl-' + inventory_option_counter).show('fast');
                $('#tbl-' + inventory_option_counter +' .imageselector,  select[name=image]').ImageSelect('remove');
                $('#tbl-' + inventory_option_counter +' .imageselector,  select[name=image]').ImageSelect();
                $(this).remove()
                return false
              });

              $('#id_tags').chosen();
              $('#id_Sizes').after("<a class='icon plus-icon item-ref' href='{% url add_size %}'>&nbsp</a>");
              $('#id_Colors').after("<a class='icon plus-icon item-ref' href='{% url add_color %}'>&nbsp</a>");
              // $('.inventory').tooltip();

              var add_item_form = $('#add-item-form');

              add_item_form.ajaxForm({
                url : this.action,
                dataType : 'json',
                success : function(json) {
                  if(json.success == false) {
                    if(json.message != undefined && json.message)
                      alert(json.message);

                    if(json.errors != undefined)
                      process_form_errors(json, add_item_form)
                  } else {
                    window.location.href = '/product_list';
                  }
                }
              });
              var active_image_form = null;
              $('.addProductImage').click(function(){

                $('.clonedform').remove();
                var cln = $('#new_image_form').clone();

                $(this).after(cln.addClass('clonedform').show())


                cln.find('form').ajaxForm({
                        url : this.action,
                        // dataType : 'json',
                        success : function(json) {
                          if (json.success) {
                            setTimeout(function(){
                              var $newel = $(json.html)
                              $('.imageselector,  select[name=image], select[name=featured_image]').append($newel)
                              active_image_form.find('.new_image_'+json.message).attr('selected','selected')
                              $('.imageselector,  select[name=image], select[name=featured_image]').ImageSelect('remove');
                              $('.imageselector,  select[name=image], select[name=featured_image]').ImageSelect();
                              $(cln).fadeOut(1000).remove()
                            },1000)
                            
                            

                          } else {
                            $('.fixed-popup .alert-message').text(json.message);            
                          }
                        }
                      });

                $('#id_new-image').change(function(){
                  cln.find('form').submit()
                  active_image_form = cln.closest('td').find('select');
                })
                return false
              })

        
          $('#id_accept_refund').change(function(e){
            if ($(this).is(':checked')){
              $('#id_not_accept_refund').attr('checked',false)
            }
          })
           $('#id_not_accept_refund').change(function(e){
            if ($(this).is(':checked')){
              $('#id_accept_refund').attr('checked',false)
            }
          })

            $('.password-container').pschecker();

              
          $('input[name=selling_options]').change(function() {
            $('input[name="selling_options"]').attr('checked', false);
            $(this).attr('checked', true);
            
            $('li > input').each(function() {
              $(this).remove();
            });
            if($('input[name=selling_options]:checked').val() == 'no yes' || $('input[name=selling_options]:checked').val() == 'yes yes') {
              $(this).parent().parent().append("<input class='more-details inline txt' type='text' name='more_details' placeholder='Please enter your web address' />");
            } else if($('input[name=selling_options]:checked').val() == 'yes no') {
              $(this).parent().parent().append("<input class='more-details inline txt' type='text' name='more_details' placeholder='Where do you currently sell online?' />");
            }
          });
          if($('input[name=selling_options]:checked').val() == 'no yes' || $('input[name=selling_options]:checked').val() == 'yes yes') {
            $(this).parent().parent().append("<input class='more-details inline txt' type='text' name='more_details' placeholder='Please enter your web address' />");
          } else if($('input[name=selling_options]:checked').val() == 'yes no') {
            $(this).parent().parent().append("<input class='more-details inline txt' type='text' name='more_details' placeholder='Where do you currently sell online?' />");
          }


                  $('#company-information-menu-item').addClass('active-menu');

        $(".quest").click(function() {
            $("#upload_avatar").click();
        });
        $('#avatar-upload-form').ajaxForm(function(data) {
            message = "";
            if(data.result == "ok") {
                $('.retailer-logo').attr('src', data.source);
                message = "Upload Successful!";
            } else {
                message = "There was an error. Please try again!";
            }
            $('#bigform-error').stop();
            $('#bigform-error').animate({
                "opacity" : "1"
            }, "fast", function() {
                changeError($('#bigform-error')[0], message);
                $('#bigform-error').css('display', 'inline');
                $('#bigform-error').delay(2000).fadeOut(1000);
            });
        });
        $('input[type=file]').bind('change', function() {
            var str = "";
            str = $(this).val();
            if(str != "" && str.length > 0) {
                if(str.match(/.*\.(jpg|png|gif)$/)) {
                    $("#avatar-upload-form").submit();
                } else {
                    $('#bigform-error').stop();
                    $('#bigform-error').animate({
                        "opacity" : "1"
                    }, "fast", function() {
                        changeError($('#bigform-error')[0], "Please Upload a valid image!");
                        $('#bigform-error').css('display', 'inline');
                        $('#bigform-error').delay(2000).fadeOut(1000);
                    });
                }
            }
        }).change();

        $('#new_shipping_type').hide();

        $('#others').change(function() {
            if($('#others').is(':checked')) {
                $('#new_shipping_type').fadeIn(500);
            } else {
                $('#new_shipping_type').fadeOut(500);
            }
        });

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

                $('#account-information-menu-item').addClass('active-menu');
        
        // make inline edit
        $('.editable').hide();
  },
  accounts:function(){


    $('#payment-form').validate(PAYMENT_FORM_VALIDATE_OPTIONS)


    $('#shipping-form').submit(function(){
      $(this).find('.submit-button').hide()
      $(this).find('.spinbox').append('<img src="/static/images/loading.gif">')
      submit_shipping_option_form()
      return false;
    })






/*
  THIS IS ALL STYLISTS ACCOUNTS STUFF (SOON TO BE REMOVED HOPEFULLY)
*/

    $('#tester').focus()
            var login_form = $('#mng-account-form');
    
    login_form.ajaxForm({
        url : this.action,
        dataType : 'json',
        success : function(json)
        {
            if (json.success == false && json.errors != undefined)
                process_form_errors(json, login_form)
            else {
                //do something if there aren't errors
                
                window.location.href = "/"; 
            }
        }
    }); 

    

    function hide_form_errors()
    {
        $('.errorlist').remove();
    }

    function process_form_errors(json, form){
        var curField;
        
        hide_form_errors();
        //form.clearForm();
        errors = json.errors;
    
        if (errors.__all__ != undefined)
            form.append(errors.__all__);

        prefix = form.find(":hidden[name='prefix']").val();

        prefix == undefined ? prefix = '' : prefix = prefix + '-';
        $('.error').removeClass('error');
        $('.help-inline').text('');
        for (field in errors) {
            if(errors.hasOwnProperty(field)){
                curField = $('[name=' + field + '], [name=' + field + ']');
                if(curField.attr('type') === 'checkbox'){
                    curField.parent().siblings('.help-inline').text(errors[field][0]);
                } else {
                    curField.siblings('.help-inline').text(errors[field][0]);
                }
                curField.parents('.control-group:first').addClass('error')
            }
        }
      }

        $(".quest").click(function() {
            $("#upload_avatar").click();
        });
        $('#avatar-upload-form').ajaxForm(function(data) {
            message = "";
            console.log(data);
            if(data.result == "ok") {
                $('.acct-avatar').attr('src', data.source);
                $('#avatar-error').css('display', 'none');
                // message = "Upload Successful!";
            } else {
                message = data.error;
                $('#avatar-error').stop();
                $('#avatar-error').animate({
                    "opacity" : "1"
                }, "fast", function() {
                    changeError($('#avatar-error')[0], message);
                    $('#avatar-error').css('display', 'inline');
                });
                // message = "There were errors with your image upload. Please try again!";
            }
        });
        $('#upload_avatar').bind('change', function() {
            var str = "";
            str = $(this).val();
            if(str != "" && str.length > 0) {
                if(str.match(/.*\.(jpg|png|gif)$/)) {
                    $("#avatar-upload-form").submit();
                } else {
                    $('#avatar-error').stop();
                    $('#avatar-error').animate({
                        "opacity" : "1"
                    }, "fast", function() {
                        changeError($('#avatar-error')[0], "Please Upload a valid image!");
                        $('#avatar-error').css('display', 'inline');
                    });
                }
            }
        }).change();
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
        })

    }
/*
  END STYLISTS ACCOUNTS STUFF
*/





    
}




var add_rack_modal_options = {
    afterOpenFunction:init_add_rack_modal
  }

  var item_modal_options = {
    afterOpenFunction:init_item_modal
  }

    
$(document).ready(function() {
    var pageScrLoader = $('body').attr('data-role');
    console.log('page:',pageScrLoader);
    if ( pageScrLoader && stunable[pageScrLoader] ) {
        stunable.common()
        stunable[pageScrLoader]();
        return true;
    } else if ( !pageScrLoader ) {
        return stunable.common.apply( this );
    }else{
        stunable.common();
    }
   //console.log( pageScrLoader + ' does not exist' );
});