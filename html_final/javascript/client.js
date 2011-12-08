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
eval(function(p,a,c,k,e,r){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)r[e(c)]=k[c]||e(c);k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('h.i[\'1a\']=h.i[\'z\'];h.O(h.i,{y:\'D\',z:9(x,t,b,c,d){6 h.i[h.i.y](x,t,b,c,d)},17:9(x,t,b,c,d){6 c*(t/=d)*t+b},D:9(x,t,b,c,d){6-c*(t/=d)*(t-2)+b},13:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t+b;6-c/2*((--t)*(t-2)-1)+b},X:9(x,t,b,c,d){6 c*(t/=d)*t*t+b},U:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t+1)+b},R:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t+b;6 c/2*((t-=2)*t*t+2)+b},N:9(x,t,b,c,d){6 c*(t/=d)*t*t*t+b},M:9(x,t,b,c,d){6-c*((t=t/d-1)*t*t*t-1)+b},L:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t+b;6-c/2*((t-=2)*t*t*t-2)+b},K:9(x,t,b,c,d){6 c*(t/=d)*t*t*t*t+b},J:9(x,t,b,c,d){6 c*((t=t/d-1)*t*t*t*t+1)+b},I:9(x,t,b,c,d){e((t/=d/2)<1)6 c/2*t*t*t*t*t+b;6 c/2*((t-=2)*t*t*t*t+2)+b},G:9(x,t,b,c,d){6-c*8.C(t/d*(8.g/2))+c+b},15:9(x,t,b,c,d){6 c*8.n(t/d*(8.g/2))+b},12:9(x,t,b,c,d){6-c/2*(8.C(8.g*t/d)-1)+b},Z:9(x,t,b,c,d){6(t==0)?b:c*8.j(2,10*(t/d-1))+b},Y:9(x,t,b,c,d){6(t==d)?b+c:c*(-8.j(2,-10*t/d)+1)+b},W:9(x,t,b,c,d){e(t==0)6 b;e(t==d)6 b+c;e((t/=d/2)<1)6 c/2*8.j(2,10*(t-1))+b;6 c/2*(-8.j(2,-10*--t)+2)+b},V:9(x,t,b,c,d){6-c*(8.o(1-(t/=d)*t)-1)+b},S:9(x,t,b,c,d){6 c*8.o(1-(t=t/d-1)*t)+b},Q:9(x,t,b,c,d){e((t/=d/2)<1)6-c/2*(8.o(1-t*t)-1)+b;6 c/2*(8.o(1-(t-=2)*t)+1)+b},P:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6-(a*8.j(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b},H:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d)==1)6 b+c;e(!p)p=d*.3;e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);6 a*8.j(2,-10*t)*8.n((t*d-s)*(2*8.g)/p)+c+b},T:9(x,t,b,c,d){f s=1.l;f p=0;f a=c;e(t==0)6 b;e((t/=d/2)==2)6 b+c;e(!p)p=d*(.3*1.5);e(a<8.w(c)){a=c;f s=p/4}m f s=p/(2*8.g)*8.r(c/a);e(t<1)6-.5*(a*8.j(2,10*(t-=1))*8.n((t*d-s)*(2*8.g)/p))+b;6 a*8.j(2,-10*(t-=1))*8.n((t*d-s)*(2*8.g)/p)*.5+c+b},F:9(x,t,b,c,d,s){e(s==u)s=1.l;6 c*(t/=d)*t*((s+1)*t-s)+b},E:9(x,t,b,c,d,s){e(s==u)s=1.l;6 c*((t=t/d-1)*t*((s+1)*t+s)+1)+b},16:9(x,t,b,c,d,s){e(s==u)s=1.l;e((t/=d/2)<1)6 c/2*(t*t*(((s*=(1.B))+1)*t-s))+b;6 c/2*((t-=2)*t*(((s*=(1.B))+1)*t+s)+2)+b},A:9(x,t,b,c,d){6 c-h.i.v(x,d-t,0,c,d)+b},v:9(x,t,b,c,d){e((t/=d)<(1/2.k)){6 c*(7.q*t*t)+b}m e(t<(2/2.k)){6 c*(7.q*(t-=(1.5/2.k))*t+.k)+b}m e(t<(2.5/2.k)){6 c*(7.q*(t-=(2.14/2.k))*t+.11)+b}m{6 c*(7.q*(t-=(2.18/2.k))*t+.19)+b}},1b:9(x,t,b,c,d){e(t<d/2)6 h.i.A(x,t*2,0,c,d)*.5+b;6 h.i.v(x,t*2-d,0,c,d)*.5+c*.5+b}});',62,74,'||||||return||Math|function|||||if|var|PI|jQuery|easing|pow|75|70158|else|sin|sqrt||5625|asin|||undefined|easeOutBounce|abs||def|swing|easeInBounce|525|cos|easeOutQuad|easeOutBack|easeInBack|easeInSine|easeOutElastic|easeInOutQuint|easeOutQuint|easeInQuint|easeInOutQuart|easeOutQuart|easeInQuart|extend|easeInElastic|easeInOutCirc|easeInOutCubic|easeOutCirc|easeInOutElastic|easeOutCubic|easeInCirc|easeInOutExpo|easeInCubic|easeOutExpo|easeInExpo||9375|easeInOutSine|easeInOutQuad|25|easeOutSine|easeInOutBack|easeInQuad|625|984375|jswing|easeInOutBounce'.split('|'),0,{}));



///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Text input field populators
//this.focus(function(){});



// CLEAR TEXT INPUTS OF DEFAULT VALUE ON FOCUS
function clearInput(textField) {
	if (textField.value == textField.defaultValue) {
		textField.value = "";
	}
}
// RESTORE TEXT INPUT DEFAULT VALUE ON BLUR
function restoreInput(textField){
	if (textField.value == "" || isEmpty(textField.value)){
		textField.value = textField.defaultValue;
	}
}

function isEmpty(tarString){
	var blanks = /^\s*$/
	if(blanks.test(tarString)){
		return true;
	}
	return false;
}

function isDefault(textField){
	if (textField.value == textField.defaultValue){
		return true;
	}
	return false;
}



///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
// MAKE SELECT BOXES (DROP-DOWNS) PRETTY

