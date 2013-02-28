
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
      if (! logged_in &&  $('body').attr('data-role')!='accounts'){
        $('#login_box').modal({clickClose: false,escapeClose:false,showClose:false})

      }

      setupCustomTabs($('#left-panel'));  
      $('.panel-inner-content').html($('.panel-header .active').find('.tab-content').html()).fadeIn(1000, function() {
          // console.log('panel thing just happened')
        });             

      init_refclicks($('.refclick'))
      init_refsubmits($('.refsubmit'))

      $('.cart_slide_trigger').hover(reveal_cart)
      $('.cart_slide_trigger').click(reveal_cart)

      initTouch()

      $('.arbitrary_modal').click(function(e){
        console.log( $($(this).data('target')))
        $($(this).data('target')).modal()
      })

      $('.form_errors').modal()


      $('.address_action').click(function(e){
        var t = $(this);
        if (t.data('val')=='suggested'){
          $('.validated_address_form').submit()
        }else{
        $.modal.close();
        }
      })

    }
    ,shop: function(){            
        setupCarousel($('.iosSlider'));
        initSwipe($('.iosSlider'))
        initDrop(); 
        initRackEvents();
    }
    ,racks: function(){
      // console.log('racks setup')
      initDrop(); 
      initDrag($('.item'))
      initRackEvents();

     

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
                window.location.href = $(this).data('href');
            
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

        $('#zipcode_form').submit(function(e){
          e.preventDefault()
        })

        function update_shipping_handling_fee(event){
          if (event){
            event.preventDefault()
          }
            var field=$('#zipcode_field')
            var zipcode = $('input[name="zipcode"]').val();
            valid_shipping_info = false;                
            if (zipcode.length == 5) {
                $('html').addClass('wait');
                $.ajax({
                    url : field.data('href'),
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
    
      },
      retailers:function(){

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
            $('#terms-continue-btn').attr('href', $(this).data('href')).css('color', 'black').click(function(e){
                if (!$('#terms-input').is(':checked')) {
                    e.preventDefault();
                } 
            });
        })

           $('select[name=image]').ImageSelect(); 
           $('select[name=featured_image]').ImageSelect(); 
           
           $('.imageselector').ImageSelect();

           $('.deetsclick').click(function(){
            console.log(this)
            $(this).closest('.product_row').toggleClass('nodeets')
           })

           $('.select_all').click(function () {
               $($(this).data('target')).attr('checked', this.checked);
           });

           $('.delete-link').click(function(){
                $(this).closest('td').find('.item_selector').attr('checked','checked');
                $('#action_select').val('delete');
                $('.action_submit').submit();
           })

           $('.click_to_expand').click(function(e){
              $(this).parent().toggleClass('collapsed')
              return false
           })

           $('#id_uploaded_zip').change(function(){
            $('.long_process_submit_form').submit(function(){
             $(this).find('.submit_holder').html('<img src="/static/images/gui/loading.gif">');
            })
           })

           try{
           if (updates_in_progress != undefined){
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
                    window.location.href = '/retailers/product_list';
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
                            var $newel = $(json.html)
                            $('.imageselector,  select[name=image], select[name=featured_image]').append($newel)
                            active_image_form.find('.new_image_'+json.message).attr('selected','selected')
                            $('.imageselector,  select[name=image], select[name=featured_image]').ImageSelect('remove');
                            $('.imageselector,  select[name=image], select[name=featured_image]').ImageSelect();
                            $(cln).fadeOut(1000).remove()
                            


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
        // make inline edit
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

      },
      accounts:function(){
        $('#tester').focus()


          //         // the validation code
          //     container = $('#bigform-error1');
          //     // validate form on keyup and submit
          //     validator = $('#waitlist-form').validate({
          //       errorLabelContainer : container,
          //       //errorClass : 'field-error',
          //       errorElement : 'errorlist',
          //       invalidHandler : function(form, validator) {
          //         //display error on submit
          //         var errors = validator.numberOfInvalids();
          //         if(errors) {
          //           if(validator.errorList[0].message) {
          //             $('#bigform-error1').text = "";
          //             $('#bigform-error1').animate({
          //               "opacity" : "1"
          //             }, "fast", function() {
          //               changeError($('#bigform-error1')[0], validator.errorList[0].message);
          //               $('#bigform-error1').css('display', 'inline').css('opacy', '1');
          //             });
          //             validator.errorList[0].element.focus();
          //             $(validator.errorList[0].element).addClass('field-error');
          //           }
          //         }
          //       },
          //       showErrors : function(errorMap, errorList) {
          //         //display error on blur
          //         $("#waitlist-form'").find("input").each(function() {
          //           $(this).removeClass("error");
          //         });
          //         $("#bigform-error1").html("");
          //         if(errorList.length) {
          //           $('#bigform-error1').animate({
          //             "opacity" : "1"
          //           }, "fast", function() {
          //             changeError($('#bigform-error1')[0], errorList[0]['message']);
          //             $('#bigform-error1').css('display', 'inline').css('opacy', '1');
          //           });
          //           $(errorList[0]['element']).addClass("field-error");
          //         } else {
          //           $("#waitlist-form").find("input").each(function() {
          //             $(this).removeClass("field-error");
          //           });
          //         }
          //       },
          //       submitHandler : function(form) {
          //         $(".field-error").removeClass("field-error");
          //         form.submit();
          //       },
          //       rules : {
          //         email : {
          //           required : true,
          //           email : true
          //         },
          //       },
          //       messages : {
          //         email : "Stella can't reach you there",
          //       }
          //     });
          }


}


    
$(document).ready(function() {
    var pageScrLoader = $('body').attr('data-role');
   console.log('page:',pageScrLoader)
    if ( pageScrLoader && stunable[pageScrLoader] ) {
        return stunable[pageScrLoader].apply( this, stunable.common());
    } else if ( !pageScrLoader ) {
        return stunable.common.apply( this );
    }else{
        stunable.common();
    }
   //console.log( pageScrLoader + ' does not exist' );
});