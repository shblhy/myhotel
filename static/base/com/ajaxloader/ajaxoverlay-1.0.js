/*
 * Ajax overlay 1.0
 *
 *	onAjax 不与 timer 共用
 *  1.改写成方法
 *  2.添加error方法，与remove方法区别，没淡出效果
 *  3.当容器的高度高于window，loader的top为window的一半
 *
 *
 * 
 */
;
(function($) {

	var Ajaxloader = function(el, options) {
		var defaults = {
			bgColor: 'black',
			duration: 0,
			opacity: 0.1,
			classOveride: false, //遮罩层class
			fadeOut: 100, //淡出时间
			onAjax: false,
			timer: false,

			loadingInfo: false,
			loadingText: '正在加载中,请稍候...',

			/**3**/
			zIndex:'auto',//'auto'(default body->2147483647 else 99998) 'top' int 
			/**end3**/
			color: '#1c96e2',
			shape: 'rounded',
			diameter: 64,//大小，默认40
			density: 90,//密度，默认40
			range: 1,//反差，默认1.3 
			speed: 3//转速，默认2 
		};

		//初始化颜色
		options.bgColor = options.bgColor ? options.bgColor : 'black';
		if(options.bgColor == 'black'){
			options.bgColor = '#000';
			if(!options.opacity){
				options.opacity = 0.1;
			}
		}else if(options.bgColor == 'white'){
			options.bgColor = '#FFF';
			if(!options.opacity){
				options.opacity = 0.5;
			}
		};

		this.options = $.extend(defaults, options), _this = this;

		if (this.options.onAjax) {
			(function(el, _this, options) {
				$(el).on('ajaxStart.loading', function() {
					_this.init(this, options);
				}).on('ajaxStop.loading', function() {
					_this.remove(this, options);
					$(this).data('ajaxloader', '');
				});
			})(el, _this, this.options)
		} else {
			if ($(el).children('.ajax_wrapper').length) {
				return;
			}
			_this.init(el, this.options);
		}
	}

	Ajaxloader.prototype = {
		constructor: Ajaxloader,
		init: function(el, options) {
			var container = $(el);
			//给容器添加.relative类
			container.addClass('relative');
			/**3**
			//计算容器宽高，包括padding
			var width = container.width() + parseInt(container.css('padding-left')) + parseInt(container.css('padding-right')),
				height = container.height() + parseInt(container.css('padding-top')) + parseInt(container.css('padding-bottom'));
			var loaderWrapper = $('<div></div>').css({
				'width': width,
				'height': height,
				'position': 'absolute',
				'top': 0,
				'left': 0,
				'z-index': 99999
			}).addClass('ajax_wrapper');
			// Create the overlay 
			//给容器添加.relative样式
			var overlay = $('<div><style>.relative{position:relative !important}</style></div>').css({
				'background-color': options.bgColor,
				'opacity': options.opacity,
				'width': width,
				'height': height,
				'position': 'absolute',
				'top': 0,
				'left': 0
			}).addClass('ajax_overlay');
			**/
			var zIndex = options.zIndex === 'auto' ? (container[0] === $('body')[0] ? '2147483646' : '999' ) : (options.zIndex === 'top' ? '2147483647' : options.zIndex);
			//计算容器宽高，包括padding
			var width = container.width() + parseInt(container.css('padding-left')) + parseInt(container.css('padding-right')),
				height = container.height() + parseInt(container.css('padding-top')) + parseInt(container.css('padding-bottom'));
			var loaderWrapper = $('<div></div>').css({
				'width': width,
				'height': height,
				'position': 'absolute',
				'top': 0,
				'left': 0,
				'z-index': zIndex
			}).addClass('ajax_wrapper');
			//给容器添加.relative样式
			var overlay = $('<div><style>.relative{position:relative !important}</style></div>').css({
				'background-color': options.bgColor,
				'opacity': options.opacity,
				'width': width,
				'height': height,
				'position': (container[0] === $('body')[0] ? 'fixed' : 'absolute'),
				'top': 0,
				'left': 0,
				'z-index': zIndex
			}).addClass('ajax_overlay');
			/**end3**/
			// add an overiding class name to set new loader style 
			if (options.classOveride) {
				overlay.addClass(options.classOveride);
			}
			var canvasFrame = document.createDocumentFragment();
			// 设置加速定时器
			(function speed(loader, options, time) {
				if (options.speed < 10 && options.timer) {
					setTimeout(function() {
						loader.setSpeed(options.speed++);
						speed(loader, options, time + 1000);
					}, time);
				}
			})(new CanvasImageLoader(canvasFrame, options), options, 1000);

			/**3**
			var ajax_loader = $('<div></div>').addClass('ajax_loader').css({
				'position': 'absolute',
				'left': '50%',
				'top': '50%',
				'z-index': '2147483647'
			}).append(canvasFrame);
			**/
			var top = (height > $(window).height() ? $(window).height()/2 :'50%'), 			
			position = container[0] === $('body')[0] ? 'fixed' : 'absolute' ;
			var ajax_loader = $('<div></div>').addClass('ajax_loader').css({
				'position': position,
				'left': '50%',
				'top': top,
				'z-index': parseInt(zIndex)+1
			}).append(canvasFrame);
			/**end3**/

			loaderWrapper.append(ajax_loader).appendTo(container);

			//加载文字
			/*
			var loadingText = $('<div></div>').css({
				'width': '180px',
				'left': options.diameter/2 + 7 + 'px',
				'position': 'absolute',
				'text-align': 'left',
				'top': '-8px'
			}).text(options.loadingText);
			*/
			if (options.loadingInfo) {
				var loadingText = $('<div></div>').css({
					'width': '180px',
					'left': '-90px',
					'position': 'absolute',
					'text-align': 'center',
					'top': options.diameter / 2 + 7 + 'px'
				}).text(options.loadingText);

				ajax_loader.append(loadingText);
			}

			overlay.hide().appendTo(loaderWrapper).show();
		},
		remove: function(el, options) {
			var container = $(el);
			var loaderWrapper = container.children(".ajax_wrapper");
			if (loaderWrapper.length) {
				loaderWrapper.fadeOut(options.fadeOut, function() {
					loaderWrapper.remove();
					//给容器添加.relative类
					container.removeClass('relative');
				});
			}
			container.data('ajaxloader', '');
		},
		error: function(el, options) {
			var container = $(el);
			var loaderWrapper = container.children(".ajax_wrapper");
			if (loaderWrapper.length) {
				loaderWrapper.remove();
				//给容器添加.relative类
				container.removeClass('relative');
			}
			container.data('ajaxloader', '');
		}
	}

	$.fn.ajaxLoader = function(options) {
		return this.each(function() {
			if (typeof options != 'string') {
				$(this).data('ajaxloader', new Ajaxloader(this, options));
			} else {
				var ajaxloader = $(this).data('ajaxloader');
				if (ajaxloader) {
					ajaxloader[options](this, ajaxloader.options);
				}
			}
		})
	};
})(jQuery);