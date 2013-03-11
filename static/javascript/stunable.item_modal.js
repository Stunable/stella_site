
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
		console.log('setItemDetailsEvent')
			
			$('.modal-item-details #variation_choices span').click(function() {	
				$(this).siblings().removeClass('selected');
				$(this).addClass('selected');
				
				var target_spans=$('.'+$(this).data('name')),
					variations_to_hide = $(this).data('target');

				if (! $(variations_to_hide+'.selected').hasClass($(this).data('name'))){
					$(variations_to_hide+'.selected').removeClass('selected')
				}
				
				$(variations_to_hide).hide();
				target_spans.show();

			});
			
			// $('.modal-item-details .item-color-list span').click(function() {
			// 	if (!$(this).hasClass('selected')) {
			// 		$('.modal-item-details .item-color-list span').removeClass('selected');
			// 		$(this).addClass('selected');
			// 	}
			// 	$('.click_to_cart').data('href',$(this).data('href'))
			// });

			$('#add-to-cart-link, .buy-now, #add-to-wishlist-link').click(function(e) {

				e.preventDefault();

				if (($('.modal-item-details .item-size-list .selected').length == 0 || $('.modal-item-details .item-color-list .selected').length == 0)
					&& !$(this).data('href')) { //IF this is a wishlist modal window, we already know the variation to add to cart
					alert('Please select size and color');
				} else {
					console.log($(this));
					$.post($(this).data('href'),function(data){
						$.modal.close()
						var cs = reveal_cart(e,data,true);
					},'html')

				}
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
		
		
		// for(i in inventories) {
		// 	var inventory = inventories[i];
		// 	var selectedclass = '';
			
		// 	if (inventories.length === 1){
		// 		selectedclass=' class="selected"'
		// 		$('.item-color-list').html('');
		// 		// $('.item-color-list').append('<span class="selected"><a href="' + inventories[i].add_cart_url + '" >' + inventories[i].color +"</a></span>");	
		// 	}

		// 	if (added_sizes.indexOf(inventory.size) === -1){
		// 		var el = $("<span"+selectedclass+"><a href='#'>" + inventory.size +"</a></span>")
		// 		if (inventory.is_onsale){
		// 			el.addClass('onsale')
		// 		}
		// 		$('.item-size-list').append(el);
				
		// 		added_sizes.push(inventory.size)
		// 	}
		// //console.log(inventory.color)
		// 	if (added_colors.indexOf(inventory.color) === -1){
		// 		var t = "<span"+selectedclass+'><a data-image="'+inventory.imgid+'" data-saleprice="'+inventory.saleprice+'" data-regprice="'+inventory.regularprice+'" data-onsale="'+inventory.is_onsale+'" href="" data-href="' + inventory.add_cart_url + '" >' + inventory.color +'</a></span>'
		// 		var el = $(t)

		// 		if (inventory.is_onsale){
		// 			el.addClass('onsale')
		// 		}
		// //console.log('adding ',el)
		// 	$('.item-color-list').append(el);		
		// 		added_colors.push(inventory.color)
		// 	}

		// 	$('.item-size-list span').click(function(e) {
		// 		e.preventDefault();
		// 		$('.item-color-list').html('');
		// 		for(i in inventories) {
		// 			var inventory = inventories[i]
		// 			if (inventories[i].size === $(this).text()) {
		// 				var t = '<span id="'+inventory.id+'" '+selectedclass+'><a data-image="'+inventory.imgid+'" data-saleprice="'+inventories[i].saleprice+'" data-regprice="'+inventories[i].regularprice+'" data-onsale="'+'" href="" data-href="' + inventory.add_cart_url + '" >' + inventory.color +'</a></span>'
		// 				var el = $(t)

		// 				if (inventories[i].is_onsale){
		// 					el.addClass('onsale')
		// 				}
		// 				$('.item-color-list').append(el);				
		// 			}
		// 		}

		// 		// if ($('.item-color-list').children().length === 1){
		// 			$('.item-color-list').find('span').first().addClass('selected');
		// 			$('#modal_item_price').html(formatPrice($('.item-color-list').find('a')))
		// 		// }

		// 	});
			
		// }

		
		init_refclicks($('.refclick'))
		

		setItemDetailsEvent();

		$('.zoom_this.featured').load(function(){$(this).damonzoom()});

		$('#retailer-header .modalitem').textfill(25)
		$('#retailer-header .retailer').textfill(40)
	}
		
	   
	    
	    	    



