
	var add_selected_product_variant_url = undefined;
	
	////console.log(inventories)
	
	function formatPrice(element){
		$e = $(element);
		var d = {
			'onsale':$e.data('onsale'),
			'regprice':$e.data('regprice'),
			'saleprice':$e.data('saleprice')
		};

		if (d.onsale){
			return '<span class="dim"><span class="dollar">$</span><span class="struck">'+
					d.regprice+
					'</span></span><br><span class="sale"><span class="dollar">$</span>'+
					d.saleprice+
					'</span>'
		}else{
			return '<span class="dollar">$</span>'+d.regprice;
		}
	}

function setItemDetailsEvent(){
		//console.log('setItemDetailsEvent')
			$('.item-details .chzn-container').remove();
			$('.item-details #friends-select').css('display', 'block').removeClass('chzn-done').chosen();
			
			$('.item-details .item-size-list span').click(function() {
				if (!$(this).hasClass('selected')) {
					$('.item-details .item-size-list span').removeClass('selected');
					$(this).addClass('selected');
				}
			});
			
			$('.item-details .item-color-list span').click(function() {
				if (!$(this).hasClass('selected')) {
					$('.item-details .item-color-list span').removeClass('selected');
					$(this).addClass('selected');
				}
			});
			
			$('#add-to-cart-link, .buy-now').click(function(e) {
				e.preventDefault();

				if ($('.item-details .item-size-list .selected').length == 0 || $('.item-details .item-color-list .selected').length == 0) {
					alert('Please select size and color');
				} else {

					$.post($('.item-details .item-color-list .selected a').data('href'),function(data){
						$.modal.close()
						var cs = reveal_cart(e,data,true);
					},'html')

				}
			});
		
			$('.item-details .about_retailer').click(aboutDetailsClicked);
				
			$('.item-details .flip').click(function(e){
				e.preventDefault();
				$('.item-details .about_retailer').click();
			});
			
			
			setupRackIt();			
			
			$(".confirmation").hide();
			$('#send_it_to_rack').click(function() {
				if($('#rack_it_form').valid()) {
					$('#loading').show();
					$('#loading').css('display', 'inline');
					$('#loading').css('position', 'relative');
					$('#loading').css('top', '-35px');
					$('#loading').css('left', '190px');
					$.getJSON('/racks/add_item/?' + $('#rack_it_form').serialize(), function(data) {
						$("#rack_confirmation").text(data.result == 'ok' ? "Sent" : "Error").show();
						if(data.result != 'ok') {
							//alert(data.text);
							$('bigform-error').html("");
						} else {
							// 	 fancy box after 2 second on success
							setTimeout($.modal.close(), 2000);
						}
					});
				}
			});
			$('#send_it_to_admirer').click(function() {
				if($('#send_to_admirer_form').valid()) {
					$.getJSON('/racks/sent_to_admirer/?' + $('#send_to_admirer_form').serialize(), function(data) {
						$("#send_item_confirmation").text(data.result == 'ok' ? "Sent" : "Error").show();
						if(data.result != 'ok') {
							//alert(data.text);
							$('#bigform-error').html("");
						} else {
							// close fancy box after 2 second on success
							setTimeout("$.modal.close()", 2000);
						}
					});
				}
			});
			//Fancybox
			///------------------------------------------------------
			//variables
			var itemLink = $('.item-ref'), trash = $('.trash');
	
			// the validation code
			container = $('#bigform-error');
			// validate form on keyup and submit
			validator = $('#send_to_admirer_form').validate({
				errorLabelContainer : container,
				errorElement : 'errorlist',
				invalidHandler : function(form, validator) {
					//display error on submit
					var errors = validator.numberOfInvalids();
					if(errors) {
						if(validator.errorList[0].message) {
							$("#bigform-error p").html("");
							$('#bigform-error').animate({
								"opacity" : "1"
							}, "fast", function() {
								changeError($('#bigform-error')[0], validator.errorList[0].message);
								$('#bigform-error').css('display', 'inline').css('opacy', '1');
							});
							validator.errorList[0].element.focus();
							$(validator.errorList[0].element).addClass('field-error');
						}
					}
				},
				showErrors : function(errorMap, errorList) {
					//display error on blur
					$("#send_to_admirer_form").find("textarea, select").each(function() {
						$(this).removeClass("error");
					});
					$("#bigform-error p").html("");
					if(errorList.length) {
						$('#bigform-error').animate({
							"opacity" : "1"
						}, "fast", function() {
							changeError($('#bigform-error')[0], errorList[0]['message']);
							$('#bigform-error').css('display', 'inline').css('opacy', '1');
						});
						$(errorList[0]['element']).addClass("field-error");
					} else {
						$("#send_to_admirer_form").find("textarea, select").each(function() {
							$(this).removeClass("field-error");
						});
					}
				},
				submitHandler : function(form) {
					$(".field-error").removeClass("field-error");
					form.submit();
				},
				rules : {
					admirer : {
						required : true,
					},
					message : {
						required : true,
					},
				},
				messages : {
					admirer : "Please choose your admirer",
					message : "Please enter your message",
				}
			});
			$('#admirer').blur(function() {
				$('#send_to_admirer_form').validate().element('#admirer');
			});
			$('#message').blur(function() {
				$('#send_to_admirer_form').validate().element('#send_to_admirer_form');
			});
			//send to rack validation
			// the validation code
			container1 = $('#bigform-error1');
			// validate form on keyup and submit
			validator1 = $('#rack_it_form').validate({
				errorLabelContainer : container1,
				errorElement : 'errorlist',
				invalidHandler : function(form, validator1) {
					//display error on submit
					var errors = validator.numberOfInvalids();
					if(errors) {
						if(validator.errorList[0].message) {
							$("#bigform-error1 p").html("");
							$('#bigform-error1').animate({
								"opacity" : "1"
							}, "fast", function() {
								changeError($('#bigform-error1')[0], validator.errorList[0].message);
								$('#bigform-error1').css('display', 'inline').css('opacy', '1');
							});
							validator1.errorList[0].element.focus();
							$(validator1.errorList[0].element).addClass('field-error');
						}
					}
				},
				showErrors : function(errorMap, errorList) {
					//display error on blur
					$("#rack_it_form").find("textarea, select").each(function() {
						$(this).removeClass("error");
					});
					$("#bigform-error1 p").html("");
					if(errorList.length) {
						$('#bigform-error1').animate({
							"opacity" : "1"
						}, "fast", function() {
							changeError($('#bigform-error1')[0], errorList[0]['message']);
							$('#bigform-error1').css('display', 'inline').css('opacy', '1');
						});
						$(errorList[0]['element']).addClass("field-error");
					} else {
						$("#rack_it_form").find("textarea, select").each(function() {
							$(this).removeClass("field-error");
						});
					}
				},
				submitHandler : function(form) {
					$(".field-error").removeClass("field-error");
					form.submit();
				},
				rules : {
					rack : {
						required : true,
					},
				},
				messages : {
					rack : "Please choose your rack",
				}
			});
			$('#rack').blur(function() {
				$('#rack_it_form').validate().element('#rack');
			});
			$('#loading1').hide()
            .ajaxStart(function() {
                $(this).show();
                $('#bigform-error').text("");
                $('.confirmation').hide();
            })
            .ajaxStop(function() {
                $(this).hide();
            });

           
		}

	function aboutDetailsClicked(e){
			var modal_height = $('.modal').height();
			var modal_top = $('.modal').position().top

		//console.log('size',modal_top)
			e.preventDefault();
            var link = $(this);
            var container = link.parents('.item-details');
            e.preventDefault();
           //console.log(link.data('href'))
            $.get(link.data('href'), function(content){
                container.flip({
                    direction:'lr',
                    color: '#FFFFFF',
                    content: content,
                    onEnd: function(){
                        $('.retailer-wrapper .close').click($.modal.close);
                        $('.retailer-wrapper .flip').click(function(){
                            container.flip({
                                direction:'lr',
                                color: '#FFFFFF',
                                content: container.data('flipRevertedSettings').content,
                                onEnd: function(){
                                    setItemDetailsEvent();
                                }
                            });
                        });
                    },
                    onAnimation: function(){
                    	$('#fu').animate({
						    // opacity: 0.25,
						    // left: '+=50',
						    // top:modal_top.toString()+'px'
						    height: (modal_height+23).toString()+'px'
						  }, 250, function() {
    // Animation complete.
  							});
                    }

                });
            });         
        }

