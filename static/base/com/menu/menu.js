$.fn.menu = function(b) {
	var c = $.extend({
		effect : "fade"
	}, b);
	$this = $(this);
	if(c.effect == "fade") {
		$("li", $this).hover(function() {
			$("> ul, > div", this).hide().fadeIn(200)
		}, function() {
			$("> ul, > div", this).fadeOut(200)
		})
	} else {
		if(c.effect == "slide") {
			$("li", $this).hover(function() {
				$("> ul, > div", this).stop().hide().css({
					display : "block",
					opacity : 0,
					marginTop : 0
				}).animate({
					opacity : 1,
					marginTop : 0
				}, 250)
			}, function() {
				$("> ul, > div", this).stop().animate({
					opacity : 0,
					marginTop : 0
				}, 250, function() {
					$(this).hide()
				})
			})
		}
	}
	$("> li > a", $this).hover(function() {
		$(".bubble-top", this).stop().animate({
			marginTop : -3
		}, 200)
	}, function() {
		$(".bubble-top", this).stop().animate({
			marginTop : 0
		}, 200)
	});
	return this
}