(function($){
 $.fn.extend({
 	customStyle : function(options) {
	  if(!$.browser.msie || ($.browser.msie&&$.browser.version>6)){
	  return this.each(function() {
			var currentSelected = $(this).find(':selected');
			$(this).after('<span class="customStyleSelectBox"><span class="customStyleSelectBoxInner">'+currentSelected.text()+'</span></span>').css({position:'absolute', opacity:0,fontSize:'0.86em'});
			var selectBoxSpan = $(this).next();
			var selectBoxWidth = parseInt($(this).width()) - parseInt(selectBoxSpan.css('padding-left')) - parseInt(selectBoxSpan.css('padding-right'));			
			var selectBoxSpanInner = selectBoxSpan.find(':first-child');
			selectBoxSpan.css({display:'inline-block'});
			selectBoxSpanInner.css({width:'147px', display:'inline-block'});
			var selectBoxHeight = parseInt(selectBoxSpan.height()) + parseInt(selectBoxSpan.css('padding-top')) + parseInt(selectBoxSpan.css('padding-bottom'));
			$(this).height(selectBoxHeight).change(function(){
				selectBoxSpanInner.text($(this).val()).parent().addClass('changed');
			});
	  });
	  }
	}
 });

//drop down box initializer
$('select.styled').customStyle();

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
;(function($){var tmp,loading,overlay,wrap,outer,content,close,title,nav_left,nav_right,selectedIndex=0,selectedOpts={},selectedArray=[],currentIndex=0,currentOpts={},currentArray=[],ajaxLoader=null,imgPreloader=new Image(),imgRegExp=/\.(jpg|gif|png|bmp|jpeg)(.*)?$/i,swfRegExp=/[^\.]\.(swf)\s*$/i,loadingTimer,loadingFrame=1,titleHeight=0,titleStr='',start_pos,final_pos,busy=false,fx=$.extend($('<div/>')[0],{prop:0}),isIE6=$.browser.msie&&$.browser.version<7&&!window.XMLHttpRequest,_abort=function(){loading.hide();imgPreloader.onerror=imgPreloader.onload=null;if(ajaxLoader){ajaxLoader.abort()}tmp.empty()},_error=function(){if(false===selectedOpts.onError(selectedArray,selectedIndex,selectedOpts)){loading.hide();busy=false;return}selectedOpts.titleShow=false;selectedOpts.width='auto';selectedOpts.height='auto';tmp.html('<p id="fancybox-error">The requested content cannot be loaded.<br />Please try again later.</p>');_process_inline()},_start=function(){var obj=selectedArray[selectedIndex],href,type,title,str,emb,ret;_abort();selectedOpts=$.extend({},$.fn.fancybox.defaults,(typeof $(obj).data('fancybox')=='undefined'?selectedOpts:$(obj).data('fancybox')));ret=selectedOpts.onStart(selectedArray,selectedIndex,selectedOpts);if(ret===false){busy=false;return}else if(typeof ret=='object'){selectedOpts=$.extend(selectedOpts,ret)}title=selectedOpts.title||(obj.nodeName?$(obj).attr('title'):obj.title)||'';if(obj.nodeName&&!selectedOpts.orig){selectedOpts.orig=$(obj).children("img:first").length?$(obj).children("img:first"):$(obj)}if(title===''&&selectedOpts.orig&&selectedOpts.titleFromAlt){title=selectedOpts.orig.attr('alt')}href=selectedOpts.href||(obj.nodeName?$(obj).attr('href'):obj.href)||null;if((/^(?:javascript)/i).test(href)||href=='#'){href=null}if(selectedOpts.type){type=selectedOpts.type;if(!href){href=selectedOpts.content}}else if(selectedOpts.content){type='html'}else if(href){if(href.match(imgRegExp)){type='image'}else if(href.match(swfRegExp)){type='swf'}else if($(obj).hasClass("iframe")){type='iframe'}else if(href.indexOf("#")===0){type='inline'}else{type='ajax'}}if(!type){_error();return}if(type=='inline'){obj=href.substr(href.indexOf("#"));type=$(obj).length>0?'inline':'ajax'}selectedOpts.type=type;selectedOpts.href=href;selectedOpts.title=title;if(selectedOpts.autoDimensions){if(selectedOpts.type=='html'||selectedOpts.type=='inline'||selectedOpts.type=='ajax'){selectedOpts.width='auto';selectedOpts.height='auto'}else{selectedOpts.autoDimensions=false}}if(selectedOpts.modal){selectedOpts.overlayShow=true;selectedOpts.hideOnOverlayClick=false;selectedOpts.hideOnContentClick=false;selectedOpts.enableEscapeButton=false;selectedOpts.showCloseButton=false}selectedOpts.padding=parseInt(selectedOpts.padding,10);selectedOpts.margin=parseInt(selectedOpts.margin,10);tmp.css('padding',(selectedOpts.padding+selectedOpts.margin));$('.fancybox-inline-tmp').unbind('fancybox-cancel').bind('fancybox-change',function(){$(this).replaceWith(content.children())});switch(type){case'html':tmp.html(selectedOpts.content);_process_inline();break;case'inline':if($(obj).parent().is('#fancybox-content')===true){busy=false;return}$('<div class="fancybox-inline-tmp" />').hide().insertBefore($(obj)).bind('fancybox-cleanup',function(){$(this).replaceWith(content.children())}).bind('fancybox-cancel',function(){$(this).replaceWith(tmp.children())});$(obj).appendTo(tmp);_process_inline();break;case'image':busy=false;$.fancybox.showActivity();imgPreloader=new Image();imgPreloader.onerror=function(){_error()};imgPreloader.onload=function(){busy=true;imgPreloader.onerror=imgPreloader.onload=null;_process_image()};imgPreloader.src=href;break;case'swf':selectedOpts.scrolling='no';str='<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="'+selectedOpts.width+'" height="'+selectedOpts.height+'"><param name="movie" value="'+href+'"></param>';emb='';$.each(selectedOpts.swf,function(name,val){str+='<param name="'+name+'" value="'+val+'"></param>';emb+=' '+name+'="'+val+'"'});str+='<embed src="'+href+'" type="application/x-shockwave-flash" width="'+selectedOpts.width+'" height="'+selectedOpts.height+'"'+emb+'></embed></object>';tmp.html(str);_process_inline();break;case'ajax':busy=false;$.fancybox.showActivity();selectedOpts.ajax.win=selectedOpts.ajax.success;ajaxLoader=$.ajax($.extend({},selectedOpts.ajax,{url:href,data:selectedOpts.ajax.data||{},error:function(XMLHttpRequest,textStatus,errorThrown){if(XMLHttpRequest.status>0){_error()}},success:function(data,textStatus,XMLHttpRequest){var o=typeof XMLHttpRequest=='object'?XMLHttpRequest:ajaxLoader;if(o.status==200){if(typeof selectedOpts.ajax.win=='function'){ret=selectedOpts.ajax.win(href,data,textStatus,XMLHttpRequest);if(ret===false){loading.hide();return}else if(typeof ret=='string'||typeof ret=='object'){data=ret}}tmp.html(data);_process_inline()}}}));break;case'iframe':_show();break}},_process_inline=function(){var w=selectedOpts.width,h=selectedOpts.height;if(w.toString().indexOf('%')>-1){w=parseInt(($(window).width()-(selectedOpts.margin*2))*parseFloat(w)/100,10)+'px'}else{w=w=='auto'?'auto':w+'px'}if(h.toString().indexOf('%')>-1){h=parseInt(($(window).height()-(selectedOpts.margin*2))*parseFloat(h)/100,10)+'px'}else{h=h=='auto'?'auto':h+'px'}selectedOpts.width=tmp.width();selectedOpts.height=tmp.height();_show()},_process_image=function(){selectedOpts.width=imgPreloader.width;selectedOpts.height=imgPreloader.height;$("<img />").attr({'id':'fancybox-img','src':imgPreloader.src,'alt':selectedOpts.title}).appendTo(tmp);_show()},_show=function(){var pos,equal;loading.hide();if(wrap.is(":visible")&&false===currentOpts.onCleanup(currentArray,currentIndex,currentOpts)){$.event.trigger('fancybox-cancel');busy=false;return}busy=true;$(content.add(overlay)).unbind();$(window).unbind("resize.fb scroll.fb");$(document).unbind('keydown.fb');if(wrap.is(":visible")&&currentOpts.titlePosition!=='outside'){wrap.css('height',wrap.height())}currentArray=selectedArray;currentIndex=selectedIndex;currentOpts=selectedOpts;if(currentOpts.overlayShow){overlay.css({'background-color':currentOpts.overlayColor,'opacity':currentOpts.overlayOpacity,'cursor':currentOpts.hideOnOverlayClick?'pointer':'auto','height':$(document).height()});if(!overlay.is(':visible')){if(isIE6){$('select:not(#fancybox-tmp select)').filter(function(){return this.style.visibility!=='hidden'}).css({'visibility':'hidden'}).one('fancybox-cleanup',function(){this.style.visibility='inherit'})}overlay.show()}}else{overlay.hide()}final_pos=_get_zoom_to();_process_title();if(wrap.is(":visible")){$(close.add(nav_left).add(nav_right)).hide();pos=wrap.position(),start_pos={top:pos.top,left:pos.left,width:wrap.width(),height:wrap.height()};equal=(start_pos.width==final_pos.width&&start_pos.height==final_pos.height);content.fadeTo(currentOpts.changeFade,0.3,function(){var finish_resizing=function(){content.html(tmp.contents()).fadeTo(currentOpts.changeFade,1,_finish)};$.event.trigger('fancybox-change');content.empty().removeAttr('filter').css({'border-width':currentOpts.padding,'width':final_pos.width-currentOpts.padding*2,'height':selectedOpts.autoDimensions?'auto':final_pos.height-titleHeight-currentOpts.padding*2});if(equal){finish_resizing()}else{fx.prop=0;$(fx).animate({prop:1},{duration:currentOpts.changeSpeed,easing:currentOpts.easingChange,step:_draw,complete:finish_resizing})}});return}wrap.removeAttr("style");content.css('border-width',0);if(currentOpts.transitionIn=='elastic'){start_pos=_get_zoom_from();content.html(tmp.contents());wrap.show();if(currentOpts.opacity){final_pos.opacity=0}fx.prop=0;$(fx).animate({prop:1},{duration:currentOpts.speedIn,easing:currentOpts.easingIn,step:_draw,complete:_finish});return}if(currentOpts.titlePosition=='inside'&&titleHeight>0){title.show()}content.css({'width':final_pos.width-currentOpts.padding*2,'height':selectedOpts.autoDimensions?'auto':final_pos.height-titleHeight-currentOpts.padding*2}).html(tmp.contents());wrap.css(final_pos).fadeIn(currentOpts.transitionIn=='none'?0:currentOpts.speedIn,_finish)},_format_title=function(title){if(title&&title.length){if(currentOpts.titlePosition=='float'){return'<table id="fancybox-title-float-wrap" cellpadding="0" cellspacing="0"><tr><td id="fancybox-title-float-left"></td><td id="fancybox-title-float-main">'+title+'</td><td id="fancybox-title-float-right"></td></tr></table>'}return'<div id="fancybox-title-'+currentOpts.titlePosition+'">'+title+'</div>'}return false},_process_title=function(){titleStr=currentOpts.title||'';titleHeight=0;title.empty().removeAttr('style').removeClass();if(currentOpts.titleShow===false){title.hide();return}titleStr=$.isFunction(currentOpts.titleFormat)?currentOpts.titleFormat(titleStr,currentArray,currentIndex,currentOpts):_format_title(titleStr);if(!titleStr||titleStr===''){title.hide();return}title.addClass('fancybox-title-'+currentOpts.titlePosition).html(titleStr).appendTo('body').show();switch(currentOpts.titlePosition){case'inside':title.css({'width':final_pos.width-(currentOpts.padding*2),'marginLeft':currentOpts.padding,'marginRight':currentOpts.padding});titleHeight=title.outerHeight(true);title.appendTo(outer);final_pos.height+=titleHeight;break;case'over':title.css({'marginLeft':currentOpts.padding,'width':final_pos.width-(currentOpts.padding*2),'bottom':currentOpts.padding}).appendTo(outer);break;case'float':title.css('left',parseInt((title.width()-final_pos.width-40)/2,10)*-1).appendTo(wrap);break;default:title.css({'width':final_pos.width-(currentOpts.padding*2),'paddingLeft':currentOpts.padding,'paddingRight':currentOpts.padding}).appendTo(wrap);break}title.hide()},_set_navigation=function(){if(currentOpts.enableEscapeButton||currentOpts.enableKeyboardNav){$(document).bind('keydown.fb',function(e){if(e.keyCode==27&&currentOpts.enableEscapeButton){e.preventDefault();$.fancybox.close()}else if((e.keyCode==37||e.keyCode==39)&&currentOpts.enableKeyboardNav&&e.target.tagName!=='INPUT'&&e.target.tagName!=='TEXTAREA'&&e.target.tagName!=='SELECT'){e.preventDefault();$.fancybox[e.keyCode==37?'prev':'next']()}})}if(!currentOpts.showNavArrows){nav_left.hide();nav_right.hide();return}if((currentOpts.cyclic&&currentArray.length>1)||currentIndex!==0){nav_left.show()}if((currentOpts.cyclic&&currentArray.length>1)||currentIndex!=(currentArray.length-1)){nav_right.show()}},_finish=function(){if(!$.support.opacity){content.get(0).style.removeAttribute('filter');wrap.get(0).style.removeAttribute('filter')}if(selectedOpts.autoDimensions){content.css('height','auto')}wrap.css('height','auto');if(titleStr&&titleStr.length){title.show()}if(currentOpts.showCloseButton){close.show()}_set_navigation();if(currentOpts.hideOnContentClick){content.bind('click',$.fancybox.close)}if(currentOpts.hideOnOverlayClick){overlay.bind('click',$.fancybox.close)}$(window).bind("resize.fb",$.fancybox.resize);if(currentOpts.centerOnScroll){$(window).bind("scroll.fb",$.fancybox.center)}if(currentOpts.type=='iframe'){$('<iframe id="fancybox-frame" name="fancybox-frame'+new Date().getTime()+'" frameborder="0" hspace="0" '+($.browser.msie?'allowtransparency="true""':'')+' scrolling="'+selectedOpts.scrolling+'" src="'+currentOpts.href+'"></iframe>').appendTo(content)}wrap.show();busy=false;$.fancybox.center();currentOpts.onComplete(currentArray,currentIndex,currentOpts);_preload_images()},_preload_images=function(){var href,objNext;if((currentArray.length-1)>currentIndex){href=currentArray[currentIndex+1].href;if(typeof href!=='undefined'&&href.match(imgRegExp)){objNext=new Image();objNext.src=href}}if(currentIndex>0){href=currentArray[currentIndex-1].href;if(typeof href!=='undefined'&&href.match(imgRegExp)){objNext=new Image();objNext.src=href}}},_draw=function(pos){var dim={width:parseInt(start_pos.width+(final_pos.width-start_pos.width)*pos,10),height:parseInt(start_pos.height+(final_pos.height-start_pos.height)*pos,10),top:parseInt(start_pos.top+(final_pos.top-start_pos.top)*pos,10),left:parseInt(start_pos.left+(final_pos.left-start_pos.left)*pos,10)};if(typeof final_pos.opacity!=='undefined'){dim.opacity=pos<0.5?0.5:pos}wrap.css(dim);content.css({'width':dim.width-currentOpts.padding*2,'height':dim.height-(titleHeight*pos)-currentOpts.padding*2})},_get_viewport=function(){return[$(window).width()-(currentOpts.margin*2),$(window).height()-(currentOpts.margin*2),$(document).scrollLeft()+currentOpts.margin,$(document).scrollTop()+currentOpts.margin]},_get_zoom_to=function(){var view=_get_viewport(),to={},resize=currentOpts.autoScale,double_padding=currentOpts.padding*2,ratio;if(currentOpts.width.toString().indexOf('%')>-1){to.width=parseInt((view[0]*parseFloat(currentOpts.width))/100,10)}else{to.width=currentOpts.width+double_padding}if(currentOpts.height.toString().indexOf('%')>-1){to.height=parseInt((view[1]*parseFloat(currentOpts.height))/100,10)}else{to.height=currentOpts.height+double_padding}if(resize&&(to.width>view[0]||to.height>view[1])){if(selectedOpts.type=='image'||selectedOpts.type=='swf'){ratio=(currentOpts.width)/(currentOpts.height);if((to.width)>view[0]){to.width=view[0];to.height=parseInt(((to.width-double_padding)/ratio)+double_padding,10)}if((to.height)>view[1]){to.height=view[1];to.width=parseInt(((to.height-double_padding)*ratio)+double_padding,10)}}else{to.width=Math.min(to.width,view[0]);to.height=Math.min(to.height,view[1])}}to.top=parseInt(Math.max(view[3]-20,view[3]+((view[1]-to.height-40)*0.5)),10);to.left=parseInt(Math.max(view[2]-20,view[2]+((view[0]-to.width-40)*0.5)),10);return to},_get_obj_pos=function(obj){var pos=obj.offset();pos.top+=parseInt(obj.css('paddingTop'),10)||0;pos.left+=parseInt(obj.css('paddingLeft'),10)||0;pos.top+=parseInt(obj.css('border-top-width'),10)||0;pos.left+=parseInt(obj.css('border-left-width'),10)||0;pos.width=obj.width();pos.height=obj.height();return pos},_get_zoom_from=function(){var orig=selectedOpts.orig?$(selectedOpts.orig):false,from={},pos,view;if(orig&&orig.length){pos=_get_obj_pos(orig);from={width:pos.width+(currentOpts.padding*2),height:pos.height+(currentOpts.padding*2),top:pos.top-currentOpts.padding-20,left:pos.left-currentOpts.padding-20}}else{view=_get_viewport();from={width:currentOpts.padding*2,height:currentOpts.padding*2,top:parseInt(view[3]+view[1]*0.5,10),left:parseInt(view[2]+view[0]*0.5,10)}}return from},_animate_loading=function(){if(!loading.is(':visible')){clearInterval(loadingTimer);return}$('div',loading).css('top',(loadingFrame*-40)+'px');loadingFrame=(loadingFrame+1)%12};$.fn.fancybox=function(options){if(!$(this).length){return this}$(this).data('fancybox',$.extend({},options,($.metadata?$(this).metadata():{}))).unbind('click.fb').bind('click.fb',function(e){e.preventDefault();if(busy){return}busy=true;$(this).blur();selectedArray=[];selectedIndex=0;var rel=$(this).attr('rel')||'';if(!rel||rel==''||rel==='nofollow'){selectedArray.push(this)}else{selectedArray=$("a[rel="+rel+"], area[rel="+rel+"]");selectedIndex=selectedArray.index(this)}_start();return});return this};$.fancybox=function(obj){var opts;if(busy){return}busy=true;opts=typeof arguments[1]!=='undefined'?arguments[1]:{};selectedArray=[];selectedIndex=parseInt(opts.index,10)||0;if($.isArray(obj)){for(var i=0,j=obj.length;i<j;i++){if(typeof obj[i]=='object'){$(obj[i]).data('fancybox',$.extend({},opts,obj[i]))}else{obj[i]=$({}).data('fancybox',$.extend({content:obj[i]},opts))}}selectedArray=jQuery.merge(selectedArray,obj)}else{if(typeof obj=='object'){$(obj).data('fancybox',$.extend({},opts,obj))}else{obj=$({}).data('fancybox',$.extend({content:obj},opts))}selectedArray.push(obj)}if(selectedIndex>selectedArray.length||selectedIndex<0){selectedIndex=0}_start()};$.fancybox.showActivity=function(){clearInterval(loadingTimer);loading.show();loadingTimer=setInterval(_animate_loading,66)};$.fancybox.hideActivity=function(){loading.hide()};$.fancybox.next=function(){return $.fancybox.pos(currentIndex+1)};$.fancybox.prev=function(){return $.fancybox.pos(currentIndex-1)};$.fancybox.pos=function(pos){if(busy){return}pos=parseInt(pos);selectedArray=currentArray;if(pos>-1&&pos<currentArray.length){selectedIndex=pos;_start()}else if(currentOpts.cyclic&&currentArray.length>1){selectedIndex=pos>=currentArray.length?0:currentArray.length-1;_start()}return};$.fancybox.cancel=function(){if(busy){return}busy=true;$.event.trigger('fancybox-cancel');_abort();selectedOpts.onCancel(selectedArray,selectedIndex,selectedOpts);busy=false};$.fancybox.close=function(){if(busy||wrap.is(':hidden')){return}busy=true;if(currentOpts&&false===currentOpts.onCleanup(currentArray,currentIndex,currentOpts)){busy=false;return}_abort();$(close.add(nav_left).add(nav_right)).hide();$(content.add(overlay)).unbind();$(window).unbind("resize.fb scroll.fb");$(document).unbind('keydown.fb');content.find('iframe').attr('src',isIE6&&/^https/i.test(window.location.href||'')?'javascript:void(false)':'about:blank');if(currentOpts.titlePosition!=='inside'){title.empty()}wrap.stop();function _cleanup(){overlay.fadeOut('fast');title.empty().hide();wrap.hide();$.event.trigger('fancybox-cleanup');content.empty();currentOpts.onClosed(currentArray,currentIndex,currentOpts);currentArray=selectedOpts=[];currentIndex=selectedIndex=0;currentOpts=selectedOpts={};busy=false}if(currentOpts.transitionOut=='elastic'){start_pos=_get_zoom_from();var pos=wrap.position();final_pos={top:pos.top,left:pos.left,width:wrap.width(),height:wrap.height()};if(currentOpts.opacity){final_pos.opacity=1}title.empty().hide();fx.prop=1;$(fx).animate({prop:0},{duration:currentOpts.speedOut,easing:currentOpts.easingOut,step:_draw,complete:_cleanup})}else{wrap.fadeOut(currentOpts.transitionOut=='none'?0:currentOpts.speedOut,_cleanup)}};$.fancybox.resize=function(){if(overlay.is(':visible')){overlay.css('height',$(document).height())}$.fancybox.center(true)};$.fancybox.center=function(){var view,align;if(busy){return}align=arguments[0]===true?1:0;view=_get_viewport();if(!align&&(wrap.width()>view[0]||wrap.height()>view[1])){return}wrap.stop().animate({'top':parseInt(Math.max(view[3]-20,view[3]+((view[1]-content.height()-40)*0.5)-currentOpts.padding)),'left':parseInt(Math.max(view[2]-20,view[2]+((view[0]-content.width()-40)*0.5)-currentOpts.padding))},typeof arguments[0]=='number'?arguments[0]:200)};$.fancybox.init=function(){if($("#fancybox-wrap").length){return}$('body').append(tmp=$('<div id="fancybox-tmp"></div>'),loading=$('<div id="fancybox-loading"><div></div></div>'),overlay=$('<div id="fancybox-overlay"></div>'),wrap=$('<div id="fancybox-wrap"></div>'));outer=$('<div id="fancybox-outer"></div>').appendTo(wrap);outer.append(close=$(),content=$('<div id="fancybox-content"></div>'),title=$(),nav_left=$(),nav_right=$());close.click($.fancybox.close);loading.click($.fancybox.cancel);nav_left.click(function(e){e.preventDefault();$.fancybox.prev()});nav_right.click(function(e){e.preventDefault();$.fancybox.next()});if($.fn.mousewheel){wrap.bind('mousewheel.fb',function(e,delta){if(busy){e.preventDefault()}else if($(e.target).get(0).clientHeight==0||$(e.target).get(0).scrollHeight===$(e.target).get(0).clientHeight){e.preventDefault();$.fancybox[delta>0?'prev':'next']()}})}if(!$.support.opacity){wrap.addClass('fancybox-ie')}if(isIE6){loading.addClass('fancybox-ie6');wrap.addClass('fancybox-ie6');$('<iframe id="fancybox-hide-sel-frame" src="'+(/^https/i.test(window.location.href||'')?'javascript:void(false)':'about:blank')+'" scrolling="no" border="0" frameborder="0" tabindex="-1"></iframe>').prependTo(outer)}};$.fn.fancybox.defaults={padding:10,margin:40,opacity:false,modal:false,cyclic:false,scrolling:'auto',width:560,height:340,autoScale:true,autoDimensions:true,centerOnScroll:false,ajax:{},swf:{wmode:'transparent'},hideOnOverlayClick:true,hideOnContentClick:false,overlayShow:true,overlayOpacity:0.7,overlayColor:'#777',titleShow:true,titlePosition:'float',titleFormat:null,titleFromAlt:false,transitionIn:'fade',transitionOut:'fade',speedIn:300,speedOut:300,changeSpeed:300,changeFade:'fast',easingIn:'swing',easingOut:'swing',showCloseButton:true,showNavArrows:true,enableEscapeButton:true,enableKeyboardNav:true,onStart:function(){},onCancel:function(){},onComplete:function(){},onCleanup:function(){},onClosed:function(){},onError:function(){},specialC:null};$(document).ready(function(){$.fancybox.init()})})(jQuery);


//Fancybox 
///------------------------------------------------------
//variables
var closeBox	= $('.close-box').parent(),
	itemLink	= $('.item-ref'),
	trash		= $('.trash');

//determines new class for a button
closeBox.click($.fancybox.close);
closeBox.click(function(e){e.preventDefault();});

//Fancybox initializer
itemLink.fancybox({
	'speedIn'		:	1000,
	'speedOut'		:	500,
	'overlayShow'	:	true,
	'overlayOpacity':	0.85,
	'titleShow'     :	false,
	'overlayColor' 	:	'#000',
	'transitionIn'	:	'elastic',
	'transitionOut'	:	'elastic',
	'easingIn'      :	'easeOutBack',
	'easingOut'     :	'easeInBack',
	'onStart'		:	function(){ $('.item-info,.item-actions,#invitation-form').css('opacity','0').delay(200).animate({ opacity: 1}, 800); },
	'onCleanup'		:	function(){ $('.item-info,.item-actions,#invitation-form').fadeOut(300).delay(350).fadeIn(); }
    
});



///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Custom jQuery Code
$(function(){
	//hides items in the closet after clicking on a trash icon
	trash.click(function(e){
		e.preventDefault();
		$(this).closest('.item').fadeOut(800);
	});
	$('.styled').css('height',32).css('width',205);

	//sent message appearence
	if($.browser.msie){
		$('.confirmation').addClass('ie-fix-none');
		$('.send').click(function(e){
			e.preventDefault();
			$(this).next('.confirmation').removeClass('ie-fix-none').addClass('ie-fix-block');
			$(this).next('.confirmation').animate({ opacity: 1}, 500);
		});
	}else{
		$('.confirmation').css('opacity', 0);
		$('.send').click(function(e){
			e.preventDefault();
			$(this).next('.confirmation').animate({ opacity: 1}, 500);
		});
	}
});





///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

/*!
 * jQuery Cycle Plugin (with Transition Definitions)
 * Examples and documentation at: http://jquery.malsup.com/cycle/
 * Copyright (c) 2007-2010 M. Alsup
 * Version: 2.9997 (13-OCT-2011)
 * Dual licensed under the MIT and GPL licenses.
 * http://jquery.malsup.com/license.html
 * Requires: jQuery v1.3.2 or later
 */
;(function(a){function r(b){function e(b){for(;b&&b.nodeName.toLowerCase()!="html";b=b.parentNode){var c=a.css(b,"background-color");if(c&&c.indexOf("rgb")>=0){var e=c.match(/\d+/g);return"#"+d(e[0])+d(e[1])+d(e[2])}if(c&&c!="transparent")return c}return"#ffffff"}function d(a){a=parseInt(a,10).toString(16);return a.length<2?"0"+a:a}c("applying clearType background-color hack");b.each(function(){a(this).css("background-color",e(this))})}function q(b,c){var d=a(c.pager);a.each(b,function(e,f){a.fn.cycle.createPagerAnchor(e,f,d,b,c)});c.updateActivePagerLink(c.pager,c.startingSlide,c.activePagerClass)}function o(b,c){var d=c?1:-1;var e=b.elements;var f=b.$cont[0],g=f.cycleTimeout;if(g){clearTimeout(g);f.cycleTimeout=0}if(b.random&&d<0){b.randomIndex--;if(--b.randomIndex==-2)b.randomIndex=e.length-2;else if(b.randomIndex==-1)b.randomIndex=e.length-1;b.nextSlide=b.randomMap[b.randomIndex]}else if(b.random){b.nextSlide=b.randomMap[b.randomIndex]}else{b.nextSlide=b.currSlide+d;if(b.nextSlide<0){if(b.nowrap)return false;b.nextSlide=e.length-1}else if(b.nextSlide>=e.length){if(b.nowrap)return false;b.nextSlide=0}}var h=b.onPrevNextEvent||b.prevNextClick;if(a.isFunction(h))h(d>0,b.nextSlide,e[b.nextSlide]);m(e,b,1,c);return false}function n(a,b,d,e){if(d.timeoutFn){var f=d.timeoutFn.call(a,a,b,d,e);while(d.fx!="none"&&f-d.speed<250)f+=d.speed;c("calculated timeout: "+f+"; speed: "+d.speed);if(f!==false)return f}return d.timeout}function m(b,d,e,f){function p(){var a=0,c=d.timeout;if(d.timeout&&!d.continuous){a=n(b[d.currSlide],b[d.nextSlide],d,f);if(d.fx=="shuffle")a-=d.speedOut}else if(d.continuous&&g.cyclePause)a=10;if(a>0)g.cycleTimeout=setTimeout(function(){m(b,d,0,!d.backwards)},a)}if(e&&d.busy&&d.manualTrump){c("manualTrump in go(), stopping active transition");a(b).stop(true,true);d.busy=0}if(d.busy){c("transition active, ignoring new tx request");return}var g=d.$cont[0],h=b[d.currSlide],i=b[d.nextSlide];if(g.cycleStop!=d.stopCount||g.cycleTimeout===0&&!e)return;if(!e&&!g.cyclePause&&!d.bounce&&(d.autostop&&--d.countdown<=0||d.nowrap&&!d.random&&d.nextSlide<d.currSlide)){if(d.end)d.end(d);return}var j=false;if((e||!g.cyclePause)&&d.nextSlide!=d.currSlide){j=true;var k=d.fx;h.cycleH=h.cycleH||a(h).height();h.cycleW=h.cycleW||a(h).width();i.cycleH=i.cycleH||a(i).height();i.cycleW=i.cycleW||a(i).width();if(d.multiFx){if(f&&(d.lastFx==undefined||++d.lastFx>=d.fxs.length))d.lastFx=0;else if(!f&&(d.lastFx==undefined||--d.lastFx<0))d.lastFx=d.fxs.length-1;k=d.fxs[d.lastFx]}if(d.oneTimeFx){k=d.oneTimeFx;d.oneTimeFx=null}a.fn.cycle.resetState(d,k);if(d.before.length)a.each(d.before,function(a,b){if(g.cycleStop!=d.stopCount)return;b.apply(i,[h,i,d,f])});var l=function(){d.busy=0;a.each(d.after,function(a,b){if(g.cycleStop!=d.stopCount)return;b.apply(i,[h,i,d,f])});if(!g.cycleStop){p()}};c("tx firing("+k+"); currSlide: "+d.currSlide+"; nextSlide: "+d.nextSlide);d.busy=1;if(d.fxFn)d.fxFn(h,i,d,l,f,e&&d.fastOnEvent);else if(a.isFunction(a.fn.cycle[d.fx]))a.fn.cycle[d.fx](h,i,d,l,f,e&&d.fastOnEvent);else a.fn.cycle.custom(h,i,d,l,f,e&&d.fastOnEvent)}else{p()}if(j||d.nextSlide==d.currSlide){d.lastSlide=d.currSlide;if(d.random){d.currSlide=d.nextSlide;if(++d.randomIndex==b.length)d.randomIndex=0;d.nextSlide=d.randomMap[d.randomIndex];if(d.nextSlide==d.currSlide)d.nextSlide=d.currSlide==d.slideCount-1?0:d.currSlide+1}else if(d.backwards){var o=d.nextSlide-1<0;if(o&&d.bounce){d.backwards=!d.backwards;d.nextSlide=1;d.currSlide=0}else{d.nextSlide=o?b.length-1:d.nextSlide-1;d.currSlide=o?0:d.nextSlide+1}}else{var o=d.nextSlide+1==b.length;if(o&&d.bounce){d.backwards=!d.backwards;d.nextSlide=b.length-2;d.currSlide=b.length-1}else{d.nextSlide=o?0:d.nextSlide+1;d.currSlide=o?b.length-1:d.nextSlide-1}}}if(j&&d.pager)d.updateActivePagerLink(d.pager,d.currSlide,d.activePagerClass)}function l(b,c){b.addSlide=function(d,e){var f=a(d),g=f[0];if(!b.autostopCount)b.countdown++;c[e?"unshift":"push"](g);if(b.els)b.els[e?"unshift":"push"](g);b.slideCount=c.length;f.css("position","absolute");f[e?"prependTo":"appendTo"](b.$cont);if(e){b.currSlide++;b.nextSlide++}if(!a.support.opacity&&b.cleartype&&!b.cleartypeNoBg)r(f);if(b.fit&&b.width)f.width(b.width);if(b.fit&&b.height&&b.height!="auto")f.height(b.height);g.cycleH=b.fit&&b.height?b.height:f.height();g.cycleW=b.fit&&b.width?b.width:f.width();f.css(b.cssBefore);if(b.pager||b.pagerAnchorBuilder)a.fn.cycle.createPagerAnchor(c.length-1,g,a(b.pager),c,b);if(a.isFunction(b.onAddSlide))b.onAddSlide(f);else f.hide()}}function k(b){var e,f,g=a.fn.cycle.transitions;if(b.fx.indexOf(",")>0){b.multiFx=true;b.fxs=b.fx.replace(/\s*/g,"").split(",");for(e=0;e<b.fxs.length;e++){var h=b.fxs[e];f=g[h];if(!f||!g.hasOwnProperty(h)||!a.isFunction(f)){d("discarding unknown transition: ",h);b.fxs.splice(e,1);e--}}if(!b.fxs.length){d("No valid transitions named; slideshow terminating.");return false}}else if(b.fx=="all"){b.multiFx=true;b.fxs=[];for(p in g){f=g[p];if(g.hasOwnProperty(p)&&a.isFunction(f))b.fxs.push(p)}}if(b.multiFx&&b.randomizeEffects){var i=Math.floor(Math.random()*20)+30;for(e=0;e<i;e++){var j=Math.floor(Math.random()*b.fxs.length);b.fxs.push(b.fxs.splice(j,1)[0])}c("randomized fx sequence: ",b.fxs)}return true}function j(b){b.original={before:[],after:[]};b.original.cssBefore=a.extend({},b.cssBefore);b.original.cssAfter=a.extend({},b.cssAfter);b.original.animIn=a.extend({},b.animIn);b.original.animOut=a.extend({},b.animOut);a.each(b.before,function(){b.original.before.push(this)});a.each(b.after,function(){b.original.after.push(this)})}function i(b,c,f,h,i){var n=a.extend({},a.fn.cycle.defaults,h||{},a.metadata?b.metadata():a.meta?b.data():{});var p=a.isFunction(b.data)?b.data(n.metaAttr):null;if(p)n=a.extend(n,p);if(n.autostop)n.countdown=n.autostopCount||f.length;var s=b[0];b.data("cycle.opts",n);n.$cont=b;n.stopCount=s.cycleStop;n.elements=f;n.before=n.before?[n.before]:[];n.after=n.after?[n.after]:[];if(!a.support.opacity&&n.cleartype)n.after.push(function(){g(this,n)});if(n.continuous)n.after.push(function(){m(f,n,0,!n.backwards)});j(n);if(!a.support.opacity&&n.cleartype&&!n.cleartypeNoBg)r(c);if(b.css("position")=="static")b.css("position","relative");if(n.width)b.width(n.width);if(n.height&&n.height!="auto")b.height(n.height);if(n.startingSlide)n.startingSlide=parseInt(n.startingSlide,10);else if(n.backwards)n.startingSlide=f.length-1;if(n.random){n.randomMap=[];for(var t=0;t<f.length;t++)n.randomMap.push(t);n.randomMap.sort(function(a,b){return Math.random()-.5});n.randomIndex=1;n.startingSlide=n.randomMap[1]}else if(n.startingSlide>=f.length)n.startingSlide=0;n.currSlide=n.startingSlide||0;var u=n.startingSlide;c.css({position:"absolute",top:0,left:0}).hide().each(function(b){var c;if(n.backwards)c=u?b<=u?f.length+(b-u):u-b:f.length-b;else c=u?b>=u?f.length-(b-u):u-b:f.length-b;a(this).css("z-index",c)});a(f[u]).css("opacity",1).show();g(f[u],n);if(n.fit){if(!n.aspect){if(n.width)c.width(n.width);if(n.height&&n.height!="auto")c.height(n.height)}else{c.each(function(){var b=a(this);var c=n.aspect===true?b.width()/b.height():n.aspect;if(n.width&&b.width()!=n.width){b.width(n.width);b.height(n.width/c)}if(n.height&&b.height()<n.height){b.height(n.height);b.width(n.height*c)}})}}if(n.center&&(!n.fit||n.aspect)){c.each(function(){var b=a(this);b.css({"margin-left":n.width?(n.width-b.width())/2+"px":0,"margin-top":n.height?(n.height-b.height())/2+"px":0})})}if(n.center&&!n.fit&&!n.slideResize){c.each(function(){var b=a(this);b.css({"margin-left":n.width?(n.width-b.width())/2+"px":0,"margin-top":n.height?(n.height-b.height())/2+"px":0})})}var v=n.containerResize&&!b.innerHeight();if(v){var w=0,x=0;for(var y=0;y<f.length;y++){var z=a(f[y]),A=z[0],B=z.outerWidth(),C=z.outerHeight();if(!B)B=A.offsetWidth||A.width||z.attr("width");if(!C)C=A.offsetHeight||A.height||z.attr("height");w=B>w?B:w;x=C>x?C:x}if(w>0&&x>0)b.css({width:w+"px",height:x+"px"})}var D=false;if(n.pause)b.hover(function(){D=true;this.cyclePause++;e(s,true)},function(){D&&this.cyclePause--;e(s,true)});if(k(n)===false)return false;var E=false;h.requeueAttempts=h.requeueAttempts||0;c.each(function(){var b=a(this);this.cycleH=n.fit&&n.height?n.height:b.height()||this.offsetHeight||this.height||b.attr("height")||0;this.cycleW=n.fit&&n.width?n.width:b.width()||this.offsetWidth||this.width||b.attr("width")||0;if(b.is("img")){var c=a.browser.msie&&this.cycleW==28&&this.cycleH==30&&!this.complete;var e=a.browser.mozilla&&this.cycleW==34&&this.cycleH==19&&!this.complete;var f=a.browser.opera&&(this.cycleW==42&&this.cycleH==19||this.cycleW==37&&this.cycleH==17)&&!this.complete;var g=this.cycleH==0&&this.cycleW==0&&!this.complete;if(c||e||f||g){if(i.s&&n.requeueOnImageNotLoaded&&++h.requeueAttempts<100){d(h.requeueAttempts," - img slide not loaded, requeuing slideshow: ",this.src,this.cycleW,this.cycleH);setTimeout(function(){a(i.s,i.c).cycle(h)},n.requeueTimeout);E=true;return false}else{d("could not determine size of image: "+this.src,this.cycleW,this.cycleH)}}}return true});if(E)return false;n.cssBefore=n.cssBefore||{};n.cssAfter=n.cssAfter||{};n.cssFirst=n.cssFirst||{};n.animIn=n.animIn||{};n.animOut=n.animOut||{};c.not(":eq("+u+")").css(n.cssBefore);a(c[u]).css(n.cssFirst);if(n.timeout){n.timeout=parseInt(n.timeout,10);if(n.speed.constructor==String)n.speed=a.fx.speeds[n.speed]||parseInt(n.speed,10);if(!n.sync)n.speed=n.speed/2;var F=n.fx=="none"?0:n.fx=="shuffle"?500:250;while(n.timeout-n.speed<F)n.timeout+=n.speed}if(n.easing)n.easeIn=n.easeOut=n.easing;if(!n.speedIn)n.speedIn=n.speed;if(!n.speedOut)n.speedOut=n.speed;n.slideCount=f.length;n.currSlide=n.lastSlide=u;if(n.random){if(++n.randomIndex==f.length)n.randomIndex=0;n.nextSlide=n.randomMap[n.randomIndex]}else if(n.backwards)n.nextSlide=n.startingSlide==0?f.length-1:n.startingSlide-1;else n.nextSlide=n.startingSlide>=f.length-1?0:n.startingSlide+1;if(!n.multiFx){var G=a.fn.cycle.transitions[n.fx];if(a.isFunction(G))G(b,c,n);else if(n.fx!="custom"&&!n.multiFx){d("unknown transition: "+n.fx,"; slideshow terminating");return false}}var H=c[u];if(!n.skipInitializationCallbacks){if(n.before.length)n.before[0].apply(H,[H,H,n,true]);if(n.after.length)n.after[0].apply(H,[H,H,n,true])}if(n.next)a(n.next).bind(n.prevNextEvent,function(){return o(n,1)});if(n.prev)a(n.prev).bind(n.prevNextEvent,function(){return o(n,0)});if(n.pager||n.pagerAnchorBuilder)q(f,n);l(n,f);return n}function h(b){if(b.next)a(b.next).unbind(b.prevNextEvent);if(b.prev)a(b.prev).unbind(b.prevNextEvent);if(b.pager||b.pagerAnchorBuilder)a.each(b.pagerAnchors||[],function(){this.unbind().remove()});b.pagerAnchors=null;if(b.destroy)b.destroy(b)}function g(b,c){if(!a.support.opacity&&c.cleartype&&b.style.filter){try{b.style.removeAttribute("filter")}catch(d){}}}function f(b,c,f){function j(b,c,e){if(!b&&c===true){var f=a(e).data("cycle.opts");if(!f){d("options not found, can not resume");return false}if(e.cycleTimeout){clearTimeout(e.cycleTimeout);e.cycleTimeout=0}m(f.elements,f,1,!f.backwards)}}if(b.cycleStop==undefined)b.cycleStop=0;if(c===undefined||c===null)c={};if(c.constructor==String){switch(c){case"destroy":case"stop":var g=a(b).data("cycle.opts");if(!g)return false;b.cycleStop++;if(b.cycleTimeout)clearTimeout(b.cycleTimeout);b.cycleTimeout=0;g.elements&&a(g.elements).stop();a(b).removeData("cycle.opts");if(c=="destroy")h(g);return false;case"toggle":b.cyclePause=b.cyclePause===1?0:1;j(b.cyclePause,f,b);e(b);return false;case"pause":b.cyclePause=1;e(b);return false;case"resume":b.cyclePause=0;j(false,f,b);e(b);return false;case"prev":case"next":var g=a(b).data("cycle.opts");if(!g){d('options not found, "prev/next" ignored');return false}a.fn.cycle[c](g);return false;default:c={fx:c}}return c}else if(c.constructor==Number){var i=c;c=a(b).data("cycle.opts");if(!c){d("options not found, can not advance slide");return false}if(i<0||i>=c.elements.length){d("invalid slide index: "+i);return false}c.nextSlide=i;if(b.cycleTimeout){clearTimeout(b.cycleTimeout);b.cycleTimeout=0}if(typeof f=="string")c.oneTimeFx=f;m(c.elements,c,1,i>=c.currSlide);return false}return c}function e(b,c,d){var e=a(b).data("cycle.opts");var f=!!b.cyclePause;if(f&&e.paused)e.paused(b,e,c,d);else if(!f&&e.resumed)e.resumed(b,e,c,d)}function d(){window.console&&console.log&&console.log("[cycle] "+Array.prototype.join.call(arguments," "))}function c(b){a.fn.cycle.debug&&d(b)}var b="2.9997";if(a.support==undefined){a.support={opacity:!a.browser.msie}}a.expr[":"].paused=function(a){return a.cyclePause};a.fn.cycle=function(b,e){var g={s:this.selector,c:this.context};if(this.length===0&&b!="stop"){if(!a.isReady&&g.s){d("DOM not ready, queuing slideshow");a(function(){a(g.s,g.c).cycle(b,e)});return this}d("terminating; zero elements found by selector"+(a.isReady?"":" (DOM not ready)"));return this}return this.each(function(){var h=f(this,b,e);if(h===false)return;h.updateActivePagerLink=h.updateActivePagerLink||a.fn.cycle.updateActivePagerLink;if(this.cycleTimeout)clearTimeout(this.cycleTimeout);this.cycleTimeout=this.cyclePause=0;var j=a(this);var k=h.slideExpr?a(h.slideExpr,this):j.children();var l=k.get();var o=i(j,k,l,h,g);if(o===false)return;if(l.length<2){d("terminating; too few slides: "+l.length);return}var p=o.continuous?10:n(l[o.currSlide],l[o.nextSlide],o,!o.backwards);if(p){p+=o.delay||0;if(p<10)p=10;c("first timeout: "+p);this.cycleTimeout=setTimeout(function(){m(l,o,0,!h.backwards)},p)}})};a.fn.cycle.resetState=function(b,c){c=c||b.fx;b.before=[];b.after=[];b.cssBefore=a.extend({},b.original.cssBefore);b.cssAfter=a.extend({},b.original.cssAfter);b.animIn=a.extend({},b.original.animIn);b.animOut=a.extend({},b.original.animOut);b.fxFn=null;a.each(b.original.before,function(){b.before.push(this)});a.each(b.original.after,function(){b.after.push(this)});var d=a.fn.cycle.transitions[c];if(a.isFunction(d))d(b.$cont,a(b.elements),b)};a.fn.cycle.updateActivePagerLink=function(b,c,d){a(b).each(function(){a(this).children().removeClass(d).eq(c).addClass(d)})};a.fn.cycle.next=function(a){o(a,1)};a.fn.cycle.prev=function(a){o(a,0)};a.fn.cycle.createPagerAnchor=function(b,d,f,g,h){var i;if(a.isFunction(h.pagerAnchorBuilder)){i=h.pagerAnchorBuilder(b,d);c("pagerAnchorBuilder("+b+", el) returned: "+i)}else i='<a href="#">'+(b+1)+"</a>";if(!i)return;var j=a(i);if(j.parents("body").length===0){var k=[];if(f.length>1){f.each(function(){var b=j.clone(true);a(this).append(b);k.push(b[0])});j=a(k)}else{j.appendTo(f)}}h.pagerAnchors=h.pagerAnchors||[];h.pagerAnchors.push(j);var l=function(c){c.preventDefault();h.nextSlide=b;var d=h.$cont[0],e=d.cycleTimeout;if(e){clearTimeout(e);d.cycleTimeout=0}var f=h.onPagerEvent||h.pagerClick;if(a.isFunction(f))f(h.nextSlide,g[h.nextSlide]);m(g,h,1,h.currSlide<b)};if(/mouseenter|mouseover/i.test(h.pagerEvent)){j.hover(l,function(){})}else{j.bind(h.pagerEvent,l)}if(!/^click/.test(h.pagerEvent)&&!h.allowPagerClickBubble)j.bind("click.cycle",function(){return false});var n=h.$cont[0];var o=false;if(h.pauseOnPagerHover){j.hover(function(){o=true;n.cyclePause++;e(n,true,true)},function(){o&&n.cyclePause--;e(n,true,true)})}};a.fn.cycle.hopsFromLast=function(a,b){var c,d=a.lastSlide,e=a.currSlide;if(b)c=e>d?e-d:a.slideCount-d;else c=e<d?d-e:d+a.slideCount-e;return c};a.fn.cycle.commonReset=function(b,c,d,e,f,g){a(d.elements).not(b).hide();if(typeof d.cssBefore.opacity=="undefined")d.cssBefore.opacity=1;d.cssBefore.display="block";if(d.slideResize&&e!==false&&c.cycleW>0)d.cssBefore.width=c.cycleW;if(d.slideResize&&f!==false&&c.cycleH>0)d.cssBefore.height=c.cycleH;d.cssAfter=d.cssAfter||{};d.cssAfter.display="none";a(b).css("zIndex",d.slideCount+(g===true?1:0));a(c).css("zIndex",d.slideCount+(g===true?0:1))};a.fn.cycle.custom=function(b,c,d,e,f,g){var h=a(b),i=a(c);var j=d.speedIn,k=d.speedOut,l=d.easeIn,m=d.easeOut;i.css(d.cssBefore);if(g){if(typeof g=="number")j=k=g;else j=k=1;l=m=null}var n=function(){i.animate(d.animIn,j,l,function(){e()})};h.animate(d.animOut,k,m,function(){h.css(d.cssAfter);if(!d.sync)n()});if(d.sync)n()};a.fn.cycle.transitions={fade:function(b,c,d){c.not(":eq("+d.currSlide+")").css("opacity",0);d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d);d.cssBefore.opacity=0});d.animIn={opacity:1};d.animOut={opacity:0};d.cssBefore={top:0,left:0}}};a.fn.cycle.ver=function(){return b};a.fn.cycle.defaults={activePagerClass:"activeSlide",after:null,allowPagerClickBubble:false,animIn:null,animOut:null,aspect:false,autostop:0,autostopCount:0,backwards:false,before:null,center:null,cleartype:!a.support.opacity,cleartypeNoBg:false,containerResize:1,continuous:0,cssAfter:null,cssBefore:null,delay:0,easeIn:null,easeOut:null,easing:null,end:null,fastOnEvent:0,fit:0,fx:"fade",fxFn:null,height:"auto",manualTrump:true,metaAttr:"cycle",next:null,nowrap:0,onPagerEvent:null,onPrevNextEvent:null,pager:null,pagerAnchorBuilder:null,pagerEvent:"click.cycle",pause:0,pauseOnPagerHover:0,prev:null,prevNextEvent:"click.cycle",random:0,randomizeEffects:1,requeueOnImageNotLoaded:true,requeueTimeout:250,rev:0,shuffle:null,skipInitializationCallbacks:false,slideExpr:null,slideResize:1,speed:1e3,speedIn:null,speedOut:null,startingSlide:0,sync:1,timeout:4e3,timeoutFn:null,updateActivePagerLink:null,width:null}})(jQuery);(function(a){a.fn.cycle.transitions.none=function(b,c,d){d.fxFn=function(b,c,d,e){a(c).show();a(b).hide();e()}};a.fn.cycle.transitions.fadeout=function(b,c,d){c.not(":eq("+d.currSlide+")").css({display:"block",opacity:1});d.before.push(function(b,c,d,e,f,g){a(b).css("zIndex",d.slideCount+(!g===true?1:0));a(c).css("zIndex",d.slideCount+(!g===true?0:1))});d.animIn.opacity=1;d.animOut.opacity=0;d.cssBefore.opacity=1;d.cssBefore.display="block";d.cssAfter.zIndex=0};a.fn.cycle.transitions.scrollUp=function(b,c,d){b.css("overflow","hidden");d.before.push(a.fn.cycle.commonReset);var e=b.height();d.cssBefore.top=e;d.cssBefore.left=0;d.cssFirst.top=0;d.animIn.top=0;d.animOut.top=-e};a.fn.cycle.transitions.scrollDown=function(b,c,d){b.css("overflow","hidden");d.before.push(a.fn.cycle.commonReset);var e=b.height();d.cssFirst.top=0;d.cssBefore.top=-e;d.cssBefore.left=0;d.animIn.top=0;d.animOut.top=e};a.fn.cycle.transitions.scrollLeft=function(b,c,d){b.css("overflow","hidden");d.before.push(a.fn.cycle.commonReset);var e=b.width();d.cssFirst.left=0;d.cssBefore.left=e;d.cssBefore.top=0;d.animIn.left=0;d.animOut.left=0-e};a.fn.cycle.transitions.scrollRight=function(b,c,d){b.css("overflow","hidden");d.before.push(a.fn.cycle.commonReset);var e=b.width();d.cssFirst.left=0;d.cssBefore.left=-e;d.cssBefore.top=0;d.animIn.left=0;d.animOut.left=e};a.fn.cycle.transitions.scrollHorz=function(b,c,d){b.css("overflow","hidden").width();d.before.push(function(b,c,d,e){if(d.rev)e=!e;a.fn.cycle.commonReset(b,c,d);d.cssBefore.left=e?c.cycleW-1:1-c.cycleW;d.animOut.left=e?-b.cycleW:b.cycleW});d.cssFirst.left=0;d.cssBefore.top=0;d.animIn.left=0;d.animOut.top=0};a.fn.cycle.transitions.scrollVert=function(b,c,d){b.css("overflow","hidden");d.before.push(function(b,c,d,e){if(d.rev)e=!e;a.fn.cycle.commonReset(b,c,d);d.cssBefore.top=e?1-c.cycleH:c.cycleH-1;d.animOut.top=e?b.cycleH:-b.cycleH});d.cssFirst.top=0;d.cssBefore.left=0;d.animIn.top=0;d.animOut.left=0};a.fn.cycle.transitions.slideX=function(b,c,d){d.before.push(function(b,c,d){a(d.elements).not(b).hide();a.fn.cycle.commonReset(b,c,d,false,true);d.animIn.width=c.cycleW});d.cssBefore.left=0;d.cssBefore.top=0;d.cssBefore.width=0;d.animIn.width="show";d.animOut.width=0};a.fn.cycle.transitions.slideY=function(b,c,d){d.before.push(function(b,c,d){a(d.elements).not(b).hide();a.fn.cycle.commonReset(b,c,d,true,false);d.animIn.height=c.cycleH});d.cssBefore.left=0;d.cssBefore.top=0;d.cssBefore.height=0;d.animIn.height="show";d.animOut.height=0};a.fn.cycle.transitions.shuffle=function(b,c,d){var e,f=b.css("overflow","visible").width();c.css({left:0,top:0});d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,true,true)});if(!d.speedAdjusted){d.speed=d.speed/2;d.speedAdjusted=true}d.random=0;d.shuffle=d.shuffle||{left:-f,top:15};d.els=[];for(e=0;e<c.length;e++)d.els.push(c[e]);for(e=0;e<d.currSlide;e++)d.els.push(d.els.shift());d.fxFn=function(b,c,d,e,f){if(d.rev)f=!f;var g=f?a(b):a(c);a(c).css(d.cssBefore);var h=d.slideCount;g.animate(d.shuffle,d.speedIn,d.easeIn,function(){var c=a.fn.cycle.hopsFromLast(d,f);for(var i=0;i<c;i++)f?d.els.push(d.els.shift()):d.els.unshift(d.els.pop());if(f){for(var j=0,k=d.els.length;j<k;j++)a(d.els[j]).css("z-index",k-j+h)}else{var l=a(b).css("z-index");g.css("z-index",parseInt(l,10)+1+h)}g.animate({left:0,top:0},d.speedOut,d.easeOut,function(){a(f?this:b).hide();if(e)e()})})};a.extend(d.cssBefore,{display:"block",opacity:1,top:0,left:0})};a.fn.cycle.transitions.turnUp=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,false);d.cssBefore.top=c.cycleH;d.animIn.height=c.cycleH;d.animOut.width=c.cycleW});d.cssFirst.top=0;d.cssBefore.left=0;d.cssBefore.height=0;d.animIn.top=0;d.animOut.height=0};a.fn.cycle.transitions.turnDown=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,false);d.animIn.height=c.cycleH;d.animOut.top=b.cycleH});d.cssFirst.top=0;d.cssBefore.left=0;d.cssBefore.top=0;d.cssBefore.height=0;d.animOut.height=0};a.fn.cycle.transitions.turnLeft=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,true);d.cssBefore.left=c.cycleW;d.animIn.width=c.cycleW});d.cssBefore.top=0;d.cssBefore.width=0;d.animIn.left=0;d.animOut.width=0};a.fn.cycle.transitions.turnRight=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,true);d.animIn.width=c.cycleW;d.animOut.left=b.cycleW});a.extend(d.cssBefore,{top:0,left:0,width:0});d.animIn.left=0;d.animOut.width=0};a.fn.cycle.transitions.zoom=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,false,true);d.cssBefore.top=c.cycleH/2;d.cssBefore.left=c.cycleW/2;a.extend(d.animIn,{top:0,left:0,width:c.cycleW,height:c.cycleH});a.extend(d.animOut,{width:0,height:0,top:b.cycleH/2,left:b.cycleW/2})});d.cssFirst.top=0;d.cssFirst.left=0;d.cssBefore.width=0;d.cssBefore.height=0};a.fn.cycle.transitions.fadeZoom=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,false);d.cssBefore.left=c.cycleW/2;d.cssBefore.top=c.cycleH/2;a.extend(d.animIn,{top:0,left:0,width:c.cycleW,height:c.cycleH})});d.cssBefore.width=0;d.cssBefore.height=0;d.animOut.opacity=0};a.fn.cycle.transitions.blindX=function(b,c,d){var e=b.css("overflow","hidden").width();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d);d.animIn.width=c.cycleW;d.animOut.left=b.cycleW});d.cssBefore.left=e;d.cssBefore.top=0;d.animIn.left=0;d.animOut.left=e};a.fn.cycle.transitions.blindY=function(b,c,d){var e=b.css("overflow","hidden").height();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d);d.animIn.height=c.cycleH;d.animOut.top=b.cycleH});d.cssBefore.top=e;d.cssBefore.left=0;d.animIn.top=0;d.animOut.top=e};a.fn.cycle.transitions.blindZ=function(b,c,d){var e=b.css("overflow","hidden").height();var f=b.width();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d);d.animIn.height=c.cycleH;d.animOut.top=b.cycleH});d.cssBefore.top=e;d.cssBefore.left=f;d.animIn.top=0;d.animIn.left=0;d.animOut.top=e;d.animOut.left=f};a.fn.cycle.transitions.growX=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,true);d.cssBefore.left=this.cycleW/2;d.animIn.left=0;d.animIn.width=this.cycleW;d.animOut.left=0});d.cssBefore.top=0;d.cssBefore.width=0};a.fn.cycle.transitions.growY=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,false);d.cssBefore.top=this.cycleH/2;d.animIn.top=0;d.animIn.height=this.cycleH;d.animOut.top=0});d.cssBefore.height=0;d.cssBefore.left=0};a.fn.cycle.transitions.curtainX=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,false,true,true);d.cssBefore.left=c.cycleW/2;d.animIn.left=0;d.animIn.width=this.cycleW;d.animOut.left=b.cycleW/2;d.animOut.width=0});d.cssBefore.top=0;d.cssBefore.width=0};a.fn.cycle.transitions.curtainY=function(b,c,d){d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,false,true);d.cssBefore.top=c.cycleH/2;d.animIn.top=0;d.animIn.height=c.cycleH;d.animOut.top=b.cycleH/2;d.animOut.height=0});d.cssBefore.height=0;d.cssBefore.left=0};a.fn.cycle.transitions.cover=function(b,c,d){var e=d.direction||"left";var f=b.css("overflow","hidden").width();var g=b.height();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d);if(e=="right")d.cssBefore.left=-f;else if(e=="up")d.cssBefore.top=g;else if(e=="down")d.cssBefore.top=-g;else d.cssBefore.left=f});d.animIn.left=0;d.animIn.top=0;d.cssBefore.top=0;d.cssBefore.left=0};a.fn.cycle.transitions.uncover=function(b,c,d){var e=d.direction||"left";var f=b.css("overflow","hidden").width();var g=b.height();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,true,true);if(e=="right")d.animOut.left=f;else if(e=="up")d.animOut.top=-g;else if(e=="down")d.animOut.top=g;else d.animOut.left=-f});d.animIn.left=0;d.animIn.top=0;d.cssBefore.top=0;d.cssBefore.left=0};a.fn.cycle.transitions.toss=function(b,c,d){var e=b.css("overflow","visible").width();var f=b.height();d.before.push(function(b,c,d){a.fn.cycle.commonReset(b,c,d,true,true,true);if(!d.animOut.left&&!d.animOut.top)a.extend(d.animOut,{left:e*2,top:-f/2,opacity:0});else d.animOut.opacity=0});d.cssBefore.left=0;d.cssBefore.top=0;d.animIn.left=0};a.fn.cycle.transitions.wipe=function(b,c,d){var e=b.css("overflow","hidden").width();var f=b.height();d.cssBefore=d.cssBefore||{};var g;if(d.clip){if(/l2r/.test(d.clip))g="rect(0px 0px "+f+"px 0px)";else if(/r2l/.test(d.clip))g="rect(0px "+e+"px "+f+"px "+e+"px)";else if(/t2b/.test(d.clip))g="rect(0px "+e+"px 0px 0px)";else if(/b2t/.test(d.clip))g="rect("+f+"px "+e+"px "+f+"px 0px)";else if(/zoom/.test(d.clip)){var h=parseInt(f/2,10);var i=parseInt(e/2,10);g="rect("+h+"px "+i+"px "+h+"px "+i+"px)"}}d.cssBefore.clip=d.cssBefore.clip||g||"rect(0px 0px 0px 0px)";var j=d.cssBefore.clip.match(/(\d+)/g);var k=parseInt(j[0],10),l=parseInt(j[1],10),m=parseInt(j[2],10),n=parseInt(j[3],10);d.before.push(function(b,c,d){if(b==c)return;var g=a(b),h=a(c);a.fn.cycle.commonReset(b,c,d,true,true,false);d.cssAfter.display="block";var i=1,j=parseInt(d.speedIn/13,10)-1;(function o(){var a=k?k-parseInt(i*(k/j),10):0;var b=n?n-parseInt(i*(n/j),10):0;var c=m<f?m+parseInt(i*((f-m)/j||1),10):f;var d=l<e?l+parseInt(i*((e-l)/j||1),10):e;h.css({clip:"rect("+a+"px "+d+"px "+c+"px "+b+"px)"});i++<=j?setTimeout(o,13):g.css("display","none")})()});a.extend(d.cssBefore,{display:"block",opacity:1,top:0,left:0});d.animIn={left:0};d.animOut={left:0}}})(jQuery)

