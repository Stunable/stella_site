$(document).ready(function(){  
    var name = ".left-panel";  
    var menuYloc = null;  
    menuYloc = parseInt($(name).css("top").substring(0,$(name).css("top").indexOf("px")))
    console.log(name)
      $(window).scroll(function () {
          if ($(document).scrollTop() == 0) {
              var offset = menuYloc+$(document).scrollTop()+"px";
              $(name).animate({top:offset},{duration:250,queue:false});  
          }
          if ($(document).scrollTop() > 400) {
              var offset = menuYloc-100+$(document).scrollTop()+"px";
              $(name).animate({top:offset},{duration:250,queue:false});  
          } 
      });
});