
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
		// console.log('setItemDetailsEvent')
			
			$('.modal-item-details #variation_choices span').click(function(e) {	
				$(this).siblings().removeClass('selected');
				$(this).addClass('selected');
				
				var target_spans=$('.'+$(this).data('name')),
					variations_to_hide = $(this).data('target');

				if (! $(variations_to_hide+'.selected').hasClass($(this).data('name'))){
					$(variations_to_hide+'.selected').removeClass('selected')
				}
				
				$(variations_to_hide).hide();
				target_spans.show();


				var selsize = $('.item-size-list span.selected'),
					selcolor = $('.item-color-list span.selected'),
					variation = $('.'+selsize.data('name')+'.'+selcolor.data('name'))

				if (!variation.length){
					target_spans.first().click()
					return false;
				}

				if(variation.data('imagetarget')){
					$('.item-pictures '+variation.data('imagetarget')).click();
				}

				$('#item-header .item-price').html('<span class="">'+variation.data('size')+'</span>'+',<span class="">'+variation.data('name')+' - </span>' + '<span class="dollar">$</span>'+'<span class="">'+variation.data('price')+'</span>');

			});
			
			$('#add-to-cart-link, .buy-now, #add-to-wishlist-link').click(function(e) {

				e.preventDefault();

				var $t = $(this)

				if ($('.item-size-list span.selected').length && $('.item-color-list span.selected').length ){
					var selsize = $('.item-size-list span.selected'),
						selcolor = $('.item-color-list span.selected');

					var variation_id = $('.'+selsize.data('name')+'.'+selcolor.data('name')).val();

					$.post($(this).data('href')+variation_id,function(data){
					
						$.modal.close()
						$('body').append($(data).hide().fadeIn());
						// $('body').append(data)

						setTimeout(function(){$('.cart_item_added').fadeOut()},4000);

						if ($t.hasClass('cart')){
							cart_item_added();
						}else{
							wishlist_item_added();
						}

					},'html')
				}

				return false;			
			});

		}

	function aboutDetailsClicked(e){
			var modal_height = $('.modal').height();
			var modal_top = $('.modal').position().top

		//console.log('size',modal_top)
			e.preventDefault();
            var link = $(this);
            var container = link.parents('.modal-item-details');
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



function init_item_modal(){
		
		init_refclicks($('.refclick'))
		
		setItemDetailsEvent();

		$('.zoom .zoom_this.featured').load(function(){$(this).damonzoom()

			$('.text-fill').textfill()
		});

		$('.modal-item-details .item-pictures img').click(function(e){

			if($(this).hasClass('active')){
				return false;
			}
			
			$(this).siblings().removeClass('active');
			$(this).addClass('active');


			var target_img  = $('.item-visuals').find($(this).data('target'));

			if (!target_img.attr('src')){
				target_img.attr('src',target_img.data('src')).load(function(){
					// $('body').append(this);
					$('.damonzoomcontainer').hide();
					$(this).parent().fadeIn();
					// $(this).damonzoom();
					$('.item-visuals .active-image').fadeOut();
					$('.active-image').removeClass('active-image');
					$(this).parent().addClass('active-image');
					$('.zoom .active-image .zoom_this').damonzoom()
					
				});
			}else{
				$('.damonzoomcontainer').hide();
				$(target_img).parent().fadeIn();
				// $(target_img).damonzoom();
				$('.item-visuals .active-image').fadeOut();
				$('.active-image').removeClass('active-image');
				$(target_img).parent().addClass('active-image');
				$('.zoom .active-image .zoom_this').damonzoom()

			}
			
		})
	
		if ($('.item-color-list span').length < 2){
			$('.item-color-list span').first().click();
		}
		// $('#item-header .modalitem').textfill(25)

		$('.share_click').click(function(e){
			e.preventDefault();
			$(this).find('.share_floater').show();
			$(this).find('input').focus().select()

			$('.modal').click(function(e){
				$('.share_floater').fadeOut();
			})

			return false;
		})
		
	}
		
	   
	    
	    	    