/// Carousel initializer and parameters
//

$('#rotator').cycle({
    fx			:	'scrollHorz',
	prev		:	'#prev',
	next		:	'#next',
    speed		:	2000,
    timeout		:	0,
	cleartype	:	true,
	onPrevNextEvent: function(isNext, zeroBasedSlideIndex, slideElement) {
		$('.blocker').css('z-index',5);
	},
	after: function(currSlideElement, nextSlideElement, options, forwardFlag) {
		$('.blocker').css('z-index',0);
	}
});


//Carousel messed up list item fix
//
$('#rotator').find('.item-list').eq(0).css('position','relative');

if($.browser.msie){
	$('.item').find('.no,.hanger').addClass('ie-icon-link');
}


///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

// Footer down push
function getWindowHeight() {
	var windowHeight = 0;
	if (typeof(window.innerHeight) == 'number') {
		windowHeight = window.innerHeight;
	}
	else {
		if (document.documentElement && document.documentElement.clientHeight) {
			windowHeight = document.documentElement.clientHeight;
		}
		else {
			if (document.body && document.body.clientHeight) {
				windowHeight = document.body.clientHeight;
			}
		}
	}
	return windowHeight;
}
function setFooter() {
	if (document.getElementById) {
		var windowHeight = getWindowHeight();
		if (windowHeight > 0) {
			var contentHeight = document.getElementById('main').offsetHeight;
			var footerElement = document.getElementById('footer');
			var footerHeight  = footerElement.offsetHeight;
			if (windowHeight - (contentHeight + footerHeight) >= 0) {
				footerElement.style.position = 'relative';
				footerElement.style.top = (windowHeight - (contentHeight + footerHeight)) + 'px';
			}
			else {
				footerElement.style.position = 'static';
			}
		}
	}
}

