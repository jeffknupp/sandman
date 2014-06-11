/* Smartclick Plugin for iDevices */
// Ref: http://cubiq.org/remove-onclick-delay-on-webkit-for-iphone
// Copyright SmartAdmin

$.fn.noClickDelay = function() {
	var $wrapper = this,
	 	$target = this,
	 	moved = false;
	$wrapper.bind('touchstart mousedown', function(e) {
		e.preventDefault();
		moved = false;
		$target = $(e.target);
		if ($target.nodeType == 3) {
			$target = $($target.parent());
		}
		$target.addClass('pressed');
		$wrapper.bind('touchmove mousemove', function(e) {
			moved = true;
			$target.removeClass('pressed');
		});
		$wrapper.bind('touchend mouseup', function(e) {
			$wrapper.unbind('mousemove touchmove');
			$wrapper.unbind('mouseup touchend');
			if (!moved && $target.length) {
				$target.removeClass('pressed');
				$target.trigger('click');
				$target.focus();
			}
		});
	});
};