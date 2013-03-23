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
    var pluginName = "damonscroll",
        defaults = {
            orientation: "horizontal",
            target_element: null,
            threshold_percent: 50,
            nextkey : $('.next'),
            prevkey : $('.prev'),
            keynav : true,
            scrollstep:3
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
            this.is_animating = false;
            this.anim_duration = 900;
            this._next_page = this.options.first_page || 2;
            this.num_per_page = this.options.num_per_page || 6;
            this._add_function= this.options.add_function || function(items){
                this._t.append(items);
            }
            this.items_to_add = [];

            if (!this.options.target_element){
                throw('you must specify a "target_element" selector which should be a container element that scrolls inside a bigger scrolling element')
            }else{
                this._t = $(this.options.target_element);
            }
            
            var self = this;
            this.handler = this[this.options.orientation]();
            
            $(this.element).scroll(function(){
                self.onScroll()
            })

            // $(this.element).bind('mousewheel', function(event) {
            //     console.log(event)
            //    var delta = event.originalEvent.wheelDeltaY;
            //     if(delta>0){
            //         self.go_to_nextpage()}
            //     else{
            //         self.go_to_prevpage();
            //     }

            //     return false;
            // });

            // $(this.element).bind("mousewheel",function(ev, delta) {
            //     var scrollTop = $(this).scrollTop();
            //     // $(this).scrollTop(scrollTop-Math.round(delta));
            // });

            if(this.options.keynav) {
                $(document).bind("keydown.damonscroll", function(e) {              
                    if (e.keyCode === 37) {                     
                        self.go_to_prevpage();
                    }
                    else if (e.keyCode === 39) {                        
                        self.go_to_nextpage();
                    }
                
                });
            }

            $('.btn.next').click(function(e){
                 self.go_to_nextpage();
            })
            $('.btn.prev').click(function(e){
                 self.go_to_prevpage();
            })

        },
        go_to_nextpage: function(number){
            this.handler.next_page();
        },
        go_to_prevpage: function(number){
            // console.log('prev')
            this.handler.prev_page();
        },
        onScroll: function() {
            if (this.handler.get_percentage(this.element).p > this.options.threshold_percent){
                this.procure_elements()
            }

        },
        horizontal:function(el){
            var self = this
            var $t = this._t;
            var $e = $(this.element)
            return {
                get_percentage: function(el){
                    var $element = $(el),
                    ew = $element.width(),
                    tw = $t.width(),
                    total = tw-ew;
                    return {'p':100*$element.scrollLeft()/total,'dir':'horizontal'}
                }
                ,animate: function(number){
                    if (!self.is_animating){
                        self.is_animating = true;
                        $e.stop(true).animate({
                            scrollLeft: $e.scrollLeft()+number
                         }, self.anim_duration,function(){self.is_animating = false;self.post_anim_callback()});
                    }   
                },
                next_page: function(){
                    self.handler.animate($e.width()*.66)
                }
                ,prev_page: function(){
                    self.handler.animate(-$e.width()*.66)
                }
            }
        },
        vertical:function(el){
            var self = this
            var $t = this._t;
            var $e = $(this.element)
            return {
                get_percentage: function(el){
                    var $element = $(el),
                    ew = $element.height(),
                    tw = $t.height(),
                    total = tw-ew;
                    return {'p':100*$element.scrollTop()/total,'dir':'vertical'}
                }
                ,animate: function(number){
                    if (!self.is_animating){
                        self.is_animating = true;
                        $e.stop(true).animate({
                            scrollTop: $e.scrollTop()+number
                         }, self.anim_duration,function(){self.is_animating = false;self.post_anim_callback()});
                    }
                }
                ,next_page: function(){
                    self.handler.animate($e.height()*.66);
                }
                ,prev_page: function(){
                    self.handler.animate(-$e.height()*.66);
                }
            }
        },
        procure_elements: function(){
            if (this._no_more_items){
                return false
            }
            if (!this._loading){
                this._loading = true;
                var self = this;
                $.ajax({
                        url: '?page=' + this._next_page + '&item_per_page=' + this.num_per_page,
                        success: function(data) {
                            var items = $(data).find('.item')

                            if (! items.length){
                                self._no_more_items = true;
                            }

                            self.items_to_add= items;
                            if (!self.is_animating){
                                self.post_anim_callback();
                            }
                            self._next_page = $(data).data('nextpage')
                            // console.log($(data).data('nextpage'))
                            self._loading = false;
                        }
                        ,dataType:'html'
                    });
            }
        },
        get_url:function(){
            return this.options.url || window.location
        },
        post_anim_callback:function(){
            if (this.items_to_add.length){
                this._add_function(this.items_to_add)
            }
        }

    };

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