if (!document.getElementById('homepage')
	&& !document.getElementById('welcome')
	&& !document.getElementById('thank-you')){
	window.onload	= function(){
		setFooter();
	}
	window.onresize	= function(){
		setFooter();
	}	
}


///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------

// Given email field is valid ? Return true : Display given error, return false
function mailCheck(emailField, validFunc, errorFunc, errMsg) {
	var filter = /^.+@.+\..{2,4}$/
	var email = emailField.value;
	// Pass
	if (filter.test(email) && email != "") {
		validFunc([emailField]);
		return true;
	}
	else if(isEmpty(email)) {
		emailField.value = emailField.defaultValue;
	}
	// Fail
	else {
		errorFunc([emailField], errMsg);
		return false;
	}
}
// Check if fields are equal, execute appropriate function
function validCheck(fieldA, fieldB, validFunc, errorFunc, errMsg){
	if(fieldA.value == fieldB.value && fieldA.value != fieldA.defaultValue){
		validFunc([fieldA, fieldB]);
		return true;
	}
	else {
		errorFunc([fieldA, fieldB], errMsg);
		return false;
	}
}
// Check if fields are equal, execute appropriate function
function filledCheck(field, validFunc, errorFunc, errMsg){
	if(field.value != "" && field.value != null && field.value != field.defaultValue && !isEmpty(field.value)){
		validFunc([field]);
		return true;
	}
	else {
		errorFunc([field], errMsg);
		return false;
	}
}
// Wait list valid form function
function waitValid() {
	//$('#waitlist-form .btn').removeAttr('disabled');
	$('#waitlist-error').animate({"opacity": "0"},"fast", function(){
		$('#waitlist-form').css({'padding-bottom' : '25px', 'margin-bottom' : '0px'});
		$('#waitlist-error').css('display', 'none');
	});
}
// Wait list erroneous form function
function waitError() {
	$('#waitlist-form').css({'padding-bottom' : '0px', 'margin-bottom' : '-3px'});
	$('#waitlist-error').css('display', 'inline');
	$('#waitlist-error').animate({"opacity": "1"},"fast");
	//$('#waitlist-form .btn').attr('disabled', 'disabled');
}

