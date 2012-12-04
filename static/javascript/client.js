// JavaScript Document
///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
/*
* jQuery Easing v1.3 - http://gsgd.co.uk/sandbox/jquery/easing/
* Uses the built in easing capabilities added In jQuery 1.1
* to offer multiple easing options
* TERMS OF USE - jQuery Easing
* Open source under the BSD License.
* Copyright Â© 2008 George McGinley Smith
* All rights reserved.
*/

// t: current time, b: begInnIng value, c: change In value, d: duration
eval( function(p, a, c, k, e, r) {
	e = function(c) {
		return (c < a ? '' : e(parseInt(c / a))) + (( c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
	};
	if(!''.replace(/^/, String)) {
		while(c--)
		r[e(c)] = k[c] || e(c);
		k = [
		function(e) {
			return r[e]
		}];

		e = function() {
			return '\\w+'
		};
		c = 1
	};
	while(c--)
	if(k[c])
		p = p.replace(new RegExp('\\b' + e(c) + '\\b', 'g'), k[c]);
	return p
}('h.i[\'1a\']=h.i[\'z\'];h.O(h.i,{y:\'D\',z:9(x,t,b,c,d){6 h.i[h.i.y](x,t,b,c,d)},17:9(x,t,b,c,d){6 c*(t/=d)*t+b},D:9(x,t,b,c,d){6-c*(t/=d)*(t-2)+b},13:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t+b;6-c/2*((--t)*(t-2)-1)+b},X:9(x,t,b,c,d){6 c*(t/=d)*t*t+b},U:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t+1)+b},R:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t+b;6 c/2*((t-=2)*t*t+2)+b},N:9(x,t,b,c,d){6 c*(t/=d)*t*t*t+b},M:9(x,t,b,c,d){6-c*((t=t/d-1)*t*t*t-1)+b},L:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t+b;6-c/2*((t-=2)*t*t*t-2)+b},K:9(x,t,b,c,d){6 c*(t/=d)*t*t*t*t+b},J:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t*t*t+1)+b},I:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t*t+b;6 c/2*((t-=2)*t*t*t*t+2)+b},G:9(x,t,b,c,d){6-c*8.C(t/d*(8.g/2))+c+b},15:9(x,t,b,c,d){6 c*8.n(t/d*(8.g/2))+b},12:9(x,t,b,c,d){6-c/2*(8.C(8.g*t/d)-1)+b},Z:9(x,t,b,c,d){6(t==0)?b:c*8.j(2,10*(t/d-1))+b},Y:9(x,t,b,c,d){6(t==d)?b+c:c*(-8.j(2,-10*t/d)+1)+b},W:9(x,t,b,c,d){e(t==0)6 b;e(t==d)6 b+c;e((t/=d/2)<1)6 c/2*8.j(2,10*(t-1))+b;6 c/2*(-8.j(2,-10*--t)+2)+b},V:9(x,t,b,c,d){6-c*(8.o(1-(t/=d)*t)-1)+b},S:9(x,t,b,c,d){6 c*8.o(1-(t=t/d-1)*t)+b},Q:9(x,t,b,c,d){e((t/=d/2)<1)6-c/2*(8.o(1-t*t)-1)+b;6 c/2*(8.o(1-(t-=2)*t)+1)+b},P:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6-(a*8.j(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b},H:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6 a*8.j(2,-10*t)*8.n((t*d-s)*(2*8.g)/p)+c+b},T:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d/2)==2)6 b+c;e(!p)p=d*(.3*1.5);e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);e(t<1)6-.5*(a*8.j(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b;6 a*8.j(2,-10*(t-=1))*8.n((t*d-s)*(2*8.g)/p)*.5+c+b},F:9(x,t,b,c,d,s){e(s==u)s=1.l;6 c*(t/=d)*t*((s+1)*t-s)+b},E:9(x,t,b,c,d,s){e(s==u)s=1.l;6 c*((t=t/d-1)*t*((s+1)*t+s)+1)+b},16:9(x,t,b,c,d,s){e(s==u)s=1.l;e((t/=d/2)<1)6 c/2*(t*t*(((s*=(1.B))+1)*t-s))+b;6 c/2*((t-=2)*t*(((s*=(1.B))+1)*t+s)+2)+b},A:9(x,t,b,c,d){6 c-h.i.v(x,d-t,0,c,d)+b},v:9(x,t,b,c,d){e((t/=d)<(1/2.k)){6 c*(7.q*t*t)+b}m e(t<(2/2.k)){6 c*(7.q*(t-=(1.5/2.k))*t+.k)+b}m e(t<(2.5/2.k)){6 c*(7.q*(t-=(2.14/2.k))*t+.11)+b}m{6 c*(7.q*(t-=(2.18/2.k))*t+.19)+b}},1b:9(x,t,b,c,d){e(t<d/2)6 h.i.A(x,t*2,0,c,d)*.5+b;6 h.i.v(x,t*2-d,0,c,d)*.5+c*.5+b}});', 62, 74, '||||||return||Math|function|||||if|var|PI|jQuery|easing|pow|75|70158|else|sin|sqrt||5625|asin|||undefined|easeOutBounce|abs||def|swing|easeInBounce|525|cos|easeOutQuad|easeOutBack|easeInBack|easeInSine|easeOutElastic|easeInOutQuint|easeOutQuint|easeInQuint|easeInOutQuart|easeOutQuart|easeInQuart|extend|easeInElastic|easeInOutCirc|easeInOutCubic|easeOutCirc|easeInOutElastic|easeOutCubic|easeInCirc|easeInOutExpo|easeInCubic|easeOutExpo|easeInExpo||9375|easeInOutSine|easeInOutQuad|25|easeOutSine|easeInOutBack|easeInQuad|625|984375|jswing|easeInOutBounce'.split('|'), 0, {}));
//---------------------

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Text input field populators
//this.focus(function(){});

// CLEAR TEXT INPUTS OF DEFAULT VALUE ON FOCUS
function clearInput(textField) {
	if(textField.value == textField.defaultValue) {
		textField.value = "";
	}
}

// RESTORE TEXT INPUT DEFAULT VALUE ON BLUR
function restoreInput(textField) {
	if(textField.value == "" || isEmpty(textField.value)) {
		textField.value = textField.defaultValue;
	}
}

function isEmpty(tarString) {
	var blanks = /^\s*$/
	if(blanks.test(tarString)) {
		return true;
	}
	return false;
}

function isDefault(textField) {
	if(textField.value == textField.defaultValue) {
		return true;
	}
	return false;
}

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
// MAKE SELECT BOXES (DROP-DOWNS) PRETTY

(
	function($) {
		$.fn.extend({
			customStyle : function(options) {
				if(!$.browser.msie || ($.browser.msie && $.browser.version > 6)) {
					return this.each(function() {
						var currentSelected = $(this).find(':selected');
						$(this).after('<span class="customStyleSelectBox"><span class="customStyleSelectBoxInner">' + currentSelected.text() + '</span></span>').css({
							position : 'absolute',
							opacity : 0,
							fontSize : '0.86em'
						});
						var selectBoxSpan = $(this).next();
						var selectBoxWidth = parseInt($(this).width()) - parseInt(selectBoxSpan.css('padding-left')) - parseInt(selectBoxSpan.css('padding-right'));
						var selectBoxSpanInner = selectBoxSpan.find(':first-child');
						selectBoxSpan.css({
							display : 'inline-block'
						});
						selectBoxSpanInner.css({
							width : '211px',
							display : 'inline-block'
						});
						var selectBoxHeight = parseInt(selectBoxSpan.height()) + parseInt(selectBoxSpan.css('padding-top')) + parseInt(selectBoxSpan.css('padding-bottom'));
						$(this).height(selectBoxHeight).change(function() {
							selectBoxSpanInner.text($(this).find(':selected').text()).parent().addClass('changed');
						});
					});
				}
			}
		});

		//drop down box initializer
		//$('select.styled').customStyle();

	})(jQuery);

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

/*
* FancyBox - jQuery Plugin
* Simple and fancy lightbox alternative
*
* Examples and documentation at: http://fancybox.net
*
* Copyright (c) 2008 - 2010 Janis Skarnelis
* That said, it is hardly a one-person project. Many people have submitted bugs, code, and offered their advice freely. Their support is greatly appreciated.
*
* Version: 1.3.4 (11/11/2010)
* Requires: jQuery v1.3+
*
* Dual licensed under the MIT and GPL licenses:
*   http://www.opensource.org/licenses/mit-license.php
*   http://www.gnu.org/licenses/gpl.html
*/
;(function($) {
	var tmp, loading, overlay, wrap, outer, content, close, title, nav_left, nav_right, selectedIndex = 0, selectedOpts = {}, selectedArray = [], currentIndex = 0, currentOpts = {}, currentArray = [], ajaxLoader = null, imgPreloader = new Image(), imgRegExp = /\.(jpg|gif|png|bmp|jpeg)(.*)?$/i, swfRegExp = /[^\.]\.(swf)\s*$/i, loadingTimer, loadingFrame = 1, titleHeight = 0, titleStr = '', start_pos, final_pos, busy = false, fx = $.extend($('<div/>')[0], {
		prop : 0
	}), isIE6 = $.browser.msie && $.browser.version < 7 && !window.XMLHttpRequest, _abort = function() {
		loading.hide();
		imgPreloader.onerror = imgPreloader.onload = null;
		if(ajaxLoader) {
			ajaxLoader.abort()
		}
		tmp.empty()
	}, _error = function() {
		if(false === selectedOpts.onError(selectedArray, selectedIndex, selectedOpts)) {
			loading.hide();
			busy = false;
			return
		}
		selectedOpts.titleShow = false;
		selectedOpts.width = 'auto';
		selectedOpts.height = 'auto';
		tmp.html('<p id="fancybox-error">The requested content cannot be loaded.<br />Please try again later.</p>');
		_process_inline()
	}, _start = function() {
		var obj = selectedArray[selectedIndex], href, type, title, str, emb, ret;
		_abort();
		selectedOpts = $.extend({}, $.fn.fancybox.defaults, ( typeof $(obj).data('fancybox') == 'undefined' ? selectedOpts : $(obj).data('fancybox')));
		ret = selectedOpts.onStart(selectedArray, selectedIndex, selectedOpts);
		if(ret === false) {
			busy = false;
			return
		} else if( typeof ret == 'object') {
			selectedOpts = $.extend(selectedOpts, ret)
		}
		title = selectedOpts.title || (obj.nodeName ? $(obj).attr('title') : obj.title) || '';
		if(obj.nodeName && !selectedOpts.orig) {
			selectedOpts.orig = $(obj).children("img:first").length ? $(obj).children("img:first") : $(obj)
		}
		if(title === '' && selectedOpts.orig && selectedOpts.titleFromAlt) {
			title = selectedOpts.orig.attr('alt')
		}
		href = selectedOpts.href || (obj.nodeName ? $(obj).attr('href') : obj.href) || null;
		if((/^(?:javascript)/i).test(href) || href == '#') {
			href = null
		}
		if(selectedOpts.type) {
			type = selectedOpts.type;
			if(!href) {
				href = selectedOpts.content
			}
		} else if(selectedOpts.content) {
			type = 'html'
		} else if(href) {
			if(href.match(imgRegExp)) {
				type = 'image'
			} else if(href.match(swfRegExp)) {
				type = 'swf'
			} else if($(obj).hasClass("iframe")) {
				type = 'iframe'
			} else if(href.indexOf("#") === 0) {
				type = 'inline'
			} else {
				type = 'ajax'
			}
		}
		if(!type) {
			_error();
			return
		}
		if(type == 'inline') {
			obj = href.substr(href.indexOf("#"));
			type = $(obj).length > 0 ? 'inline' : 'ajax'
		}
		selectedOpts.type = type;
		selectedOpts.href = href;
		selectedOpts.title = title;
		if(selectedOpts.autoDimensions) {
			if(selectedOpts.type == 'html' || selectedOpts.type == 'inline' || selectedOpts.type == 'ajax') {
				selectedOpts.width = 'auto';
				selectedOpts.height = 'auto'
			} else {
				selectedOpts.autoDimensions = false
			}
		}
		if(selectedOpts.modal) {
			selectedOpts.overlayShow = true;
			selectedOpts.hideOnOverlayClick = false;
			selectedOpts.hideOnContentClick = false;
			selectedOpts.enableEscapeButton = false;
			selectedOpts.showCloseButton = false
		}
		selectedOpts.padding = parseInt(selectedOpts.padding, 10);
		selectedOpts.margin = parseInt(selectedOpts.margin, 10);
		tmp.css('padding', (selectedOpts.padding + selectedOpts.margin));
		$('.fancybox-inline-tmp').unbind('fancybox-cancel').bind('fancybox-change', function() {
			$(this).replaceWith(content.children())
		});
		switch(type) {
			case'html':
				tmp.html(selectedOpts.content);
				_process_inline();
				break;
			case'inline':
				if($(obj).parent().is('#fancybox-content') === true) {
					busy = false;
					return
				}
				$('<div class="fancybox-inline-tmp" />').hide().insertBefore($(obj)).bind('fancybox-cleanup', function() {
					$(this).replaceWith(content.children())
				}).bind('fancybox-cancel', function() {
					$(this).replaceWith(tmp.children())
				});
				$(obj).appendTo(tmp);
				_process_inline();
				break;
			case'image':
				busy = false;
				$.fancybox.showActivity();
				imgPreloader = new Image();
				imgPreloader.onerror = function() {
					_error()
				};
				imgPreloader.onload = function() {
					busy = true;
					imgPreloader.onerror = imgPreloader.onload = null;
					_process_image()
				};
				imgPreloader.src = href;
				break;
			case'swf':
				selectedOpts.scrolling = 'no';
				str = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="' + selectedOpts.width + '" height="' + selectedOpts.height + '"><param name="movie" value="' + href + '"></param>';
				emb = '';
				$.each(selectedOpts.swf, function(name, val) {
					str += '<param name="' + name + '" value="' + val + '"></param>';
					emb += ' ' + name + '="' + val + '"'
				});
				str += '<embed src="' + href + '" type="application/x-shockwave-flash" width="' + selectedOpts.width + '" height="' + selectedOpts.height + '"' + emb + '></embed></object>';
				tmp.html(str);
				_process_inline();
				break;
			case'ajax':
				busy = false;
				$.fancybox.showActivity();
				selectedOpts.ajax.win = selectedOpts.ajax.success;
				ajaxLoader = $.ajax($.extend({}, selectedOpts.ajax, {
					url : href,
					data : selectedOpts.ajax.data || {},
					error : function(XMLHttpRequest, textStatus, errorThrown) {
						if(XMLHttpRequest.status > 0) {
							_error()
						}
					},
					success : function(data, textStatus, XMLHttpRequest) {
						var o = typeof XMLHttpRequest == 'object' ? XMLHttpRequest : ajaxLoader;
						if(o.status == 200) {
							if( typeof selectedOpts.ajax.win == 'function') {
								ret = selectedOpts.ajax.win(href, data, textStatus, XMLHttpRequest);
								if(ret === false) {
									loading.hide();
									return
								} else if( typeof ret == 'string' || typeof ret == 'object') {
									data = ret
								}
							}
							tmp.html(data);
							_process_inline()
						}
					}
				}));
				break;
			case'iframe':
				_show();
				break
		}
	}, _process_inline = function() {
		var w = selectedOpts.width, h = selectedOpts.height;
		if(w.toString().indexOf('%') > -1) {
			w = parseInt(($(window).width() - (selectedOpts.margin * 2)) * parseFloat(w) / 100, 10) + 'px'
		} else {
			w = w == 'auto' ? 'auto' : w + 'px'
		}
		if(h.toString().indexOf('%') > -1) {
			h = parseInt(($(window).height() - (selectedOpts.margin * 2)) * parseFloat(h) / 100, 10) + 'px'
		} else {
			h = h == 'auto' ? 'auto' : h + 'px'
		}
		selectedOpts.width = tmp.width();
		selectedOpts.height = tmp.height();
		_show()
	}, _process_image = function() {
		selectedOpts.width = imgPreloader.width;
		selectedOpts.height = imgPreloader.height;
		$("<img />").attr({
			'id' : 'fancybox-img',
			'src' : imgPreloader.src,
			'alt' : selectedOpts.title
		}).appendTo(tmp);
		_show()
	}, _show = function() {
		var pos, equal;
		loading.hide();
		if(wrap.is(":visible") && false === currentOpts.onCleanup(currentArray, currentIndex, currentOpts)) {
			$.event.trigger('fancybox-cancel');
			busy = false;
			return
		}
		busy = true;
		$(content.add(overlay)).unbind();
		$(window).unbind("resize.fb scroll.fb");
		$(document).unbind('keydown.fb');
		if(wrap.is(":visible") && currentOpts.titlePosition !== 'outside') {
			wrap.css('height', wrap.height())
		}
		currentArray = selectedArray;
		currentIndex = selectedIndex;
		currentOpts = selectedOpts;
		if(currentOpts.overlayShow) {
			overlay.css({
				'background-color' : currentOpts.overlayColor,
				'opacity' : currentOpts.overlayOpacity,
				'cursor' : currentOpts.hideOnOverlayClick ? 'pointer' : 'auto',
				'height' : $(document).height(),
				'position' : 'fixed'
			});
			if(!overlay.is(':visible')) {
				if(isIE6) {
					$('select:not(#fancybox-tmp select)').filter(function() {
						return this.style.visibility !== 'hidden'
					}).css({
						'visibility' : 'hidden'
					}).one('fancybox-cleanup', function() {
						this.style.visibility = 'inherit'
					})
				}
				overlay.show()
			}
		} else {
			overlay.hide()
		}
		final_pos = _get_zoom_to();
		_process_title();
		if(wrap.is(":visible")) {
			$(close.add(nav_left).add(nav_right)).hide();
			pos = wrap.position(), start_pos = {
				top : pos.top,
				left : pos.left,
				width : wrap.width(),
				height : wrap.height()
			};
			equal = (start_pos.width == final_pos.width && start_pos.height == final_pos.height);
			content.fadeTo(currentOpts.changeFade, 0.3, function() {
				var finish_resizing = function() {
					content.html(tmp.contents()).fadeTo(currentOpts.changeFade, 1, _finish)
				};
				$.event.trigger('fancybox-change');
				content.empty().removeAttr('filter').css({
					'border-width' : currentOpts.padding,
					'width' : final_pos.width - currentOpts.padding * 2,
					'height' : selectedOpts.autoDimensions ? 'auto' : final_pos.height - titleHeight - currentOpts.padding * 2
				});
				if(equal) {
					finish_resizing()
				} else {
					fx.prop = 0;
					$(fx).animate({
						prop : 1
					}, {
						duration : currentOpts.changeSpeed,
						easing : currentOpts.easingChange,
						step : _draw,
						complete : finish_resizing
					})
				}
			});
			return
		}
		wrap.removeAttr("style");
		content.css('border-width', 0);
		if(currentOpts.transitionIn == 'elastic') {
			start_pos = _get_zoom_from();
			content.html(tmp.contents());
			wrap.show();
			if(currentOpts.opacity) {
				final_pos.opacity = 0
			}
			fx.prop = 0;
			
			/*************** New animation *****************/
			final_pos.top -= 600;
			final_pos.opacity = 0;
			wrap.css(final_pos);
			final_pos.top += 600;
			wrap.show();
			content.css({
					'width' : final_pos.width - currentOpts.padding * 2,
					'height' : final_pos.height - (titleHeight * 1) - currentOpts.padding * 2
			});
			
			overlay.fadeIn('fast', function() {
				$('#fancybox-wrap').transition({ y: '+600px', opacity: 1, easing: 'ease-out', duration: 500}, 
					function() {
						_finish();

					} 
				);
			});
			
			/*************** End New animation *****************/
			
			// $(fx).animate({
				// prop : 1
			// }, {
				// duration : currentOpts.speedIn,
				// easing : currentOpts.easingIn,
				// step : _draw,
				// complete : _finish
			// });
			return
		}
		if(currentOpts.titlePosition == 'inside' && titleHeight > 0) {
			title.show()
		}
		content.css({
			'width' : final_pos.width - currentOpts.padding * 2,
			'height' : selectedOpts.autoDimensions ? 'auto' : final_pos.height - titleHeight - currentOpts.padding * 2
		}).html(tmp.contents());
		wrap.css(final_pos).fadeIn(currentOpts.transitionIn == 'none' ? 0 : currentOpts.speedIn, _finish)
	}, _format_title = function(title) {
		if(title && title.length) {
			if(currentOpts.titlePosition == 'float') {
				return '<table id="fancybox-title-float-wrap" cellpadding="0" cellspacing="0"><tr><td id="fancybox-title-float-left"></td><td id="fancybox-title-float-main">' + title + '</td><td id="fancybox-title-float-right"></td></tr></table>'
			}
			return '<div id="fancybox-title-' + currentOpts.titlePosition + '">' + title + '</div>'
		}
		return false
	}, _process_title = function() {
		titleStr = currentOpts.title || '';
		titleHeight = 0;
		title.empty().removeAttr('style').removeClass();
		if(currentOpts.titleShow === false) {
			title.hide();
			return
		}
		titleStr = $.isFunction(currentOpts.titleFormat) ? currentOpts.titleFormat(titleStr, currentArray, currentIndex, currentOpts) : _format_title(titleStr);
		if(!titleStr || titleStr === '') {
			title.hide();
			return
		}
		title.addClass('fancybox-title-' + currentOpts.titlePosition).html(titleStr).appendTo('body').show();
		switch(currentOpts.titlePosition) {
			case'inside':
				title.css({
					'width' : final_pos.width - (currentOpts.padding * 2),
					'marginLeft' : currentOpts.padding,
					'marginRight' : currentOpts.padding
				});
				titleHeight = title.outerHeight(true);
				title.appendTo(outer);
				final_pos.height += titleHeight;
				break;
			case'over':
				title.css({
					'marginLeft' : currentOpts.padding,
					'width' : final_pos.width - (currentOpts.padding * 2),
					'bottom' : currentOpts.padding
				}).appendTo(outer);
				break;
			case'float':
				title.css('left', parseInt((title.width() - final_pos.width - 40) / 2, 10) * -1).appendTo(wrap);
				break;
			default:
				title.css({
					'width' : final_pos.width - (currentOpts.padding * 2),
					'paddingLeft' : currentOpts.padding,
					'paddingRight' : currentOpts.padding
				}).appendTo(wrap);
				break
		}
		title.hide()
	}, _set_navigation = function() {
		if(currentOpts.enableEscapeButton || currentOpts.enableKeyboardNav) {
			$(document).bind('keydown.fb', function(e) {
				if(e.keyCode == 27 && currentOpts.enableEscapeButton) {
					e.preventDefault();
					$.fancybox.close()
				} else if((e.keyCode == 37 || e.keyCode == 39) && currentOpts.enableKeyboardNav && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA' && e.target.tagName !== 'SELECT') {
					e.preventDefault();
					$.fancybox[e.keyCode==37?'prev':'next']()
				}
			})
		}
		if(!currentOpts.showNavArrows) {
			nav_left.hide();
			nav_right.hide();
			return
		}
		if((currentOpts.cyclic && currentArray.length > 1) || currentIndex !== 0) {
			nav_left.show()
		}
		if((currentOpts.cyclic && currentArray.length > 1) || currentIndex != (currentArray.length - 1)) {
			nav_right.show()
		}
	}, _finish = function() {
		if(!$.support.opacity) {
			content.get(0).style.removeAttribute('filter');
			wrap.get(0).style.removeAttribute('filter')
		}
		if(selectedOpts.autoDimensions) {
			content.css('height', 'auto')
		}
		wrap.css('height', 'auto');
		if(titleStr && titleStr.length) {
			title.show()
		}
		if(currentOpts.showCloseButton) {
			close.show()
		}
		_set_navigation();
		if(currentOpts.hideOnContentClick) {
			content.bind('click', $.fancybox.close)
		}
		if(currentOpts.hideOnOverlayClick) {
			overlay.bind('click', $.fancybox.close)
		}
		$(window).bind("resize.fb", $.fancybox.resize);
		if(currentOpts.centerOnScroll) {
			$(window).bind("scroll.fb", $.fancybox.center)
		}
		if(currentOpts.type == 'iframe') {
			$('<iframe id="fancybox-frame" name="fancybox-frame' + new Date().getTime() + '" frameborder="0" hspace="0" ' + ($.browser.msie ? 'allowtransparency="true""' : '') + ' scrolling="' + selectedOpts.scrolling + '" src="' + currentOpts.href + '"></iframe>').appendTo(content)
		}
		wrap.show();
		busy = false;
		$.fancybox.center();
		currentOpts.onComplete(currentArray, currentIndex, currentOpts);
		_preload_images()
	}, _preload_images = function() {
		var href, objNext;
		if((currentArray.length - 1) > currentIndex) {
			href = currentArray[currentIndex + 1].href;
			if( typeof href !== 'undefined' && href.match(imgRegExp)) {
				objNext = new Image();
				objNext.src = href
			}
		}
		if(currentIndex > 0) {
			href = currentArray[currentIndex - 1].href;
			if( typeof href !== 'undefined' && href.match(imgRegExp)) {
				objNext = new Image();
				objNext.src = href
			}
		}
	}, _draw = function(pos) {
		var dim = {
			width : parseInt(start_pos.width + (final_pos.width - start_pos.width) * pos, 10),
			height : parseInt(start_pos.height + (final_pos.height - start_pos.height) * pos, 10),
			top : parseInt(start_pos.top + (final_pos.top - start_pos.top) * pos, 10),
			left : parseInt(start_pos.left + (final_pos.left - start_pos.left) * pos, 10)
		};
		if( typeof final_pos.opacity !== 'undefined') {
			dim.opacity = pos < 0.5 ? 0.5 : pos
		}
		wrap.css(dim);
		content.css({
			'width' : dim.width - currentOpts.padding * 2,
			'height' : dim.height - (titleHeight * pos) - currentOpts.padding * 2
		})
	}, _get_viewport = function() {
		return [$(window).width() - (currentOpts.margin * 2), $(window).height() - (currentOpts.margin * 2), $(document).scrollLeft() + currentOpts.margin, $(document).scrollTop() + currentOpts.margin]
	}, _get_zoom_to = function() {
		var view = _get_viewport(), to = {}, resize = currentOpts.autoScale, double_padding = currentOpts.padding * 2, ratio;
		if(currentOpts.width.toString().indexOf('%') > -1) {
			to.width = parseInt((view[0] * parseFloat(currentOpts.width)) / 100, 10)
		} else {
			to.width = currentOpts.width + double_padding
		}
		if(currentOpts.height.toString().indexOf('%') > -1) {
			to.height = parseInt((view[1] * parseFloat(currentOpts.height)) / 100, 10)
		} else {
			to.height = currentOpts.height + double_padding
		}
		if(resize && (to.width > view[0] || to.height > view[1])) {
			if(selectedOpts.type == 'image' || selectedOpts.type == 'swf') {
				ratio = (currentOpts.width) / (currentOpts.height);
				if((to.width) > view[0]) {
					to.width = view[0];
					to.height = parseInt(((to.width - double_padding) / ratio) + double_padding, 10)
				}
				if((to.height) > view[1]) {
					to.height = view[1];
					to.width = parseInt(((to.height - double_padding) * ratio) + double_padding, 10)
				}
			} else {
				to.width = Math.min(to.width, view[0]);
				to.height = Math.min(to.height, view[1])
			}
		}
		to.top = parseInt(Math.max(view[3] - 20, view[3] + ((view[1] - to.height - 40) * 0.5)), 10);
		to.left = parseInt(Math.max(view[2] - 20, view[2] + ((view[0] - to.width - 40) * 0.5)), 10);
		return to
	}, _get_obj_pos = function(obj) {
		var pos = obj.offset();
		pos.top += parseInt(obj.css('paddingTop'), 10) || 0;
		pos.left += parseInt(obj.css('paddingLeft'), 10) || 0;
		pos.top += parseInt(obj.css('border-top-width'), 10) || 0;
		pos.left += parseInt(obj.css('border-left-width'), 10) || 0;
		pos.width = obj.width();
		pos.height = obj.height();
		return pos
	}, _get_zoom_from = function() {
		var orig = selectedOpts.orig ? $(selectedOpts.orig) : false, from = {}, pos, view;
		if(orig && orig.length) {
			pos = _get_obj_pos(orig);
			from = {
				width : pos.width + (currentOpts.padding * 2),
				height : pos.height + (currentOpts.padding * 2),
				top : pos.top - currentOpts.padding - 20,
				left : pos.left - currentOpts.padding - 20
			}
		} else {
			view = _get_viewport();
			from = {
				width : currentOpts.padding * 2,
				height : currentOpts.padding * 2,
				top : parseInt(view[3] + view[1] * 0.5, 10),
				left : parseInt(view[2] + view[0] * 0.5, 10)
			}
		}
		return from
	}, _animate_loading = function() {
		if(!loading.is(':visible')) {
			clearInterval(loadingTimer);
			return
		}
		$('div', loading).css('top', (loadingFrame * -40) + 'px');
		loadingFrame = (loadingFrame + 1) % 12
	};
	$.fn.fancybox = function(options) {
		if(!$(this).length) {
			return this
		}
		$(this).data('fancybox', $.extend({}, options, ($.metadata ? $(this).metadata() : {}))).unbind('click.fb').bind('click.fb', function(e) {
			e.preventDefault();
			if(busy) {
				return
			}
			busy = true;
			$(this).blur();
			selectedArray = [];
			selectedIndex = 0;
			var rel = $(this).attr('rel') || '';
			if(!rel || rel == '' || rel === 'nofollow') {
				selectedArray.push(this)
			} else {
				selectedArray = $("a[rel=" + rel + "], area[rel=" + rel + "]");
				selectedIndex = selectedArray.index(this)
			}
			_start();
			return
		});
		return this
	};
	$.fancybox = function(obj) {
		var opts;
		if(busy) {
			return
		}
		busy = true;
		opts = typeof arguments[1] !== 'undefined' ? arguments[1] : {};
		selectedArray = [];
		selectedIndex = parseInt(opts.index, 10) || 0;
		if($.isArray(obj)) {
			for(var i = 0, j = obj.length; i < j; i++) {
				if( typeof obj[i] == 'object') {
					$(obj[i]).data('fancybox', $.extend({}, opts, obj[i]))
				} else {
					obj[i] = $({}).data('fancybox', $.extend({
						content : obj[i]
					}, opts))
				}
			}
			selectedArray = jQuery.merge(selectedArray, obj)
		} else {
			if( typeof obj == 'object') {
				$(obj).data('fancybox', $.extend({}, opts, obj))
			} else {
				obj = $({}).data('fancybox', $.extend({
					content : obj
				}, opts))
			}
			selectedArray.push(obj)
		}
		if(selectedIndex > selectedArray.length || selectedIndex < 0) {
			selectedIndex = 0
		}
		_start()
	};
	$.fancybox.showActivity = function() {
		clearInterval(loadingTimer);
		loading.show();
		loadingTimer = setInterval(_animate_loading, 66)
	};
	$.fancybox.hideActivity = function() {
		loading.hide()
	};
	$.fancybox.next = function() {
		return $.fancybox.pos(currentIndex + 1)
	};
	$.fancybox.prev = function() {
		return $.fancybox.pos(currentIndex - 1)
	};
	$.fancybox.pos = function(pos) {
		if(busy) {
			return
		}
		pos = parseInt(pos);
		selectedArray = currentArray;
		if(pos > -1 && pos < currentArray.length) {
			selectedIndex = pos;
			_start()
		} else if(currentOpts.cyclic && currentArray.length > 1) {
			selectedIndex = pos >= currentArray.length ? 0 : currentArray.length - 1;
			_start()
		}
		return
	};
	$.fancybox.cancel = function() {
		if(busy) {
			return
		}
		busy = true;
		$.event.trigger('fancybox-cancel');
		_abort();
		selectedOpts.onCancel(selectedArray, selectedIndex, selectedOpts);
		busy = false
	};
	$.fancybox.close = function() {
		if(busy || wrap.is(':hidden')) {
			return
		}
		busy = true;
		if(currentOpts && false === currentOpts.onCleanup(currentArray, currentIndex, currentOpts)) {
			busy = false;
			return
		}
		_abort();
		$(close.add(nav_left).add(nav_right)).hide();
		$(content.add(overlay)).unbind();
		$(window).unbind("resize.fb scroll.fb");
		$(document).unbind('keydown.fb');
		content.find('iframe').attr('src', isIE6 && /^https/i.test(window.location.href || '') ? 'javascript:void(false)' : 'about:blank');
		if(currentOpts.titlePosition !== 'inside') {
			title.empty()
		}
		wrap.stop();
		function _cleanup() {
			$('#fancybox-wrap').transition({ y: '-600px', opacity: 0, easing: 'ease-in', duration: 500}, 
				function() {
					overlay.fadeOut('fast');
					wrap.hide();
					$.event.trigger('fancybox-cleanup');
					content.empty();
					currentOpts.onClosed(currentArray, currentIndex, currentOpts);
					currentArray = selectedOpts = [];
					currentIndex = selectedIndex = 0;
					currentOpts = selectedOpts = {};
					busy = false
				} 
			);
		}

		if(currentOpts.transitionOut == 'elastic') {
			_cleanup();
			// start_pos = _get_zoom_from();
			// var pos = wrap.position();
			// final_pos = {
				// top : pos.top,
				// left : pos.left,
				// width : wrap.width(),
				// height : wrap.height()
			// };
			// if(currentOpts.opacity) {
				// final_pos.opacity = 1
			// }
			// title.empty().hide();
			// fx.prop = 1;
			// $(fx).animate({
				// prop : 0
			// }, {
				// duration : currentOpts.speedOut,
				// easing : currentOpts.easingOut,
				// step : _draw,
				// complete : _cleanup
			// })
		} else {
			wrap.fadeOut(currentOpts.transitionOut == 'none' ? 0 : currentOpts.speedOut, _cleanup)
		}
		
		// $('#fancybox-wrap').transition({ y: '-600px', opacity: 0, easing: 'ease-in', duration: 1000,}, 
			// function() {$('#fancybox-overlay').transition({opacity: 0}, 1000);
		// });
	};
	$.fancybox.resize = function() {
		if(overlay.is(':visible')) {
			overlay.css('height', $(document).height())
		}
		$.fancybox.center(true)
	};
	$.fancybox.center = function() {
		var view, align;
		if(busy) {
			return
		}
		align = arguments[0] === true ? 1 : 0;
		view = _get_viewport();
		if(!align && (wrap.width() > view[0] || wrap.height() > view[1])) {
			return
		}
		// wrap.stop().animate({
			// 'top' : parseInt(Math.max(view[3] - 20, view[3] + ((view[1] - content.height() - 40) * 0.5) - currentOpts.padding)),
			// 'left' : parseInt(Math.max(view[2] - 20, view[2] + ((view[0] - content.width() - 40) * 0.5) - currentOpts.padding))
		// }, typeof arguments[0] == 'number' ? arguments[0] : 200)
	};
	$.fancybox.init = function() {
		if($("#fancybox-wrap").length) {
			return
		}
		$('body').append( tmp = $('<div id="fancybox-tmp"></div>'), loading = $('<div id="fancybox-loading"><div></div></div>'), overlay = $('<div id="fancybox-overlay"></div>'), wrap = $('<div id="fancybox-wrap"></div>'));
		outer = $('<div id="fancybox-outer"></div>').appendTo(wrap);
		outer.append( close = $(), content = $('<div id="fancybox-content"></div>'), title = $(), nav_left = $(), nav_right = $());
		close.click($.fancybox.close);
		loading.click($.fancybox.cancel);
		nav_left.click(function(e) {
			e.preventDefault();
			$.fancybox.prev()
		});
		nav_right.click(function(e) {
			e.preventDefault();
			$.fancybox.next()
		});
		if($.fn.mousewheel) {
			wrap.bind('mousewheel.fb', function(e, delta) {
				if(busy) {
					e.preventDefault()
				} else if($(e.target).get(0).clientHeight == 0 || $(e.target).get(0).scrollHeight === $(e.target).get(0).clientHeight) {
					e.preventDefault();
					$.fancybox[delta>0?'prev':'next']()
				}
			})
		}
		if(!$.support.opacity) {
			wrap.addClass('fancybox-ie')
		}
		if(isIE6) {
			loading.addClass('fancybox-ie6');
			wrap.addClass('fancybox-ie6');
			$('<iframe id="fancybox-hide-sel-frame" src="' + (/^https/i.test(window.location.href || '') ? 'javascript:void(false)' : 'about:blank') + '" scrolling="no" border="0" frameborder="0" tabindex="-1"></iframe>').prependTo(outer)
		}
	};
	$.fn.fancybox.defaults = {
		padding : 10,
		margin : 40,
		opacity : false,
		modal : false,
		cyclic : false,
		scrolling : 'auto',
		width : 560,
		height : 340,
		autoScale : true,
		autoDimensions : true,
		centerOnScroll : false,
		ajax : {},
		swf : {
			wmode : 'transparent'
		},
		hideOnOverlayClick : true,
		hideOnContentClick : false,
		overlayShow : true,
		overlayOpacity : 0.7,
		overlayColor : '#777',
		titleShow : true,
		titlePosition : 'float',
		titleFormat : null,
		titleFromAlt : false,
		transitionIn : 'fade',
		transitionOut : 'fade',
		speedIn : 300,
		speedOut : 300,
		changeSpeed : 300,
		changeFade : 'fast',
		easingIn : 'swing',
		easingOut : 'swing',
		showCloseButton : true,
		showNavArrows : true,
		enableEscapeButton : true,
		enableKeyboardNav : true,
		onStart : function() {
		},
		onCancel : function() {
		},
		onComplete : function() {
		},
		onCleanup : function() {
		},
		onClosed : function() {
		},
		onError : function() {
		},
		specialC : null
	};
	$(document).ready(function() {
		$.fancybox.init()
	})
})(jQuery);
closeBox = $('.close-box').parent();
itemLink = $('.item-ref'), trash = $('.trash');

function initFancyBox(container) {
	if (typeof container == 'undefined' ) {
		container = '';
	}
	
	//Fancybox
	///------------------------------------------------------
	//variables
	closeBox = $(container + '.close-box').parent();
	itemLink = $(container + '.item-ref'), trash = $(container + '.trash');

	//determines new class for a button
	closeBox.click($.fancybox.close);
	closeBox.click(function(e) {
		e.preventDefault();
	});
	//Fancybox initializer
	itemLink.fancybox({
		'speedIn' : 1000,
		'speedOut' : 500,
		'overlayShow' : true,
		'overlayOpacity' : 0.85,
		'titleShow' : false,
		'overlayColor' : '#000',
		'transitionIn' : 'elastic',
		'transitionOut' : 'elastic',
		'easingIn' : 'easeOutBack',
		'easingOut' : 'easeInBack',
		'onStart' : function() {
			$('.item-info,.item-actions,#invitation-form').css('opacity', '0').delay(200).animate({
				opacity : 1
			}, 800);
		},
		'onComplete': function(){
			var fancyBoxWrap = $('#fancybox-wrap'),
				mozTransform = fancyBoxWrap.css('-moz-transform'),
				matrix,
				top;
				
			// Hack for Firefox, change css transform to absolute position top,
			// to prevent the page automatically scoll to top when typing on an input in the dialog 
			if(mozTransform){
				// Parse from the format matrix(int, int, int, int, int, int)
				matrix = mozTransform.substr(7, mozTransform.length - 8).split(', ');
				top = fancyBoxWrap.css('top');
				fancyBoxWrap.css('top', (parseInt(top, 10) + parseInt(matrix[5], 10)) + 'px');
				fancyBoxWrap.css('-moz-transform', 'none');
			}			
		},
		'onCleanup' : function() {
			$('.item-info,.item-actions,#invitation-form').fadeOut(300).delay(350).fadeIn();
		}
	});
}



function getCookie(name) {
	var cookieValue = null;
	if(document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for(var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if(cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}



function touchHandler(event){
	//alert($(event.target).attr('class'))
  if($(event.target).hasClass('touchable') || $(event.target).parent().hasClass('touchable')){
  	 //alert(event.target)
  	 $('.iosSlider').data('touchCarousel').freeze()
      var touches = event.changedTouches,
          first = touches[0],
          type = "";

           switch(event.type)
      {
          case "touchstart": type = "mousedown"; $('.iosSlider').data('touchCarousel').freeze(); break;
          case "touchmove":  type="mousemove"; break;        
          case "touchend":   type="mouseup"; $('.iosSlider').data('touchCarousel').unfreeze(); break;
          default: return;
      }
      var simulatedEvent = document.createEvent("MouseEvent");
      simulatedEvent.initMouseEvent(type, true, true, window, 1,
                                first.screenX, first.screenY,
                                first.clientX, first.clientY, false,
                                false, false, false, 0/*left*/, null);

      first.target.dispatchEvent(simulatedEvent);
      event.preventDefault();
      //event.stopPropagation();
  }
}

function initTouch()
{
   document.addEventListener("touchstart", touchHandler, true);
   document.addEventListener("touchmove", touchHandler, true);
   document.addEventListener("touchend", touchHandler, true);
   document.addEventListener("touchcancel", touchHandler, true);    
}

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

// jquery ui drag and drop init function
var slideNum = 0;
var latest_slide = 0;

function manualSlideLeft(){
	// remove the prev class
	$('.prev').each(function(){
		$(this).removeClass('prev');
	});	
	
	var slider = $('.slider');
	var num = $(slider).css('left');
	var real_num = num.split('px')[0];
	if (real_num && real_num <= 0){
		real_num = parseFloat(real_num);
		real_num += 5;
		num = real_num + 'px'
		$(slider).css('left', num);
	}	
}

function manualSlideRight(){
	var slider = $('.slider');
	var num = $(slider).css('left');
	var real_num = num.split('px')[0];
	if (real_num){
		real_num = parseFloat(real_num);
		real_num -= 5;
		num = real_num + 'px'
		$(slider).css('left', num);
	}	
}

function updateSlide(){
	var left = $('.slider').css('left');
	var left_num = left.split('px')[0];
	if (left_num){
		slide_num = Math.round(parseFloat(left_num)/787);
		$('.iosSlider').iosSlider('goToSlide', Math.abs(slide_num)+1);
	} 
}

function calcSlide(){
	var left = $('.slider').css('left');
	var left_num = left.split('px')[0];
	slide_num = Math.round(parseFloat(left_num)/787);
	return slide_num
}

function initDesktopSwipe(){
	// $('.iosSlider').iosSlider({
	// 	snapToChildren: true,
	// 	desktopClickDrag: true,
	// 	startAtSlide: slideNum+1,
	// 	unselectableSelector: $('.drag_item'),
	// 	onSliderLoaded: function(args){
	// 		if (isNaN(args['currentSlideNumber'])){
	// 			slideNum = 1;
	// 		}else{
	// 			slideNum = args['currentSlideNumber'];
	// 		}
	// 		//sliderTracking
	// 		if (args.numberOfSlides){
	// 			latest_slide = args.numberOfSlides;
	// 		}else{
	// 			latest_slide = 1;
	// 		}
			
	// 	},
	// 	onSlideStart: function(args){
	// 		current = args['currentSlideObject'][0];
	// 		prev = $(current).prev();
	// 		next = $(current).next();
	// 		if ($(current).hasClass('prev')){
	// 			$(current).removeClass('prev');
	// 		}
	// 		if ($(prev).hasClass('prev')){
	// 			$(prev).removeClass('prev');
	// 		}
	// 	},
	// 	onSlideChange: function(args){
	// 		if (isNaN(args['currentSlideNumber'])){
	// 			slideNum = 1;
	// 		}else{
	// 			slideNum = args['currentSlideNumber'];
	// 			// slideNum = calcSlide();
	// 		}
	// 		if (args.numberOfSlides){
	// 			latest_slide = args.numberOfSlides;
	// 		}else{
	// 			latest_slide = 1;
	// 		}
	// 		current = args['currentSlideObject'][0];
			
			
	// 		// Append more item into this queue 
			
			
	// 		// add class to prev object
	// 		prevs = $(current).prevAll();
			
	// 		$(prevs).each(function(){
	// 			if (!$(this).hasClass('prev')){
	// 				$(this).addClass('prev');
	// 			}
	// 		});
			
	// 		currentSlideNum = parseInt($(current).find('input[name="page_id"]').val(),10);
	// 		itemPerPage = parseInt($(current).find('input[name="item_per_page"]').val(), 10);
	// 		var page = latest_slide + 1;
	// 		if (latest_slide - 2 <= currentSlideNum){
	// 			$.ajax({
	// 		  		url: '?page=' + page + '&item_per_page=' + itemPerPage,
	// 		  		success: function(data) {
	// 		  			$('.iosSlider').iosSlider('addSlide', data, latest_slide + 1);
	// 		  			$('.iosSlider').iosSlider('update');
	// 		  			initFancyBox();
	// 		  			initDragDrop();
	// 		  			fixDragDropIssue();
	// 		  		}
	// 		  	});
	// 		}			
	// 	},
	// 	sliderCSS: { overflow: 'none', width: '787px', height: '588px' },
	// 	stageCSS: { position: 'relative', top: '0', left: '0', overflow: 'none', zIndex: 1 },
	// 	navPrevSelector: $('#prev'),
	// 	navNextSelector: $('#next'),
	// });

	$('.iosSlider').touchCarousel({
	    itemsPerMove: 3,              // The number of items to move per arrow click.
	    
	    snapToItems: true,           // Snap to items, based on itemsPerMove.
	    pagingNav: false,             // Enable paging nav. Overrides snapToItems.
	                                  // Snap to first item of every group, based on itemsPerMove. 
	                                  
	    pagingNavControls: false,      // Paging controls (bullets).
	    
	    scrollSpeed:1,
	    
	    autoplay:false,               // Autoplay enabled.
	    autoplayDelay:100,	          // Delay between transitions.
	    autoplayStopAtAction:true,    // Stop autoplay forever when user clicks arrow or does any other action.
	    
	    scrollbar: true,              // Scrollbar enabled.
	    scrollbarAutoHide: false,     // Scrollbar autohide.
	    scrollbarTheme: "light",       // Scrollbar color. Can be "light" or "dark".	
	    
	    transitionSpeed: 600,         // Carousel transition speed (next/prev arrows, slideshow).		
	    
	    directionNav:true,            // Direction (arrow) navigation (true or false).
	    directionNavAutoHide:false,   // Direction (arrow) navigation auto hide on hover. 
	                                  // On touch devices arrows are always displayed.
	    
	    loopItems: false,             // Loop items (don't disable arrows on last slide and allow autoplay to loop).
	    
	    keyboardNav: true,           // Keyboard arrows navigation.
	    dragUsingMouse:true,          // Enable drag using mouse.	
	    
	    
	    scrollToLast: true,          // Last item ends at start of carousel wrapper.	
	    
	    
	    itemFallbackWidth: 500,       // Default width of the item in pixels. (used if impossible to get item width).
	    
	    baseMouseFriction: 0.0012,    // Container friction on desktop (higher friction - slower speed).
	    baseTouchFriction: 0.0008,    // Container friction on mobile.
	    lockAxis: true,               // Allow dragging only on one direction.
	    useWebkit3d: false,           // Enable WebKit 3d transform on desktop devices. 
	                                  // (on touch devices this option is turned on).
	                                  // Use it if you have only images, 3d transform makes text blurry.
	                                           
	    
	    onAnimStart: null,            // Callback, triggers before deceleration or transition animation.
	    onAnimComplete: function(){

	    	number_of_slides = this.numItems;
	    	currentSlideNum = this.getCurrentId();
	    	//console.log(currentSlideNum)
	    	//console.log(number_of_slides)
			if (number_of_slides - currentSlideNum <= 6){
				$.ajax({
			  		url: '?page=' + 3 + '&item_per_page=' + 6,
			  		success: function(data) {
			  			var slider = $('.iosSlider').data('touchCarousel')
			  			var items = $(data).find('.item')
			  			$('.touchcarousel-container').append(items);
			  			slider.addItems(items);
			  		}
			  		,dataType:'html'
			  	});
			}
	    },         // Callback, triggers after deceleration or transition animation.
	    
	    onDragStart:null,             // Callback, triggers on drag start.
	    onDragRelease: null           // Callback, triggers on drag complete.
	});	


	//$('li.some-crazy-class').css("display", "block");
	
	// add mouse over support
	// $('#prev').click(function(e){
	// 	e.preventDefault();
	// });
	// $('#next').click(function(e){
	// 	e.preventDefault();
	// });
	
	//var id; 
	// $('#prev').hover(function(){
	// 	id = setInterval(manualSlideLeft, 50);
	// }, function(){
	// 	// remove the interval
	// 	clearInterval(id);
	// 	// set carousel to the earest slide
	// 	updateSlide();		
	// });
	
	// $('#next').hover(function(){
	// 	id = setInterval(manualSlideRight, 50);
	// }, function(){
	// 	// clear interval
	// 	clearInterval(id);
	// 	updateSlide();
	// });
}

var sliderInstance;

function initSwipe(selector){
				// Temporarily replacing with swipe.js for demo
	initDesktopSwipe();
	if($('.iosSlider').length){
		sliderInstance = $('.iosSlider').data('touchCarousel');
		sliderInstance.swipeStart = new Date();
		function handle(delta) {
			
			//var c = sliderInstance._getXPos();
			if (delta > 0){
				//sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");	
				sliderInstance.prev()

			}else{
				sliderInstance.next()
				//sliderInstance.animateTo(-80, sliderInstance.settings.transitionSpeed, "easeInOutSine");	
			}
		}

		function wheel(event){
			var delta = 0;
			//if (!event) event = window.event;
			if (event.originalEvent.wheelDelta) {
				delta = event.originalEvent.wheelDelta/120; 
			} else if (event.originalEvent.detail) {
				delta = -event.originalEvent.detail/3;
			}
			//console.log(delta)
			var now = new Date()
			if (! sliderInstance._isAnimating && now - sliderInstance.swipeStart > (sliderInstance.settings.transitionSpeed*1.5)){
				handle(delta);
				sliderInstance.swipeStart = now;
			}

		    if (event.preventDefault)
		            event.preventDefault();
		    event.originalEvent.returnValue = false;
		}

		if (selector){
			$(selector).on( "mousewheel DOMMouseScroll", wheel);
		}
	}
}

function initDragDrop() {	
	$('.drag_item').draggable({
		helper : "clone",
		appendTo : 'body',
		opacity : 0.6,
	    cursorAt : {
	      top : 200,
	      left : 100  	
	    },
		zIndex: 2700,
		start: function(event, ui) {
			if ($('.iosSlider').length){
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
        	if ($('.iosSlider').length){
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
	$($('.private-racks')[1]).sortable({
		stop : function(e, ui) {
		}
	});
	$($('.public-racks')[1]).sortable({
		stop : function(e, ui) {
		}
	});
	$($('.private-racks')[1]).disableSelection();
	$($('.public-racks')[1]).disableSelection();
}

function initFriendDragDrop() {	
	$('.drag_item').draggable({
		helper : "clone",
		opacity : 0.3,
	    cursorAt : {
	      top : 200,
	      left : 100  	
	    },
		zIndex: 2700,
		start: function(event, ui) {
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
            // $('.iosSlider').iosSlider('destroy', false);
            // $('.iosSlider').css('overflow','visible');
            $('#prev').on('nxt');
            $('#next').on('nxt');
        },
        stop: function(event, ui){
            initDesktopSwipe();
            $('.iosSlider').css('overflow','hidden');
            $('.nxt').each(function(){
            	$(this).removeClass('nxt');
            });
            $('#prev').on('hover');
            $('#next').on('hover');
        }
	});	
	var temp = "";
	
	$('.panel-content').find('.share_item').droppable({
		accept : ".drag_item",
		hoverClass : "drop_item_hover",
		drop : function(event, ui) {
			var item_id = $(ui.draggable).find('a').attr('data-value');
			// var rack_id = $(this).find('span').attr('data-value');
			var admirer_id = $(this).find('a').attr('data-value');
			var admirer_type = $(this).find('a').attr('data-type');
			var droppable = $(this).find('a');

			$('#reduced_item_id').val(item_id);
			$('#reduced_admirer_id').val(admirer_id);
			$('#reduced_admirer_type').val(admirer_type)
			$('#reduced_admirer_name').val($(this).find('a').attr('data-name'));
			
			if (admirer_type!='facebook'){
				$.fancybox({
					'speedIn' : 1000,
					'speedOut' : 500,
					'overlayShow' : true,
					'overlayOpacity' : 0.85,
					'titleShow' : false,
					'overlayColor' : '#000',
					'transitionIn' : 'elastic',
					'transitionOut' : 'elastic',
					'easingIn' : 'easeOutBack',
					'easingOut' : 'easeInBack',
				     'href' : '#send_to_admirer_reduced_form',
				     'onStart' : function() {
				     	$('#loading2').hide();
						$('#send_to_admirer_reduced_form').css('opacity', '0').show().delay(200).animate({
								opacity : 1
							}, 800);
							$('#send_item_confirmation_reduced').hide();
					 },
					 'onCleanup' : function() {
						$('#reduced_item_id').val("");
						$('#reduced_admirer_id').val("");
						$('#reduced_message').val("");
						$('#reduced_admirer_type').val("")
					},
					'onClosed': function(){
						$('#send_to_admirer_reduced_form').css('opacity', '0').css('display','none');
					}
				  });
				  
				  $('#send_it_to_admirer_reduced').click(function(){
				  		$('#loading2').css('display', 'inline');
				  		$.get('/racks/sent_to_admirer/?'+ $('#reduced_send_to_admirer_form').serialize(), function(data) {
				  			$('#loading2').css('display', 'none');
							$("#send_item_confirmation_reduced").css('opacity','1').text(data.result == 'ok' ? "Sent" : "Error").show();
							
							if(data.result != 'ok') {
								// do nothing here
							} else {
								// close fancy box after 2 second on success
								setTimeout("parent.$.fancybox.close()", 2000);
							}
						},'json');
				  });
			}else{
				$.get('/racks/sent_to_admirer'+ $('#reduced_send_to_admirer_form').serialize(), function(data) {
					FB.ui(data)
				})
			}}
		});
}

//Custom jQuery Code
$(function() {
	//hides items in the closet after clicking on a trash icon
	trash.click(function(e) {
		e.preventDefault();
		var self = $(this);
		//$(this).closest('.item').fadeOut(800);
		item_to_remove = $(this);
		var href = $(this).attr('href');
		$.get(href, function(data) {
			if(data.result == 'ok')
				item_to_remove.closest('.item').fadeOut(800);
			else
				alert(data.text);
		});
	});
	
	
	// if($('.errorlist').length > 0) {
	// 	// $('.errorlist').hide();
	// 	$('#bigform-error').stop();
	// 	$('#bigform-error').animate({
	// 		"opacity" : "1"
	// 	}, "fast", function() {
	// 		changeError($('#bigform-error')[0], $('.errorlist').text());
	// 		$('.acct .password-field').css('margin-bottom', '0px');
	// 		$('#bigform-error').css('display', 'inline');
	// 	});
	// }

	$('.yes-no').live("click", function(e) {
		// cannot stopPropagation on live event, consider using click for this
		e.preventDefault();
		var id = $(this).parent().attr('id');
		if(id.indexOf("item_visual_") == 0) {
			id = id.replace("item_visual_", "");
		} else {
			id = id.replace("item_", "");
		}

		$(".yes_" + id + ", .no_" + id).removeClass('voted');

		if($(this).hasClass("yes_" + id)) {
			$(".yes_" + id).addClass("voted");
		} else {
			$(".no_" + id).addClass("voted");
		}

		$.ajax({
			type : 'POST',
			data : {
				csrfmiddlewaretoken : getCookie('csrftoken')
			},
			dataType : 'json',
			url : $(this).children().attr('href'),
			success : function(data) {
				console.log(data.text);
				if(data.success == true) {
					
				} else {
					if(data.error_message == "Not authenticated.") {
						window.location = '/accounts/login/';
					} else if(data.error_message == "Profile update is required.") {
						window.location = '/accounts/profile';
					}
				}
			}
		});
	});
	$('.styled').css('height', 32).css('width', 205);

	//sent message appearence
	if($.browser.msie) {
		$('.confirmation').addClass('ie-fix-none');
		$('.send').click(function(e) {
			if($('#invitation-form').valid()) {
				e.preventDefault();
				$.ajax({
					type : "POST",
					url : "/admirers/invite",
					data : $("#invitation-form").serialize(),
					success : function(returnvalue) {
						$("#invite-friends-modal").html(returnvalue);
						$(this).next('.confirmation').removeClass('ie-fix-none').addClass('ie-fix-block');
						if($('.errorlist').length <= 0) {
							$('.confirmation').css("display", "inline");
							$('.confirmation').css("opacity", "1");
						}
					},
					error : function() {
						$('.confirmation').html("Error!");
						$(this).next('.confirmation').removeClass('ie-fix-none').addClass('ie-fix-block');
						$('.confirmation').css("display", "inline");
						$('.confirmation').css("opacity", "1");
					}
				});
			}
		});
	} else {
		$('.confirmation').css('opacity', 0);
		$('.send').click(function(e) {
			if($('#invitation-form').valid()) {
				e.preventDefault();
				$.ajax({
					type : "POST",
					url : "/admirers/invite",
					data : $("#invitation-form").serialize(),
					success : function(returnvalue) {
						$("#invite-friends-modal").html(returnvalue);
						if($('.errorlist').length <= 0) {
							$('.confirmation').css("display", "inline");
							$('.confirmation').css("opacity", "1");
						}
					},
					error : function() {
						$('.confirmation').html("Error!");
						$('.confirmation').css("display", "inline");
						$('.confirmation').css("opacity", "1");
					}
				});

			}
		});
	}

});
var page_count = Math.ceil($('#item_count').text() / 3)
var dummy_content = '';
if(page_count > 1) {
	dummy_content = $('.item-list').html();
}

var prev_element = null;
var next_element = null;
var next_page = 1;

//Carousel messed up list item fix
//
// $('#rotator').find('.item-list').eq(0).css('position', 'relative');

page_count--;
var next_page = 0;

function forward() {
	next_page++;
	if(next_page >= page_count) {
		next_page = 1;
	}

}

function backward() {
	next_page--;

	if(next_page <= -1) {
		next_page = page_count;
	}
}


if($.browser.msie) {
	$('.item').find('.no,.hanger').addClass('ie-icon-link');
}

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

// Footer down push
function getWindowHeight() {
	var windowHeight = 0;
	if( typeof (window.innerHeight) == 'number') {
		windowHeight = window.innerHeight;
	} else {
		if(document.documentElement && document.documentElement.clientHeight) {
			windowHeight = document.documentElement.clientHeight;
		} else {
			if(document.body && document.body.clientHeight) {
				windowHeight = document.body.clientHeight;
			}
		}
	}
	return windowHeight;
}

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

// Given email field is valid ? Return true : Display given error, return false
function mailCheck(emailField, validFunc, errorFunc, errMsg) {
	var filter = /^.+@.+\..{2,4}$/
	var email = emailField.value;
	// Pass
	if(filter.test(email) && email != "") {
		validFunc([emailField]);
		return true;
	} else if(isEmpty(email)) {
		emailField.value = emailField.defaultValue;
	}
	// Fail
	else {
		errorFunc([emailField], errMsg);
		return false;
	}
}

// Check if fields are equal, execute appropriate function
function validCheck(fieldA, fieldB, validFunc, errorFunc, errMsg) {
	//if(fieldA.value == fieldB.value && fieldA.value != fieldA.defaultValue){
	if(fieldA.value == fieldB.value && (fieldA.value != fieldA.defaultValue || fieldA.value.toLowerCase() != "required") && fieldA.value != "" && fieldB.value != "") {
		validFunc([fieldA, fieldB]);
		return true;
	} else {
		errorFunc([fieldA, fieldB], errMsg);
		return false;
	}
}

// Check if fields are equal, execute appropriate function
function filledCheck(field, validFunc, errorFunc, errMsg) {
	if(field.value != "" && field.value != null && (field.value != field.defaultValue || field.value.toLowerCase() != "required") && !isEmpty(field.value)) {
		validFunc([field]);
		return true;
	} else {
		errorFunc([field], errMsg);
		return false;
	}
}

// Wait list valid form function
function waitValid() {
	//$('#waitlist-form .btn').removeAttr('disabled');
	$('#waitlist-error').animate({
		"opacity" : "0"
	}, "fast", function() {
		$('#waitlist-form').css({
			'padding-bottom' : '25px',
			'margin-bottom' : '0px'
		});
		$('#waitlist-error').css('display', 'none');
	});
}

// Wait list erroneous form function
function waitError() {
	$('#waitlist-form').css({
		'padding-bottom' : '0px',
		'margin-bottom' : '-3px'
	});
	$('#waitlist-error').css('display', 'inline');
	$('#waitlist-error').animate({
		"opacity" : "1"
	}, "fast");
	//$('#waitlist-form .btn').attr('disabled', 'disabled');
}

function bigValid(fields) {
	for(tar in fields) {
		$(fields[tar]).removeClass('field-error');
	}
	$('#bigform-error').animate({
		"opacity" : "0"
	}, "fast", function() {
		$('#bigform-error').css('display', 'none');
		$('.acct .password-field').css('margin-bottom', '40px');
	});
}

function bigError(fields, msg) {
	for(tar in fields) {
		$(fields[tar]).addClass('field-error');
	}
	$('#bigform-error').stop();
	$('#bigform-error').animate({
		"opacity" : "1"
	}, "fast", function() {
		changeError($('#bigform-error')[0], msg);
		//$('.acct .password-field').css('margin-bottom', '0px');
		$('#bigform-error').css('display', 'inline');
	});
}

function changeError(target, message) {
	target.innerHTML = message;
}

// Submit button check form, supress default if invalid
// $('#account-form .btn').click(function(event){
// mailCheck($('#account-form .txt')[0], function(){}, function(){event.preventDefault();});
// });

$('#waitlist-form .btn').click(function(event) {
	bigformCheck();
});
function submitCheck(target) {
	var formCheck = mailCheck(target, function() {
	}, function() {
	});
}

///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Auto-complete jQuery Code
$(function() {

	//Source for tags, create your own if you need
	var availableTags = ['ActionScript', 'AppleScript', 'Asp', 'BASIC', 'C', 'C++', 'Clojure', 'COBOL', 'ColdFusion', 'Erlang', 'Fortran', 'Groovy', 'Haskell', 'Java', 'JavaScript', 'Lisp', 'Perl', 'PHP', 'Python', 'Ruby', 'Scala', 'Scheme', 'aaa', 'aab', 'aba', 'baa', 'abb', 'bab', 'bba', 'aaaa', 'aaab', 'aaba', 'abaa', 'baaa', 'aabb'];

	//Some other choices
	var someOtherAvailableTags = ['True Religion', 'Levis', 'Diesel', 'Joes', 'Calvin', 'Jeans'];

	if($('#admirers-auto-complete').length > 0) {
		$.get('/admirers/get_friends', function(data) {
			$('#admirers-auto-complete').autocomplete({

				//select a field
				appendTo : '#admirer-search-form',

				//Array that holds tags
				// source : availableTags,
				source : data.friends,

				//Sorting of auto complete list
				open : function(event, ui) {
					var mylist = $('.ui-autocomplete');
					var listitems = mylist.children('li').get();
					listitems.sort(function(a, b) {
						var compA = $(a).text().toUpperCase();
						var compB = $(b).text().toUpperCase();
						return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
					});
					$.each(listitems, function(idx, itm) {
						mylist.append(itm);
					});
				}
			});
		});
	}

	if($('#welcome-auto-complete').length > 0) {
		$.get('/racks/brands', function(data) {
			$('#welcome-auto-complete').autocomplete({

				//select a field
				// appendTo : '#welcome .designer-field',

				//Array that holds tags
				source : data.brands,

				//Sorting of auto complete list
				open : function(event, ui) {

					//Sorting of auto complete list
					var mylist = $('.ui-autocomplete');
					var listitems = mylist.children('li').get();
					listitems.sort(function(a, b) {
						var compA = $(a).text().toUpperCase();
						var compB = $(b).text().toUpperCase();
						return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
					});
					$.each(listitems, function(idx, itm) {
						mylist.append(itm);
					});
				}
			});
		});
	}

	///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
	//Add racks based on keypress or

	var inpLstFld = $('#input-list-field'), newAddLst = $('#new-shared-add'), newAddLnk = $('#new-shared');
	inpLstFld.keypress(function(e) {
		if(e.keyCode == 13) {
			newAddLst.append($('<li>', {
				text : inpLstFld.val()
			}));
			$(this).val('');
		}
	});
	newAddLnk.find('.plus').click(function(e) {
		newAddLst.append($('<li>', {
			text : inpLstFld.val()
		}));
		inpLstFld.val('');
		e.preventDefault();
	});
}); ( function($) {
	// custom css expression for a case-insensitive contains()
	jQuery.expr[':'].Contains = function(a, i, m) {
		return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
	};
	jQuery.expr[':'].contains = function(a, i, m) {
		return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
	};
}(jQuery));


///------------------------------------Django AJAX CSRF Protection -------------------------------///
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
///------------------------------- End Django AJAX CSRF Protection -------------------------------///

function fixDragDropIssue(){
	var item_per_page = $($('.item_per_page')[0]).val();
	if(item_per_page == 6){
		$('.drag_item').draggable("option", "cursorAt", {left: 70, top: 70});
	}else if (item_per_page == 9){
		$('.drag_item').draggable("option", "cursorAt", {left: 60, top: 50});
	}
}



$(document).ready(function() {
  initFancyBox();
  if ($.browser.msie && $.browser.version.substr(0,1)<7)
  {
	$('li').has('ul').mouseover(function(){
		alert('est');
		$(this).children('ul').css('visibility','visible');
		}).mouseout(function(){
		$(this).children('ul').css('visibility','hidden');
		})
  }
  
  $('.spinner').sprite({ fps: 10, no_of_frames: 12 });
});

// setup ajax call for notification table
  function callNoticeAjax(){
	$.get('/racks/get_new_notifications/', function(returnData){
		if (returnData['success'] == true && returnData['has_new'] == true ){
			$('#happening-events').trigger("click");
		}
	});
  }

$(document).ready(function() {
	
	$('#event-table').click(function(event){
		event.stopPropagation();
	});
$('#happening-events').click(function() {
  // var table = document.getElementById("event-table");
  // if(table.style.display == "none") {
        // table.style.display = "block";
    // }
  // else {
    // table.style.display = "none";
  // }
  	var icon = $(this).find('.icon')[0];
  	$(icon).effect('bounce', 500, function(){
  		setTimeout(function() {
			$(icon).removeAttr("style").hide().fadeIn();
		}, 1000 );
  	});
	if ($('#event-table').css('display') == 'none'){
		// get content from ajax
		$.get('/racks/display_notice_table/', function(returnData){
			$('#event-table').html(returnData).fadeIn(2000, function(){
				// popup the buble for 10 seconds before closing it
				setTimeout("$('#event-table').fadeOut(2000)", 10000);
			});
		});		
	}else{
		$('#event-table').fadeOut(2000);
	}
	
  });
  
  setInterval(callNoticeAjax, 120000);
  
});

function setupRackIt(){
	// prevent more binds when close fancy box
	$('.rack-icon').unbind("click");
	$('.rack-icon').click(function(event){
		event.preventDefault();
		var href = $(this).attr('href');
		var item_id = $(this).attr('data-value');
		var containers = $('.private-racks').find('li span');
		if (containers.length > 0){
			rack_id = $(containers[0]).attr('data-value');
		}else{
			rack_id = "myrack";
		}
		
		var link = href + 'item_id=' + item_id +'&rack=' + rack_id;
		$.get(link, function(result){
			if(result['result'] == 'ok'){
				alert("Item Added!");
				if(result['new_rack_id']){
					// add a new rack name My Rack into the left-nav by using javascript
					$('.private-racks').html('<li class="drop_item ui-droppable">'+
                                            '<span data-value="'+ result['new_rack_id'] +'"><a href="/racks/detail/' + result['new_rack_id'] + '">' +
                                            'My Rack</a></span></li>');
                    initDragDrop();
                    fixDragDropIssue();
				}
				// check if fancy box is opened
				if($('#fu').length > 0){
					parent.$.fancybox.close();
				}
			}else{
				alert(result['Error']);
			}
		});
	});
}



function initSliderTracking() {
	sliderTracking = [];
	var pageCount = Math.ceil(parseInt($('#item_count').text(), 10) / parseInt($('#item_per_page').text(),10));
	for (var i=1; i <= pageCount; i++) {
	  sliderTracking[i] = false;
	};
	var slides = $('.iosSlider .slider .slide');
	slides.length;
	for(var i=0,j=slides.length; i<j; i++){
	  sliderTracking[parseInt($(slides[i]).find('input[name="page_id"]').val(), 10)] = true;
	};	
}



function stella_refund(transaction) {
	$.ajax({
		type: 'POST',
  		url: '/cart/shopper_return_items',
  		data: {'transactionid': transaction},
  		success: function(data) {
			$("#message-holder-" + transaction).text(text.success)
  		}
  	});
}

function stella_refund_item(item_id, transaction) {
	$.ajax({
		type: 'POST',
  		url: '/cart/shopper_return_item',
  		data: {'item_id': item_id, 'transactionid': transaction},
  		success: function(data) {
  			$(".alert").show();
  			if (data.success) {
  				if (!$(".alert").hasClass("alert-info")) $(".alert").addClass("alert-info");	
				$(".alert span").text(data.message);
				
				$('#item-' + data.item.id + '-status').text(data.item.status);
				
			} else {
				if ($(".alert").hasClass("alert-info")) $(".alert").removeClass("alert-info");	
				$(".alert span").text(data.message);
			}
  		}
  	});
}

function stella_request_refund_item(item_id, transaction) {
	$.ajax({
		type: 'POST',
  		url: '/cart/shopper_request_refund_item',
  		data: {'item_id': item_id, 'transactionid': transaction},
  		success: function(data) {
  			$(".alert").show();
  			if (data.success) {
  				if (!$(".alert").hasClass("alert-info")) $(".alert").addClass("alert-info");	
				$(".alert span").text(data.message);
				
				$('#item-' + data.item.id + '-status').parent().find('input').hide();
				$('#item-' + data.item.id + '-status').text(data.item.status);
				
			} else {
				if ($(".alert").hasClass("alert-info")) $(".alert").removeClass("alert-info");	
				$(".alert span").text(data.message);
			}
  		}
  	});
}

function not_logged_in(){
	return false
}

function login_modal(){
	initFancyBox('#social_login_box ');
}

function hookupFBMessages(STATIC_URL,URL){
    $('.friend_adder').click(function(e){
    	e.preventDefault();
        publish = {
          'method': 'feed'
          ,'link': URL
          ,'description': 'Hi, Check out Stunable'
          ,'name':"Stunable Invite"
          ,'to':$(this).attr('data-value')
          ,'picture':URL+STATIC_URL+'/images/logo_small.jpg'
        }
        FB.ui(publish);
        $('.spinner').hide()
        return false;
    })
}

//$('#fancybox-wrap').transition({ y: '-200px', opacity: 0, easing: 'snap', duration: 500,}, function() {$('#fancybox-overlay').transition({opacity: 0}, 1000);});