function init_inventory_click(){
	$('.item-details .item-color-list span').click(function(e) {
					e.preventDefault();
					if (!$(this).hasClass('selected')) {					
						$('.item-details .item-color-list span').removeClass('selected');
						$(this).addClass('selected');
						$('#modal_item_price').html(formatPrice($(this).find('a')))
					}

					if($(this).find('a').data('image')){
						$('.imgid_'+$(this).find('a').data('image')).click()
					}
					return false;

				});
}

function init_item_modal(){
		$('.spinner').sprite({ fps: 10, no_of_frames: 12 });		
		var added_sizes = [];
		var added_colors = [];
		$('.item-size-list').html('');
		
		
		for(i in inventories) {
			var inventory = inventories[i];
			var selectedclass = '';
			
			if (inventories.length === 1){
				selectedclass=' class="selected"'
				$('.item-color-list').html('');
				// $('.item-color-list').append('<span class="selected"><a href="' + inventories[i].add_cart_url + '" >' + inventories[i].color +"</a></span>");	
			}

			if (added_sizes.indexOf(inventory.size) === -1){
				var el = $("<span"+selectedclass+"><a href='#'>" + inventory.size +"</a></span>")
				if (inventory.is_onsale){
					el.addClass('onsale')
				}
				$('.item-size-list').append(el);
				
				added_sizes.push(inventory.size)
			}
		//console.log(inventory.color)
			if (added_colors.indexOf(inventory.color) === -1){
				var t = "<span"+selectedclass+'><a data-image="'+inventory.imgid+'" data-saleprice="'+inventory.saleprice+'" data-regprice="'+inventory.regularprice+'" data-onsale="'+inventory.is_onsale+'" href="" data-href="' + inventory.add_cart_url + '" >' + inventory.color +'</a></span>'
				var el = $(t)

				if (inventory.is_onsale){
					el.addClass('onsale')
				}
		//console.log('adding ',el)
			$('.item-color-list').append(el);		
				added_colors.push(inventory.color)
			}

			$('.item-size-list span').click(function(e) {
				e.preventDefault();
				$('.item-color-list').html('');
				for(i in inventories) {
					var inventory = inventories[i]
					if (inventories[i].size === $(this).text()) {
						var t = "<span"+selectedclass+'><a data-image="'+inventory.imgid+'" data-saleprice="'+inventories[i].saleprice+'" data-regprice="'+inventories[i].regularprice+'" data-onsale="'+'" href="" data-href="' + inventory.add_cart_url + '" >' + inventory.color +'</a></span>'
						var el = $(t)

						if (inventories[i].is_onsale){
							el.addClass('onsale')
						}
						$('.item-color-list').append(el);				
					}
				}
				init_inventory_click()

				// if ($('.item-color-list').children().length === 1){
					$('.item-color-list').find('span').first().addClass('selected');
					$('#modal_item_price').html(formatPrice($('.item-color-list').find('a')))
				// }

			});
			init_inventory_click();
		}
		
		

		setItemDetailsEvent();
		$('.zoom_this.featured').load(function(){$(this).damonzoom()});
	}
		
	   
	    
	    	    



