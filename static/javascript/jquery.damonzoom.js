// the semi-colon before function invocation is a safety net against concatenated
// scripts and/or other plugins which may not be closed properly.
;(function ( $, window, document, undefined ) {

    // undefined is used here as the undefined global variable in ECMAScript 3 is
    // mutable (ie. it can be changed by someone else). undefined isn't really being
    // passed in so we can ensure the value of it is truly undefined. In ES5, undefined
    // can no longer be modified.

    // window and document are passed through as local variable rather than global
    // as this (slightly) quickens the resolution process and can be more efficiently
    // minified (especially when both are regularly referenced in your plugin).

    // Create the defaults once
    var pluginName = "damonzoom",
        defaults = {
            propertyName: "value"
        };


    // The actual plugin constructor
    function Plugin( element, options ) {
        this.element = element;

        // jQuery has an extend method which merges the contents of two or
        // more objects, storing the result in the first object. The first object
        // is generally empty as we don't want to alter the default options for
        // future instances of the plugin
        this.options = $.extend( {}, defaults, options );
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    Plugin.prototype = {

        init: function() {
            // Place initialization logic here
            // You already have access to the DOM element and
            // the options via the instance, e.g. this.element
            // and this.options
            // you can add more functions like the one below and
            // call them like so: this.yourOtherFunction(this.element, this.options).


            var el = $(this.element);
            var self = this;
            //this needs to be called after the image loads
            // var _setup = function(){
            var _setup = function(el,options){
                    // console.log('calling setup',el.attr('src'))
                
                    var container = $('<div class="damonzoomcontainer"></div>').css({
                            position: 'absolute',
                            top: el.position().top,
                            left: el.position().left,
                            // opacity: 0,
                            width: el.outerWidth(),
                            height: el.outerHeight(),
                            // border: '3px solid red',
                            maxWidth: 'none',
                            overflow:'hidden',
                            display:'none'
                    })

                    var outerWidth
                        ,outerHeight
                        ,xRatio
                        ,yRatio
                        ,offset
                        ,img
                        ,container;

                    img = $("<img/>");
                     // Make in memory copy of image to avoid css issues
                    img.attr("src", el.data('big'))
                    .load(function() {
                           outerWidth = el.outerWidth();
                           outerHeight = el.outerHeight();
                           xRatio = (this.width - outerWidth) / el.outerWidth();
                           yRatio = (this.height - outerHeight) / el.outerHeight();
                           offset = el.offset();
                    
                           console.log(outerWidth)
                           console.log(outerHeight)

                           el.after(container);

                           container.append(img)


                            var move = function (e) {
                                var left = (e.pageX - container.offset().left);
                                var top = (e.pageY - container.offset().top);

                                var d = {
                                    left:(left * - xRatio) + 'px',
                                    top:(top * - yRatio) + 'px'
                                }

                                $(img).stop(true).animate(d,400,'swing')
                            }

                            $(el).mouseenter(
                                function(e){
                                    $(document).mousemove(move);
                                    container.fadeIn(600)
                                })
                            $(container).mouseleave(
                                function(e){
                                    container.fadeOut(600);
                                    $(document).unbind('mousemove',move);
                                }
                            )
                        }).css({position:'absolute'})

                }   
              
            // el.load(function(){
                _setup(el,this.options)
            // }.apply(this));
            // 

        }
    }

    // A really lightweight plugin wrapper around the constructor,
    // preventing against multiple instantiations
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new Plugin( this, options ));
            }
        });
    };

})( jQuery, window, document );