function bigValid(fields){
	for(tar in fields){
		$(fields[tar]).removeClass('field-error');
	}
	$('#bigform-error').animate({"opacity": "0"}, "fast", function(){
		$('#bigform-error').css('display', 'none');
		$('.acct .password-field').css('margin-bottom', '40px');
	});
}

function bigError(fields, msg){
	for(tar in fields){
		$(fields[tar]).addClass('field-error');
	}
	$('#bigform-error').stop();
	$('#bigform-error').animate({"opacity": "1"}, "fast", function(){
		changeError($('#bigform-error')[0], msg);
		$('.acct .password-field').css('margin-bottom', '0px');
		$('#bigform-error').css('display', 'inline');
	});
}

function bigformCheck(thefield){
	// Restore defaults if blank
	if(isEmpty(thefield.value)){
		restoreInput(thefield);
		// If an error alredy being displayed, skip
		if($('#bigform-error').css('display') == 'inline') {
			return;
		}
		// If a required field, continue validation check
		if(thefield.name != "firstname" && thefield.name != "lastname" && thefield.name != "password" && thefield.name != "validate-password"){
			return;
		}
	}
	switch(thefield.name){
		case 'postal-code':
			// Skip on zip code
			return;
			break;
		case 'firstname':
			// No first name filled out error
			filledCheck(thefield, bigValid, bigError, "Stella wants to know you on a first name basis")
			break;
		case 'lastname':
			// No last name filled out error
			filledCheck(thefield, bigValid, bigError, "Stella wants to know you on a last name basis")
			break;
		case 'email':
			// Email invalid error
			if (mailCheck(thefield, bigValid, bigError, "Stella can't reach you there") && !isDefault($('input[name=validate-email]')[0])){
				// Email mismatch error
				validCheck(thefield, $('input[name=validate-email]')[0], bigValid, bigError, "Your email address doesn't match");
			}
			break;
		case 'validate-email':
			// Email invalid error
			if (validCheck(thefield, $('input[name=email]')[0], bigValid, bigError, "Your email address doesn't match")){
				// Email mismatch error
				mailCheck(thefield, bigValid, bigError, "Stella can't reach you there");
			}
			break;
		case 'password':
			if(!isDefault($('input[name=validate-password]')[0])){
				// Password mismatch error
				validCheck(thefield, $('input[name=validate-password]')[0], bigValid, bigError, "Your password doesn't match");
			}
			break;
		case 'validate-password':
			if(!isDefault($('input[name=password]')[0])){
				// Password mismatch error
				validCheck(thefield, $('input[name=password]')[0], bigValid, bigError, "Your password doesn't match");
			}
			break;
		default:
			// Check entire form: email valid, emails and passwords match, name filled out
			if(mailCheck($('input[name=email]')[0], bigValid, bigError, "Stella can't reach you there")){
				if(filledCheck($('input[name=firstname]')[0], bigValid, bigError, "Stella wants to know you on a first name basis")){
					if(filledCheck($('input[name=lastname]')[0], bigValid, bigError, "Stella wants to know you on a last name basis")){
						if(validCheck($('input[name=email]')[0], $('input[name=validate-email]')[0], bigValid, bigError, "Your email email doesn't match")){
							validCheck($('input[name=password]')[0], $('input[name=validate-password]')[0], bigValid, bigError, "Your email password doesn't match");
						}
					}
				}
			}
	}
}

