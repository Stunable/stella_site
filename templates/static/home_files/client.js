// JavaScript Document

// CLEAR TEXT INPUTS OF DEFAULT VALUE ON FOCUS
    function clearInput(textField) {
    if (textField.value == textField.defaultValue) {
        textField.value = "";
     }
	}
// RESTORE TEXT INPUT DEFAULT VALUE ON BLUR
	function restoreInput(textField){
		if (textField.value == ""){
			textField.value = textField.defaultValue;
		}
	}
	
	
// MAKE SELECT BOXES (DROP-DOWNS) PRETTY
(function($){
 $.fn.extend({
 
 	customStyle : function(options) {
	  if(!$.browser.msie || ($.browser.msie&&$.browser.version>6)){
	  return this.each(function() {
	  
			var currentSelected = $(this).find(':selected');
			$(this).after('<span class="customStyleSelectBox"><span class="customStyleSelectBoxInner">'+currentSelected.text()+'</span></span>').css({position:'absolute', opacity:0,fontSize:'0.86em'});
			var selectBoxSpan = $(this).next();
			var selectBoxWidth = parseInt($(this).width()) - parseInt(selectBoxSpan.css('padding-left')) -parseInt(selectBoxSpan.css('padding-right'));			
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
})(jQuery);


$(function(){

$('select.styled').customStyle();

});


// MODAL WINDOWS
//function overlay() {
//	el = document.getElementById("overlay");
//	el.style.visibility = (el.style.visibility == "visible") ? "hidden" : "visible";
//}