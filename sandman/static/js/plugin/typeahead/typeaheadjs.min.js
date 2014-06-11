/**
Typeahead.js input, based on [Twitter Typeahead](http://twitter.github.io/typeahead.js).   
It is mainly replacement of typeahead in Bootstrap 3.


@class typeaheadjs
@extends text
@since 1.5.0
@final
@example
<a href="#" id="country" data-type="typeaheadjs" data-pk="1" data-url="/post" data-title="Input country"></a>
<script>
$(function(){
    $('#country').editable({
        value: 'ru',
        typeahead: {
            name: 'country',
            local: [
                {value: 'ru', tokens: ['Russia']}, 
                {value: 'gb', tokens: ['Great Britain']}, 
                {value: 'us', tokens: ['United States']}
            ],
            template: function(item) {
                return item.tokens[0] + ' (' + item.value + ')'; 
            } 
        }
    });
});
</script>
**/(function(e){"use strict";var t=function(e){this.init("typeaheadjs",e,t.defaults)};e.fn.editableutils.inherit(t,e.fn.editabletypes.text);e.extend(t.prototype,{render:function(){this.renderClear();this.setClass();this.setAttr("placeholder");this.$input.typeahead(this.options.typeahead);if(e.fn.editableform.engine==="bs3"){this.$input.hasClass("input-sm")&&this.$input.siblings("input.tt-hint").addClass("input-sm");this.$input.hasClass("input-lg")&&this.$input.siblings("input.tt-hint").addClass("input-lg")}}});t.defaults=e.extend({},e.fn.editabletypes.list.defaults,{tpl:'<input type="text">',typeahead:null,clear:!0});e.fn.editabletypes.typeaheadjs=t})(window.jQuery);