function changeError(target, message){
	target.innerHTML = message;
}

// Submit button check form, supress default if invalid
$('#account-form .btn').click(function(event){
	mailCheck($('#account-form .txt')[0], function(){}, function(){event.preventDefault();});
});

$('#waitlist-form .btn').click(function(event){
	bigformCheck();
});

function submitCheck(target){
	var formCheck = mailCheck(target, function(){}, function(){});
}


///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Auto-complete jQuery Code
$(function() {

	//Source for tags, create your own if you need 
	var availableTags = [
		'ActionScript',
		'AppleScript',
		'Asp',
		'BASIC',
		'C',
		'C++',
		'Clojure',
		'COBOL',
		'ColdFusion',
		'Erlang',
		'Fortran',
		'Groovy',
		'Haskell',
		'Java',
		'JavaScript',
		'Lisp',
		'Perl',
		'PHP',
		'Python',
		'Ruby',
		'Scala',
		'Scheme',
		'aaa',
		'aab',
		'aba',
		'baa',
		'abb',
		'bab',
		'bba',
		'aaaa',
		'aaab',
		'aaba',
		'abaa',
		'baaa',
		'aabb'
	];

	//Some other choices
	var someOtherAvailableTags = [
		'True Religion',
		'Levis',
		'Diesel',
		'Joes',
		'Calvin',
		'Jeans'
	];

$('#admirers-auto-complete').autocomplete({

	//select a field
	appendTo: '#admirer-search-form',

	//Array that holds tags
	source: availableTags,

	//Sorting of auto complete list
	open: function(event, ui){
		var mylist = $('.ui-autocomplete');
		var listitems = mylist.children('li').get();
		listitems.sort(function(a, b) {
		   var compA = $(a).text().toUpperCase();
		   var compB = $(b).text().toUpperCase();
		   return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
		});
		$.each(listitems, function(idx, itm) { mylist.append(itm); });
	}
});

$('#welcome-auto-compplete').autocomplete({

	//select a field
	appendTo: '#welcome .designer-field',

	//Array that holds tags
	source: someOtherAvailableTags,

	//Sorting of auto complete list
	open: function(event, ui){

		//Sorting of auto complete list
		var mylist = $('.ui-autocomplete');
		var listitems = mylist.children('li').get();
		listitems.sort(function(a, b) {
		   var compA = $(a).text().toUpperCase();
		   var compB = $(b).text().toUpperCase();
		   return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
		});
		$.each(listitems, function(idx, itm) { mylist.append(itm); });
	}
});


///------------------------------------------------------ Plugin/Module Separator ------------------------------------------------------
//Add racks based on keypress or

var inpLstFld = $('#input-list-field'),
	newAddLst = $('#new-shared-add'),
	newAddLnk = $('#new-shared');
inpLstFld.keypress(function(e){
	if(e.keyCode == 13) {
    	newAddLst.append($('<li>', { text: inpLstFld.val() }));
		$(this).val('');
	}
});

newAddLnk.find('.plus').click(function(e){
	newAddLst.append($('<li>', { text: inpLstFld.val() }));
	inpLstFld.val('');
	e.preventDefault();
});

});








