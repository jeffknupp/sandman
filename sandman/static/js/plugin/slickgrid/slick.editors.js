/***
 * Contains basic SlickGrid editors.
 * @module Editors
 * @namespace Slick
 */

(function($) {
	// register namespace
	$.extend(true, window, {
		"Slick" : {
			"Editors" : {
				"Text" : TextEditor,
				"Integer" : IntegerEditor,
				"Date" : DateEditor,
				"YesNoSelect" : YesNoSelectEditor,
				"Checkbox" : CheckboxEditor,
				"PercentComplete" : PercentCompleteEditor,
				"LongText" : LongTextEditor
			}
		}
	});

	function TextEditor(args) {
		var $input;
		var defaultValue;
		var scope = this;

		this.init = function() {
			$input = $("<INPUT type=text class='editor-text' />").appendTo(args.container).bind("keydown.nav", function(e) {
				if (e.keyCode === $.ui.keyCode.LEFT || e.keyCode === $.ui.keyCode.RIGHT) {
					e.stopImmediatePropagation();
				}
			}).focus().select();
		};

		this.destroy = function() {
			$input.remove();
		};

		this.focus = function() {
			$input.focus();
		};

		this.getValue = function() {
			return $input.val();
		};

		this.setValue = function(val) {
			$input.val(val);
		};

		this.loadValue = function(item) {
			defaultValue = item[args.column.field] || "";
			$input.val(defaultValue);
			$input[0].defaultValue = defaultValue;
			$input.select();
		};

		this.serializeValue = function() {
			return $input.val();
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (!($input.val() == "" && defaultValue == null)) && ($input.val() != defaultValue);
		};

		this.validate = function() {
			if (args.column.validator) {
				var validationResults = args.column.validator($input.val());
				if (!validationResults.valid) {
					return validationResults;
				}
			}

			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	function IntegerEditor(args) {
		var $input;
		var defaultValue;
		var scope = this;

		this.init = function() {
			$input = $("<INPUT type=text class='editor-text' />");

			$input.bind("keydown.nav", function(e) {
				if (e.keyCode === $.ui.keyCode.LEFT || e.keyCode === $.ui.keyCode.RIGHT) {
					e.stopImmediatePropagation();
				}
			});

			$input.appendTo(args.container);
			$input.focus().select();
		};

		this.destroy = function() {
			$input.remove();
		};

		this.focus = function() {
			$input.focus();
		};

		this.loadValue = function(item) {
			defaultValue = item[args.column.field];
			$input.val(defaultValue);
			$input[0].defaultValue = defaultValue;
			$input.select();
		};

		this.serializeValue = function() {
			return parseInt($input.val(), 10) || 0;
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (!($input.val() == "" && defaultValue == null)) && ($input.val() != defaultValue);
		};

		this.validate = function() {
			if (isNaN($input.val())) {
				return {
					valid : false,
					msg : "Please enter a valid integer"
				};
			}

			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	function DateEditor(args) {
		var $input;
		var defaultValue;
		var scope = this;
		var calendarOpen = false;

		this.init = function() {
			$input = $("<INPUT type=text class='editor-text' />");
			$input.appendTo(args.container);
			$input.datepicker({
				autoclose:true
			}).focus().select();
			
		};

		this.destroy = function() {
			$.datepicker.dpDiv.stop(true, true);
			$input.datepicker("hide");
			$input.datepicker("destroy");
			$input.remove();
		};

		this.show = function() {
			if (calendarOpen) {
				$.datepicker.dpDiv.stop(true, true).show();
			}
		};

		this.hide = function() {
			if (calendarOpen) {
				$.datepicker.dpDiv.stop(true, true).hide();
			}
		};

		this.position = function(position) {
			if (!calendarOpen) {
				return;
			}
			$.datepicker.dpDiv.css("top", position.top + 30).css("left", position.left);
		};

		this.focus = function() {
			$input.focus();
		};

		this.loadValue = function(item) {
			defaultValue = item[args.column.field];
			$input.val(defaultValue);
			$input[0].defaultValue = defaultValue;
			$input.select();
		};

		this.serializeValue = function() {
			return $input.val();
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (!($input.val() == "" && defaultValue == null)) && ($input.val() != defaultValue);
		};

		this.validate = function() {
			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	function YesNoSelectEditor(args) {
		var $select;
		var defaultValue;
		var scope = this;

		this.init = function() {
			$select = $("<SELECT tabIndex='0' class='editor-yesno'><OPTION value='yes'>Yes</OPTION><OPTION value='no'>No</OPTION></SELECT>");
			$select.appendTo(args.container);
			$select.focus();
		};

		this.destroy = function() {
			$select.remove();
		};

		this.focus = function() {
			$select.focus();
		};

		this.loadValue = function(item) {
			$select.val(( defaultValue = item[args.column.field]) ? "yes" : "no");
			$select.select();
		};

		this.serializeValue = function() {
			return ($select.val() == "yes");
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return ($select.val() != defaultValue);
		};

		this.validate = function() {
			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	function CheckboxEditor(args) {
		var $select;
		var defaultValue;
		var scope = this;

		this.init = function() {
			$select = $("<INPUT type=checkbox value='true' class='editor-checkbox' hideFocus>");
			$select.appendTo(args.container);
			$select.focus();
		};

		this.destroy = function() {
			$select.remove();
		};

		this.focus = function() {
			$select.focus();
		};

		this.loadValue = function(item) {
			defaultValue = !!item[args.column.field];
			if (defaultValue) {
				$select.prop('checked', true);
			} else {
				$select.prop('checked', false);
			}
		};

		this.serializeValue = function() {
			return $select.prop('checked');
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (this.serializeValue() !== defaultValue);
		};

		this.validate = function() {
			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	function PercentCompleteEditor(args) {
		var $input, $picker;
		var defaultValue;
		var scope = this;

		this.init = function () {
			$input = $('<input type="text" class="form-control input-sm">');
			$input.appendTo(args.container);
			
			$picker = $('<input type="text" value="0;100" />').appendTo(args.container);
			
			var this_val = args.item.percentComplete;
		
			$input.focus().select();
			$picker.ionRangeSlider({
				type: "single",
				step: 1,
				postfix: " %",
				from: this_val,
				min: 0,
				max:100,
				hasGrid: false,
				onChange: function(obj){
					var thisVal = obj.fromNumber;
					$input.val(thisVal)
				}
			});

		};

		this.destroy = function() {
			$input.remove();
			$picker.remove();
		};

		this.focus = function() {
			$input.focus();
		};

		this.loadValue = function(item) {
			$input.val( defaultValue = item[args.column.field]);
			$input.select();
		};

		this.serializeValue = function() {
			return parseInt($input.val(), 10) || 0;
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (!($input.val() == "" && defaultValue == null)) && ((parseInt($input.val(), 10) || 0) != defaultValue);
		};

		this.validate = function() {
			if (isNaN(parseInt($input.val(), 10))) {
				return {
					valid : false,
					msg : "Please enter a valid positive number"
				};
			}

			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

	/*
	 * An example of a "detached" editor.
	 * The UI is added onto document BODY and .position(), .show() and .hide() are implemented.
	 * KeyDown events are also handled to provide handling for Tab, Shift-Tab, Esc and Ctrl-Enter.
	 */
	function LongTextEditor(args) {
		var $input, $wrapper;
		var defaultValue;
		var scope = this;

		this.init = function () {
			var $container = $("body");
	  
			$wrapper = $('<div class="slick-long-text"/>')
				.appendTo($container);
	  
			$input = $('<textarea hidefocus rows="6" class="form-control">')
				.appendTo($wrapper);
	  
			$input.wrap('<div class="form-group">');
			
			$('<button class="btn btn-default btn-sm">Save</button><button class="btn btn-sm btn-link">Cancel</button>')
				.appendTo($wrapper);
	  
			$wrapper.find("button:first").bind("click", this.save);
			$wrapper.find("button:last").bind("click", this.cancel);
			$input.bind("keydown", this.handleKeyDown);
	  
			scope.position(args.position);
			$input.focus().select();
		};

		this.handleKeyDown = function(e) {
			if (e.which == $.ui.keyCode.ENTER && e.ctrlKey) {
				scope.save();
			} else if (e.which == $.ui.keyCode.ESCAPE) {
				e.preventDefault();
				scope.cancel();
			} else if (e.which == $.ui.keyCode.TAB && e.shiftKey) {
				e.preventDefault();
				args.grid.navigatePrev();
			} else if (e.which == $.ui.keyCode.TAB) {
				e.preventDefault();
				args.grid.navigateNext();
			}
		};

		this.save = function() {
			args.commitChanges();
		};

		this.cancel = function() {
			$input.val(defaultValue);
			args.cancelChanges();
		};

		this.hide = function() {
			$wrapper.hide();
		};

		this.show = function() {
			$wrapper.show();
		};

		this.position = function(position) {
			$wrapper.css("top", position.top - 5).css("left", position.left - 5)
		};

		this.destroy = function() {
			$wrapper.remove();
		};

		this.focus = function() {
			$input.focus();
		};

		this.loadValue = function(item) {
			$input.val( defaultValue = item[args.column.field]);
			$input.select();
		};

		this.serializeValue = function() {
			return $input.val();
		};

		this.applyValue = function(item, state) {
			item[args.column.field] = state;
		};

		this.isValueChanged = function() {
			return (!($input.val() == "" && defaultValue == null)) && ($input.val() != defaultValue);
		};

		this.validate = function() {
			return {
				valid : true,
				msg : null
			};
		};

		this.init();
	}

})(jQuery);
