/**
 * @author zhixin wen <wenzhixin2010@gmail.com>
 * @version 1.0.5
 *
 * http://wenzhixin.net.cn/p/multiple-select/
 *
 *1b.新增initData
 *2b.新增loadData方法
 *3b.隐藏全选复选框
 *
 * 
 *3b.getSelectData loadJson
 *
 *
 *
 */

(function($) {

	'use strict';

	function MultipleSelect($el, options) {
		/**9b**
		var that = this,
			elWidth = $el.width();

		this.$el = $el.hide();
		this.options = options;

		this.$parent = $('<div class="ms-parent"></div>');
		this.$choice = $('<button type="button" class="ms-choice"><span class="placeholder">' +
			options.placeholder + '</span><div></div></button>');
		this.$drop = $('<div class="ms-drop"></div>');
		this.$el.after(this.$parent);
		this.$parent.append(this.$choice);
		this.$parent.append(this.$drop);

		if (this.$el.prop('disabled')) {
			this.$choice.addClass('disabled');
		}
		this.$choice.css('width', elWidth + 'px')
			.find('span').css('width', (elWidth - 30) + 'px');
		this.$drop.css({
			width: (options.width || elWidth) + 'px'
		});
		$('body').click(function(e) {
			if ($(e.target)[0] === that.$choice[0] ||
					$(e.target).parents('.ms-choice')[0] === that.$choice[0]) {
				return;
			}
			if (($(e.target)[0] === that.$drop[0] ||
					$(e.target).parents('.ms-drop')[0] !== that.$drop[0]) &&
					that.options.isopen) {
				that.close();
			}
		});
		if (this.options.isopen) {
			this.open();
		}
		**/
		var that = this;
		this.elWidth = $el.width();

		this.$el = $el.hide();
		this.options = options;
		$('body').mouseup(function(e) {
			if ($(e.target)[0] !== that.$choice[0] &&
				$(e.target).parents('.ms-choice')[0] !== that.$choice[0] && ($(e.target)[0] !== that.$drop[0] &&
					$(e.target).parents('.ms-drop')[0] !== that.$drop[0]) &&
				that.options.isopen) {
				that.close();
			}
		});
		/**end9b**/
	}

	MultipleSelect.prototype = {
		constructor: MultipleSelect,

		init: function() {
			var that = this,
				html = [];
			/**9b**/
			this.$parent = $('<div class="ms-parent"></div>');
			this.$choice = $('<button type="button" class="ms-choice"><span class="placeholder">' +
				this.options.placeholder + '</span><div></div></button>');
			this.$drop = $('<div class="ms-drop"></div>');
			this.$el.after(this.$parent);
			this.$parent.append(this.$choice);
			this.$parent.append(this.$drop);

			if (this.$el.prop('disabled')) {
				this.$choice.addClass('disabled');
			}
			this.$choice.css('width', this.elWidth + 8 + 'px')
				.find('span').css('width', (this.elWidth - 22) + 'px');
			this.$drop.css({
				width: (this.options.width || this.elWidth) + 'px'
			});
			/**1.**/
			this.multipleWidth = this.$el.width();
			/**end1**/

			if (this.options.isopen) {
				this.open();
			}
			/**end9b**/
			if (this.options.filter) {
				html.push(
					'<div class="ms-search">',
					'<input type="text" autocomplete="off" autocorrect="off" autocapitilize="off" spellcheck="false">',
					'</div>'
				);
			}
			html.push('<ul>');
			if (this.options.selectAll) {
				/**1**
				html.push(
					'<li>',
						'<label>',
							'<input type="checkbox" name="selectAll" /> ',
							'[' + this.options.selectAllText + ']',
						'</label>',
					'</li>'
				);
				**/
				var width = '';
				if (this.options.multipleWidth != 'auto') {
					width = 'width:\'' + this.options.multipleWidth + '\'';
				} else {
					width = 'width:\'' + this.multipleWidth + 'px\'';
				}
				html.push(
					'<li>',
					'<label style="' + width + '">',
					'<input type="checkbox" name="selectAll" value="' + this.options.selectAllValue + '" /> ',
					'【' + this.options.selectAllText + '】',
					'</label>',
					'</li>'
				);
				/**end1**/
			}

			/**1b.新增initData**/
			if (!this.options.cuscustomParams && this.options.initData.length) {
				var initData = this.options.initData,
					optionsHTml = '';
				$.each(initData, function(v, n) {
					if(n.length)
						optionsHTml += '<option value="' + n[1] + '"' + (n[2] ? 'selected="selected"' : '') + '>' + n[0] + '</option>';
					else
						optionsHTml += '<option value="' + n.value + '"' + (n.selected ? 'selected="selected"' : '') + '>' + n.text + '</option>';						
				});
				this.$el.html(optionsHTml);
			}
			/**end1b**/

			$.each(this.$el.children(), function(i, elm) {
				html.push(that.optionToHtml(i, elm));
			});
			html.push('</ul>');
			this.$drop.html(html.join(''));
			this.$drop.find('ul').css('max-height', this.options.maxHeight + 'px');

			/**1.**
			this.$drop.find('.multiple').css('width', this.options.multipleWidth + 'px');
			*/
			if (this.options.multipleWidth != 'auto') {
				this.$drop.find('label').css('width', this.options.multipleWidth);
			} else {
				this.$drop.find('label').css('width', this.multipleWidth + 'px');
			}
			/**end1**/

			this.$searchInput = this.$drop.find('.ms-search input');
			this.$selectAll = this.$drop.find('input[name="selectAll"]');
			this.$selectGroups = this.$drop.find('input[name="selectGroup"]');
			this.$selectItems = this.$drop.find('input[name="selectItem"]:enabled');
			this.$disableItems = this.$drop.find('input[name="selectItem"]:disabled');
			this.events();

			/**1.**/
			if (this.options.selectAll && (this.$drop.find('input[name="selectItem"]:enabled').length == this.$drop.find('input[name="selectItem"]:enabled:checked').length)) {
				this.$selectAll.prop('checked', true);
				this.options.onCheckAll();
				this.$choice.prop('title', this.options.selectAllText);
			}
			/**end1**/

			this.update();

			/**6.设置选中状态**/
			if (this.options.miniSelection && (this.$el.val() == null)) {
				this.checkAll();
				this.$choice.prop('title', this.options.selectAllText).find('span').text(this.options.selectAllText).removeClass('placeholder');
			}
			/**end6**/

		},

		optionToHtml: function(i, elm, group, groupDisabled) {
			var that = this,
				$elm = $(elm),
				html = [],
				multiple = this.options.multiple;
			if ($elm.is('option')) {
				var value = $elm.val(),
					text = $elm.text(),
					selected = $elm.prop('selected'),
					disabled = groupDisabled || $elm.prop('disabled');
				html.push(
					'<li' + (multiple ? ' class="multiple"' : '') + '>',
					'<label' + (disabled ? ' class="disabled"' : '') + '>',
					'<input type="checkbox" name="selectItem" value="' + value + '"' +
					(selected ? ' checked="checked"' : '') +
					(disabled ? ' disabled="disabled"' : '') +
					(group ? ' data-group="' + group + '"' : '') +
					'/> ',
					text,
					'</label>',
					'</li>'
				);
			} else if (!group && $elm.is('optgroup')) {
				var _group = 'group_' + i,
					label = $elm.attr('label'),
					disabled = $elm.prop('disabled');
				html.push(
					'<li class="group">',
					'<label class="optgroup' + (disabled ? ' disabled' : '') + '" data-group="' + _group + '">',
					'<input type="checkbox" name="selectGroup" /> ',
					label,
					'</label>',
					'</li>');
				$.each($elm.children(), function(i, elm) {
					html.push(that.optionToHtml(i, elm, _group, disabled));
				});
			}
			return html.join('');
		},

		events: function() {
			var that = this;
			/**3.**
			this.$choice.off('click').on('click', function() {
				that[that.options.isopen ? 'close' : 'open']();
			});
			**/
			this.$choice.off('click').on('click', function(e) {
				that[that.options.isopen ? 'close' : 'open']();
				e.preventDefault();
			});
			/**end3**/
			this.$parent.off('keydown').on('keydown', function(e) {
				switch (e.which) {
					case 27: // esc key
						that.close();
						that.$choice.focus();
						break;
				}
			});
			this.$searchInput.off('keyup').on('keyup', function() {
				that.filter();
			});
			this.$selectAll.off('click').on('click', function() {
				var checked = $(this).prop('checked'),
					$items = that.$selectItems.filter(':visible');
				if ($items.length === that.$selectItems.length) {
					that[checked ? 'checkAll' : 'uncheckAll']();
				} else { // when the filter option is true
					$items.prop('checked', checked);
					/**3.**
					that.update();
					**end3**/
				}
			});
			this.$selectGroups.off('click').on('click', function() {
				var group = $(this).parent().attr('data-group'),
					$items = that.$selectItems.filter(':visible'),
					$children = $items.filter('[data-group="' + group + '"]'),
					checked = $children.length !== $children.filter(':checked').length;
				$children.prop('checked', checked);
				that.updateSelectAll();
				/**3.**
				that.update();
				**end3**/
				that.options.onOptgroupClick({
					label: $(this).parent().text(),
					checked: checked,
					children: $children.get()
				});
			});
			this.$selectItems.off('click').on('click', function() {
				that.updateSelectAll();
				/**3.**
				that.update();
				**end3**/
				that.updateOptGroupSelect();
				that.options.onClick({
					label: $(this).parent().text(),
					value: $(this).val(),
					checked: $(this).prop('checked')
				});
			});
		},

		open: function() {
			if (this.$choice.hasClass('disabled')) {
				return;
			}
			this.options.isopen = true;
			this.$choice.find('>div').addClass('open');
			this.$drop.show();
			if (this.options.filter) {
				this.$searchInput.val('');
				this.filter();
			}
			this.options.onOpen();
		},

		close: function() {
			/**5.**/
			if (this.options.miniSelection && !this.$selectItems.filter(':checked').length) {
				var $span = this.$choice.find('>span');
				$span.html('<span style="color:red">' + this.options.miniSelectionText + '</span>');
				return false;
			}
			/**end5**/
			this.options.isopen = false;
			this.$choice.find('>div').removeClass('open');
			this.$drop.hide();
			this.options.onClose();

			/**3.**/
			this.update();
			/**end3**/
		},

		update: function() {
			/**5.**
			var selects = this.getSelects('text'),
				$span = this.$choice.find('>span');
			if (selects.length) {
				$span.removeClass('placeholder').html(selects.join(','));
			} else {
				$span.addClass('placeholder').html(this.options.placeholder);
			}
			**/
			var selects = this.getSelects('text'),
				$span = this.$choice.find('>span'),
				oldInput = $span.html(), newSelection;

			if (selects.length) {
				newSelection = selects.join(',');
				if (oldInput !== newSelection) {
					this.$el.triggerHandler('change');
					$span.removeClass('placeholder').html(newSelection);
					this.$choice.prop('title', newSelection);
				}
			} else {
				if (oldInput !== this.options.placeholder) {
					this.$el.triggerHandler('change');
				}
				$span.addClass('placeholder').html(this.options.placeholder);
			}
			/**end5**/
			// set selects to select
			this.$el.val(this.getSelects());

		},

		updateSelectAll: function() {
			var $items = this.$selectItems.filter(':visible');
			this.$selectAll.prop('checked', $items.length &&
				$items.length === $items.filter(':checked').length);
		},

		updateOptGroupSelect: function() {
			var $items = this.$selectItems.filter(':visible');
			$.each(this.$selectGroups, function(i, val) {
				var group = $(val).parent().attr('data-group'),
					$children = $items.filter('[data-group="' + group + '"]');
				$(val).prop('checked', $children.length &&
					$children.length === $children.filter(':checked').length);
			});
		},

		//value or text, default: 'value'
		getSelects: function(type) {
			var values = [];
			this.$drop.find('input[name="selectItem"]:checked').each(function() {
				values.push(type === 'text' ? $(this).parent().text() : $(this).val());
			});
			/**1.**
			if (this.options.selectAll && this.$selectAll && this.$selectAll.filter(':checked').length) {
				values.push(type === 'text' ? this.options.selectAllText : this.options.selectAllValue);
			} else {
				this.$drop.find('input[name="selectItem"]:checked').each(function() {
					values.push(type === 'text' ? $(this).parent().text() : $(this).val());
				});
			}
			**end1**/
			return values;
		},

		setSelects: function(values) {
			/**7.**
			var that = this;
			this.$selectItems.prop('checked', false);
			$.each(values, function(i, value) {
				that.$selectItems.filter('[value="' + value + '"]').prop('checked', true);
			});
			this.$selectAll.prop('checked', this.$selectItems.length ===
				this.$selectItems.filter(':checked').length);
			this.update();
			**/
			if (values == this.options.selectAllValue) {
				this.checkAll();
				this.$choice.find('span').text(this.options.selectAllText).removeClass('placeholder');
			} else {
				var that = this;
				this.$selectItems.prop('checked', false);
				$.each(values, function(i, value) {
					that.$selectItems.filter('[value="' + value + '"]').prop('checked', true);
				});
				this.$selectAll.prop('checked', this.$selectItems.length ===
					this.$selectItems.filter(':checked').length);
				this.update();
			}
			/**end7**/
		},

		enable: function() {
			this.$choice.removeClass('disabled');
		},

		disable: function() {
			this.$choice.addClass('disabled');
		},

		checkAll: function() {
			this.$selectItems.prop('checked', true);
			this.$selectGroups.prop('checked', true);
			this.$selectAll.prop('checked', true);
			/**3.**
					this.update();
					**end3**/
			this.options.onCheckAll();
		},

		uncheckAll: function() {
			this.$selectItems.prop('checked', false);
			this.$selectGroups.prop('checked', false);
			this.$selectAll.prop('checked', false);
			/**3.**
					this.update();
					**end3**/
			this.options.onUncheckAll();
		},

		refresh: function() {
			this.init();
		},
		/**2b**/
		loadData: function(data) {
			this.$parent.remove();
			this.options.initData = data;
			this.init();
		},
		/**end2b**/
		filter: function() {
			var that = this,
				text = $.trim(this.$searchInput.val()).toLowerCase();
			if (text.length === 0) {
				this.$selectItems.parent().show();
				this.$disableItems.parent().show();
				this.$selectGroups.show();
			} else {
				this.$selectItems.each(function() {
					var $parent = $(this).parent();
					$parent[$parent.text().toLowerCase().indexOf(text) < 0 ? 'hide' : 'show']();
				});
				this.$disableItems.parent().hide();
				this.$selectGroups.each(function() {
					var group = $(this).attr('data-group'),
						$items = that.$selectItems.filter(':visible');
					$(this)[$items.filter('[data-group="' + group + '"]').length === 0 ? 'hide' : 'show']();
				});
			}
			this.updateSelectAll();
		}
	};

	$.fn.multipleSelect = function() {
		var option = arguments[0],
			args = arguments,

			value,
			allowedMethods = ['getSelects', 'setSelects', 'enable', 'disable', 'checkAll', 'uncheckAll', 'refresh' /**2b**/ , "loadData" /**end2b**/ ];

		this.each(function() {
			var $this = $(this),
				data = $this.data('multipleSelect'),
				options = $.extend({}, $.fn.multipleSelect.defaults, typeof option === 'object' && option);

			if (!data) {
				data = new MultipleSelect($this, options);
				$this.data('multipleSelect', data);
			}

			if (typeof option === 'string') {
				if ($.inArray(option, allowedMethods) < 0) {
					throw "Unknown method: " + option;
				}
				value = data[option](args[1]);
			} else {
				data.init();
			}
		});

		return value ? value : this;
	};

	$.fn.multipleSelect.defaults = {
		isopen: false,
		placeholder: '请选择...',
		selectAll: true,
		selectAllText: '全选',
		multiple: true,
		multipleWidth: 'auto',
		filter: false,
		width: undefined,
		maxHeight: 250,

		/**1b.新增initData**/
		initData: [],
		customParams: false,
		/**end1b**/
		/**1.**/
		selectAllValue: 'all',
		/**end1**/
		/**5.**/
		miniSelection: 0,
		miniSelectionText: '请至少选择一项',
		/**end5**/

		onOpen: function() {
			return false;
		},
		onClose: function() {
			return false;
		},
		onCheckAll: function() {
			return false;
		},
		onUncheckAll: function() {
			return false;
		},
		onOptgroupClick: function() {
			return false;
		},
		onClick: function() {
			return false;
		}
	};
})(jQuery);