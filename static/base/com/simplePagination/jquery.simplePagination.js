/**
* simplePagination.js v1.6
* A simple jQuery pagination plugin.
* http://flaviusmatis.github.com/simplePagination.js/
*
* Copyright 2012, Flavius Matis
* Released under the MIT license.
* http://flaviusmatis.github.com/license.html
*
*与服务端交互协议：请求参数： 每页显示数量iDisplayLength 从第几条开始iDisplayStart 返回参数：总记录数量items 本地缓存参数：iDisplayStart
* 
*1.新增翻页信息
*2.新增iDisplayStart从第几条记录显示
*3.更名 itemsOnPage -> iDisplayLength
*4.扩展onPageClick传入参数iDisplayStart iDisplayLength
*5.如果updateItems方法传入items小于上次总记录数，则设置到最后页
*
* 
*/

(function($){

	var methods = {
		init: function(options) {
			var o = $.extend({
				items: 1,
				iDisplayLength: 1,
				pages: 0,
				displayedPages: 5,
				edges: 1,
				currentPage: 1,
				/***2.iDisplayStart***/
				iDisplayStart: 0,
				/***end2***/

				hrefTextPrefix: '#page-',
				hrefTextSuffix: '',
				prevText: '上一页',
				nextText: '下一页',
				ellipseText: '&hellip;',
				cssStyle: 'light-theme',
				selectOnClick: true,
				/**pInfo**/
				pInfo: "第_START_-_END_记录 共_TOTAL_条",//_START_当前页起始/_END_当前页结束/_TOTAL_总记录数/_PAGE_当前页/_PAGES_总页面数
				/**end**/
				/***4.扩展onPageClick传入参数**
				onPageClick: function(pageNumber, event) {
					// Callback triggered when a page is clicked
					// Page number is given as an optional parameter
				},
				*/
				onPageClick: function(iDisplayStart, iDisplayLength, pageNumber, event, self) {
				},
				/***end4***/
				onInit: function() {
					// Callback triggered immediately after initialization
				}
			}, options || {});

			var self = this;

			o.pages = o.pages ? o.pages : Math.ceil(o.items / o.iDisplayLength) ? Math.ceil(o.items / o.iDisplayLength) : 1;
			/***2.iDisplayStart**
			o.currentPage = o.currentPage - 1;
			*/
			if(o.iDisplayStart){
			 	o.currentPage = parseInt(o.iDisplayStart / o.iDisplayLength);
			}else{
				o.currentPage = o.currentPage - 1;
			}
			/***end2***/
			o.halfDisplayed = o.displayedPages / 2;

			this.each(function() {
				self.addClass(o.cssStyle + ' simple-pagination').data('pagination', o);
				methods._draw.call(self);
			});

			o.onInit();

			return this;
		},

		selectPage: function(page) {
			methods._selectPage.call(this, page - 1);
			return this;
		},

		prevPage: function() {
			var o = this.data('pagination');
			if (o.currentPage > 0) {
				methods._selectPage.call(this, o.currentPage - 1);
			}
			return this;
		},

		nextPage: function() {
			var o = this.data('pagination');
			if (o.currentPage < o.pages - 1) {
				methods._selectPage.call(this, o.currentPage + 1);
			}
			return this;
		},

		getPagesCount: function() {
			return this.data('pagination').pages;
		},

		getCurrentPage: function () {
			return this.data('pagination').currentPage + 1;
		},

		destroy: function(){
			this.empty();
			return this;
		},

		drawPage: function (page) {
			var o = this.data('pagination');
			o.currentPage = page - 1;
			this.data('pagination', o);
			methods._draw.call(this);
			return this;
		},

		redraw: function(){
			methods._draw.call(this);
			return this;
		},

		disable: function(){
			var o = this.data('pagination');
			o.disabled = true;
			this.data('pagination', o);
			methods._draw.call(this);
			return this;
		},

		enable: function(){
			var o = this.data('pagination');
			o.disabled = false;
			this.data('pagination', o);
			methods._draw.call(this);
			return this;
		},

		updateItems: function (newItems) {
			var o = this.data('pagination');
			/***5.如果updateItems方法传入items小于上次总记录数，则设置到最后页**
			o.items = newItems;
			o.pages = Math.ceil(o.items / o.iDisplayLength) ? Math.ceil(o.items / o.iDisplayLength) : 1;
			*/
			if(o.items > newItems){
				o.items = newItems;
				o.pages = Math.ceil(o.items / o.iDisplayLength) ? Math.ceil(o.items / o.iDisplayLength) : 1;
				var pageIndex = o.currentPage >= o.pages ? (o.pages - 1) : 0;
				methods._selectPage.call(this, pageIndex);
			}else{
				o.items = newItems;
				o.pages = Math.ceil(o.items / o.iDisplayLength) ? Math.ceil(o.items / o.iDisplayLength) : 1;
			}
			/***end5***/
		
			this.data('pagination', o);
			methods._draw.call(this);
		},

		updateItemsOnPage: function (iDisplayLength) {
			var o = this.data('pagination');
			o.iDisplayLength = iDisplayLength;
			this.data('pagination', o);
			methods._selectPage.call(this, 0);
			return this;
		},

		_draw: function() {
			var	o = this.data('pagination'),
				interval = methods._getInterval(o),
				i;

			methods.destroy.call(this);

			/***1.新增翻页信息**
			var $panel = this.prop("tagName") === "UL" ? this : $('<ul></ul>').appendTo(this);
			*/
			var infoFrom = (o.iDisplayLength*(o.currentPage)+1),
			infoTo = o.iDisplayLength*(o.currentPage+1),
			/**pInfo**
			pageInfo = $('<span/>').prop('class','pull-right').css('padding','4px 5px 0 0').text('第'+ (o.items == 0 ? '0' : infoFrom) +'-'+ (infoTo > o.items ? o.items : infoTo)+'记录 共'+o.items+'条');
			**/
			pageInfo = $('<span/>').prop('class','pull-right').css('padding','4px 5px 0 0').text(o.pInfo.replace('_START_',(o.items == 0 ? '0' : infoFrom)).replace('_END_',(infoTo > o.items ? o.items : infoTo)).replace('_TOTAL_',o.items).replace('_PAGE_',o.currentPage+1).replace('_PAGES_',Math.ceil(o.items/o.iDisplayLength)));			
			/**end**/

			if(this.prop("tagName") === "UL"){
				var $panel =  this;
			}else{
				var $panel = $('<ul></ul>').prop('class','pull-right').appendTo(this);
				pageInfo.appendTo(this)
			};
			/***end1***/

			// Generate Prev link
			if (o.prevText) {
				methods._appendItem.call(this, o.currentPage - 1, {text: o.prevText, classes: 'prev'});
			}

			// Generate start edges
			if (interval.start > 0 && o.edges > 0) {
				var end = Math.min(o.edges, interval.start);
				for (i = 0; i < end; i++) {
					methods._appendItem.call(this, i);
				}
				if (o.edges < interval.start && (interval.start - o.edges != 1)) {
					$panel.append('<li class="disabled"><span class="ellipse">' + o.ellipseText + '</span></li>');
				} else if (interval.start - o.edges == 1) {
					methods._appendItem.call(this, o.edges);
				}
			}

			// Generate interval links
			for (i = interval.start; i < interval.end; i++) {
				methods._appendItem.call(this, i);
			}

			// Generate end edges
			if (interval.end < o.pages && o.edges > 0) {
				if (o.pages - o.edges > interval.end && (o.pages - o.edges - interval.end != 1)) {
					$panel.append('<li class="disabled"><span class="ellipse">' + o.ellipseText + '</span></li>');
				} else if (o.pages - o.edges - interval.end == 1) {
					methods._appendItem.call(this, interval.end++);
				}
				var begin = Math.max(o.pages - o.edges, interval.end);
				for (i = begin; i < o.pages; i++) {
					methods._appendItem.call(this, i);
				}
			}

			// Generate Next link
			if (o.nextText) {
				methods._appendItem.call(this, o.currentPage + 1, {text: o.nextText, classes: 'next'});
			}
		},

		_getInterval: function(o) {
			return {
				start: Math.ceil(o.currentPage > o.halfDisplayed ? Math.max(Math.min(o.currentPage - o.halfDisplayed, (o.pages - o.displayedPages)), 0) : 0),
				end: Math.ceil(o.currentPage > o.halfDisplayed ? Math.min(o.currentPage + o.halfDisplayed, o.pages) : Math.min(o.displayedPages, o.pages))
			};
		},

		_appendItem: function(pageIndex, opts) {
			var self = this, options, $link, o = self.data('pagination'), $linkWrapper = $('<li></li>'), $ul = self.find('ul');

			pageIndex = pageIndex < 0 ? 0 : (pageIndex < o.pages ? pageIndex : o.pages - 1);

			options = $.extend({
				text: pageIndex + 1,
				classes: ''
			}, opts || {});

			if (pageIndex == o.currentPage || o.disabled) {
				if (o.disabled) {
					$linkWrapper.addClass('disabled');
				} else {
					$linkWrapper.addClass('active');
				}
				$link = $('<span class="current">' + (options.text) + '</span>');
			} else {
				$link = $('<a href="' + o.hrefTextPrefix + (pageIndex + 1) + o.hrefTextSuffix + '" class="page-link">' + (options.text) + '</a>');
				$link.click(function(event){
					/***4.扩展onPageClick传入参数**
					return methods._selectPage.call(self, pageIndex, event);
					*/
					methods._selectPage.call(self, pageIndex);
					var pageNumber = pageIndex + 1, iDisplayStart = pageIndex*o.iDisplayLength;
					return o.onPageClick(iDisplayStart, o.iDisplayLength, pageIndex + 1, event, self);
					/***end4***/
				});
			}

			if (options.classes) {
				$link.addClass(options.classes);
			}

			$linkWrapper.append($link);

			if ($ul.length) {
				$ul.append($linkWrapper);
			} else {
				self.append($linkWrapper);
			}
		},

		_selectPage: function(pageIndex, event) {
			var o = this.data('pagination');
			o.currentPage = pageIndex;
			if (o.selectOnClick) {
				methods._draw.call(this);
			}
			/***4.扩展onPageClick传入参数**
			return o.onPageClick(pageIndex + 1, event);
			**end4***/
		}

	};

	$.fn.pagination = function(method) {

		// Method calling logic
		if (methods[method] && method.charAt(0) != '_') {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.pagination');
		}

	};

})(jQuery);
