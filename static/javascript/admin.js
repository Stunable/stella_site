
var ac_cache={};

var ac_callbacks = {

            'assign':function(el,data){
                $(el.data('val_target')).val(data.value);
                el.val(data.label)

            },
            'navigate':function(el,data){
                window.location = el.data('href')+data.value
            }
            ,'assign_combo':function(el,data){
                $(el.data('type_target')).val(data.type);
                $(el.data('val_target')).val(data.value);
                el.val(data.label)        
            }


        }

var init_AC = function(selection){

      $.each(selection,function(){


      
        var $t = $(this);
        
        $t.autocomplete({

          select: function( event, ui ) {
            if ($t.data('action')){
                ac_callbacks[$t.data('action')]($t,ui.item)
            }

            // $.post($(this).data('href'),{'action':$(this).data('action'),'target':$(this).data('target'),'value':ui.item.value},function(response){
            //     if (response.result || response.success){
            //         if (response.callback){
            //             ac_callbacks[response.callback](response.data)
            //         }
            //     }

            // },'json')
            return false;
          },
          minLength:parseInt($t.data('min')) || 4,
          delay: 500,

          source: function( request, response ) {
            var term = request.term;
            if ( term in ac_cache ) {
              response( ac_cache[ term ] );
              return;
            }
            $.getJSON( "/lookups/"+$t.data('app')+"/"+$t.data('model'), request, function( data, status, xhr ) {
              ac_cache[ term ] = data;
              response( data );

              console.log(data)
            },'json');
          },
        open: function(){
            $t.autocomplete( "widget" ).css('z-index',1000);
            // console.log($(this).autocomplete('widget'));
            return false;
        },
        appendTo:$t.parent()
          
        });

        if ($t.hasClass('combo_input')){
           if($($t.data('type_target')).val() && $($t.data('val_target')).val()){
                $.get( "/reverselookup/"+$($t.data('type_target')).val()+"/"+$($t.data('val_target')).val(), function( data) {
                    $t.val(data.label)
                },'json')
           }
        }

        if ($t.hasClass('single_input')){
           if($($t.data('val_target')).val()){
                $.get( "/reverselookup/"+$t.data('app')+'-'+$t.data('model')+"/"+$($t.data('val_target')).val(), function( data) {
                    $t.val(data.label)
                },'json')
           }
        }
    })

}

        
       
$(document).ready(function(){
	$('.image select').ImageSelect();
   $('select[name=image]').ImageSelect(); 
   $('select[name=featured_image]').ImageSelect(); 
   $('.imageselector').ImageSelect();


   function split( val ) {
      return val.split( /,\s*/ );
    }


    function extractLast( term ) {
      return split( term ).pop();
    }
 
    $( "#id_tags" )
      // don't navigate away from the field on tab when selecting an item
      .bind( "keydown", function( event ) {
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).data( "ui-autocomplete" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        source: function( request, response ) {
          $.getJSON( "/lookups/tagging/tag", {
            term: extractLast( request.term )
          }, response );
        },
        search: function() {
          // custom minLength
          var term = extractLast( this.value );
          if ( term.length < 2 ) {
            return false; 
          }
        },
        focus: function() {
          // prevent value inserted on focus
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          // remove the current input
          terms.pop();
          // add the selected item
          terms.push( ui.item.label );
          // add placeholder to get the comma-and-space at the end
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });


      $('.stunable_search-usersearchtab #id_content_type').closest('.form-row').hide()
        var f = $('.stunable_search-usersearchtab #id_object_id').closest('.form-row')
        f.hide()
        f.after('<div class="form-row"><label for="id_object_type_id_combo">Tab Source Object:</label> <input data-val_target="#id_object_id" data-type_target="#id_content_type" data-min="4" data-action="assign_combo" data-app="specialcombo" data-model="usersearchtab" class="ac_search combo_input" type="text" id="id_object_type_id_combo" style="width:300px"></div>')

        init_AC($('.ac_search'));

})