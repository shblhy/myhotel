/**
 * @author zhixin wen <wenzhixin2010@gmail.com>
 * @version 1.1.0
 *
 *1.扩展url/翻页
 *
 *
 *
 *
 *
 *
 * http://wenzhixin.net.cn/p/multiple-select/
 */

(function($) {

    'use strict';

    function MultipleSelect($el, options) {
        var that = this,
            name = $el.attr('name') || options.name || '',
            elWidth = $el.outerWidth();

        this.$el = $el.hide();
        this.options = options;

        this.$parent = $('<div class="ms-parent"></div>');
        /**1**
        this.$choice = $('<button type="button" class="ms-choice"><span class="placeholder">' +
            options.placeholder + '</span><div></div></button>');
        **/
        this.$choice = $('<a class="ms-choice"><span class="placeholder">' +
            options.placeholder + '</span><abbr></abbr><div></div></a>');
        this.$clear = this.$choice.find('abbr');
        /**end**/
        this.$drop = $('<div class="ms-drop ' + options.position + '"></div>');
        this.$el.after(this.$parent);
        this.$parent.append(this.$choice);
        this.$parent.append(this.$drop);

        if (this.$el.prop('disabled')) {
            this.$choice.addClass('disabled');
        }
        this.$parent.css('width', options.width || elWidth);

        if (!this.options.keepOpen) {
            /**
            $('body').click(function(e) {
                if ($(e.target)[0] === that.$choice[0] ||
                    $(e.target).parents('.ms-choice')[0] === that.$choice[0]) {
                    return;
                }
                if (($(e.target)[0] === that.$drop[0] ||
                    $(e.target).parents('.ms-drop')[0] !== that.$drop[0]) &&
                    that.options.isOpen) {
                    that.close();
                }
            });
            **/
            $(window).on('mouseup.multiselect', function(e) {
                if ($(e.target)[0] !== that.$choice[0] &&
                    $(e.target).parents('.ms-choice')[0] !== that.$choice[0] && ($(e.target)[0] !== that.$drop[0] &&
                        $(e.target).parents('.ms-drop')[0] !== that.$drop[0]) &&
                    that.options.isOpen) {
                    that.close();
                }
            });
            /**/
        }

        this.selectAllName = 'name="selectAll' + name + '"';
        this.selectGroupName = 'name="selectGroup' + name + '"';
        this.selectItemName = 'name="selectItem' + name + '"';

        /**新增initData**/
        if (this.options.initData && this.options.initData.length) {
            this.$el.html(this.dataToOptions(this.options.initData));
        }
        /**end**/
        /**1.tagsinput**/
        if (this.options.url) {
            this.iDisplayStart = 0;
            this.iDisplayLength = 10;
        }
    }

    MultipleSelect.prototype = {
        constructor: MultipleSelect,

        /**新增initData**/
        dataToOptions: function(data, selected) {
            var optionsHTml = '';
            $.each(data, function(v, n) {
                if (n.length)
                    optionsHTml += '<option value="' + n[1] + '"' + (n[2] ? 'selected="selected"' : '') + '>' + n[0] + '</option>';
                else
                    optionsHTml += '<option value="' + ((typeof n.value != 'undefined' && n.value != null )? n.value : n.id) + '"' + ((n.selected || selected) ? 'selected="selected"' : '') + '>' + (n.text || n.name) + '</option>';
            });
            return optionsHTml;
        },
        /**end**/

        init: function() {
            var that = this,
                html = [];
            /**1.tagsinput**/
            if (this.options.url) {
                html.push(
                    '<input class="tagsinput" type="text" disabled value="" />',
                    '<div class="row-fluid">'
                );
                if (this.options.outerBtn) {
                    html.push(
                        '<a href="javascript:void(0)" class="pull-left btn btn-small small-margin-left outerBtn"><i class="icon-filter"></i></a>'
                    );
                }
                html.push(
                    '<a href="javascript:void(0)" class="pull-right btn btn-small small-margin-right uncheckAll">'+this.options.clearAllText+'</a><a href="javascript:void(0)" class="pull-right btn btn-small small-margin-right checkAll">'+this.options.selectAllText+'</a></div>'
                );
            }
            /**end**/
            if (this.options.filter) {
                html.push(
                    '<div class="ms-search">',
                    '<input type="text" autocomplete="off" autocorrect="off" autocapitilize="off" spellcheck="false">',
                    '</div>'
                );
            }
            /**1**
            html.push('<ul>');
            **/
            html.push('<ul class="ul">');
            /**end**/
            if (this.options.selectAll && !this.options.single) {
                /**
                html.push(
                    '<li>',
                        '<label>',
                            '<input type="checkbox" ' + this.selectAllName + ' /> ',
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
                    '<input type="checkbox" ' + this.selectAllName + ' value="' + this.options.selectAllValue + '" /> ',
                    '【' + this.options.selectAllText + '】',
                    '</label>',
                    '</li>'
                );
                /**end**/
            }
            $.each(this.$el.children(), function(i, elm) {
                html.push(that.optionToHtml(i, elm));
            });
            /**
            html.push('<li class="ms-no-results">No matches found</li>');
            **/
            html.push('<li class="ms-no-results">' + this.options.noMatchesText + '</li>');
            /**/
            html.push('</ul>');
            /**1.tagsinput**/
            if (this.options.url) {
                html.push(
                    '<div class="pagination"></div>'
                );
            }
            /**end**/
            this.$drop.html(html.join(''));            
            /**1.tagsinput**
            this.$drop.find('ul').css('max-height', this.options.maxHeight + 'px');
            **/
            if (this.options.url) {
                this.$drop.find('ul').css({'height':this.options.maxHeight + 'px','overflow-y':'auto'});
            }else{
                this.$drop.find('ul').css('max-height', this.options.maxHeight + 'px');              
            }
            /**end**/
            /**
            this.$drop.find('.multiple').css('width', this.options.multipleWidth + 'px');
            **/
            if (this.options.multipleWidth != 'auto') {
                this.$drop.find('label').css('width', this.options.multipleWidth);
            } else {
                this.$drop.find('label').css('width', this.multipleWidth + 'px');
            }
            /**/

            this.$searchInput = this.$drop.find('.ms-search input');
            this.$selectAll = this.$drop.find('input[' + this.selectAllName + ']');
            this.$selectGroups = this.$drop.find('input[' + this.selectGroupName + ']');
            this.$selectItems = this.$drop.find('input[' + this.selectItemName + ']:enabled');
            this.$disableItems = this.$drop.find('input[' + this.selectItemName + ']:disabled');
            this.$noResults = this.$drop.find('.ms-no-results');
            /**1.tagsinput**/
            if (this.options.url) {
                this.$lis = this.$selectItems.closest('li');
                this.$tagsinput = this.$drop.find('.tagsinput');

                this.$pagination = this.$drop.find('.pagination');
                this.$uncheckAll = this.$drop.find('.uncheckAll');
                if(!this.options.clearAll)
                    this.$uncheckAll.hide();

                this.$checkAll = this.$drop.find('.checkAll');
                if(!this.options.selectAll)
                    this.$checkAll.hide();

                this.$pager = this.$drop.find('.pager');
                this.$selectAll.closest('li').hide();
                if (this.options.outerBtn)
                    this.$outerBtn = this.$drop.find('.outerBtn');
            }
            /**end**/
            this.events();
            /**单选**/
            if (this.options.url && this.options.single) {
                this.$tagsinputContainer.hide();
                this.$checkAll.hide();
                this.$uncheckAll.hide();
            }
            /**end**/
            /**搜索框阀值 && 1**/
            if (this.options.url || this.options.minimumResultsForSearch && this.options.minimumResultsForSearch < this.$selectItems.length + this.$disableItems.length) {
                this.$searchInput.closest('div').show();
            } else {
                this.$searchInput.closest('div').hide();
            }
            if (this.options.initSelection && this.options.initSelection.length) {
                var initSelection = this.options.initSelection,
                    $options;
                for (var i = 0, l = initSelection.length; i < l; i++) {
                    //添加监测点
                    that.$tagsinput.tagsinput('add', {
                        id: initSelection[i].value,
                        text: initSelection[i].name || initSelection[i].text
                    });                  
                    //var $options = $('<option value="'+initSelection[i].value+'" selected="selected">'+(initSelection[i].name || initSelection[i].text)+'</option>');
                    //that.$el.append($options);
                }
            }
            /**end**/
            this.update();

            if (this.options.isOpen) {
                this.open();
            }
        },

        optionToHtml: function(i, elm, group, groupDisabled) {
            var that = this,
                $elm = $(elm),
                html = [],
                multiple = this.options.multiple,
                disabled,
                /**单选**
                type = this.options.single ? 'radio' : 'checkbox';
                **/
                type = this.options.single ? 'radio' : 'checkbox';
            /**end**/

            if ($elm.is('option')) {
                var value = $elm.val(),
                    text = $elm.text(),
                    selected = $elm.prop('selected'),
                    style = this.options.styler(value) ? ' style="' + this.options.styler(value) + '"' : '';

                disabled = groupDisabled || $elm.prop('disabled');
                html.push(
                    '<li' + (multiple ? ' class="multiple"' : '') + style + '>',
                    '<label' + (disabled ? ' class="disabled"' : '') + '>',
                    '<input type="' + type + '" ' + this.selectItemName + /**1.tagsinput**/ ' title="' + text + '" ' + /**end**/ ' value="' + value + '"' +
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
                    label = $elm.attr('label');

                disabled = $elm.prop('disabled');
                html.push(
                    '<li class="group">',
                    '<label class="optgroup' + (disabled ? ' disabled' : '') + '" data-group="' + _group + '">',
                    '<input type="checkbox" ' + this.selectGroupName +
                    (disabled ? ' disabled="disabled"' : '') + ' /> ',
                    label,
                    '</label>',
                    '</li>');
                $.each($elm.children(), function(i, elm) {
                    html.push(that.optionToHtml(i, elm, _group, disabled));
                });
            }
            return html.join('');
        },
        /**1**/
        updateLis: function(data) {
            this.$lis.remove();

            if (data.length) {
                for (var index in data) {
                    this.$noResults.before($('<li><label ><input type="' + (this.options.single ? 'radio' : 'checkbox') + '" ' + this.selectItemName + ' title="' + (data[index].name || data[index].text) + '" ' + ' value="' + (data[index].value || data[index].id) + '"' + '/> ' + (data[index].name || data[index].text) + '</label></li>'));
                }
                this.$selectItems = this.$drop.find('input[' + this.selectItemName + ']:enabled');
                this.$lis = this.$selectItems.closest('li');
                this.$noResults.hide();
            } else {
                this.$selectItems = this.$drop.find('input[' + this.selectItemName + ']:enabled');
                this.$lis = $('<li />');
                this.$noResults.show();
            }
        },
        updateChecked: function() {
            var val = this.$tagsinput.tagsinput('items');
            this.$selectItems.each(function(){
                for(var i=0,l=val.length; i<l; i++){
                    if(this.value == val[i].id)
                        $(this).prop('checked', true);
                }
            });
            this.updateSelectAll();
        },
        /**end**/
        events: function() {
            var that = this;
            this.$choice.off('click').on('click', function(e) {
                e.preventDefault();
                that[that.options.isOpen ? 'close' : 'open']();
            })
                .off('focus').on('focus', this.options.onFocus)
                .off('blur').on('blur', this.options.onBlur);

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
                /**1**/
                if (that.options.url) {
                    that.refresh();
                }
                /**end**/
            });
            this.$selectAll.off('click').on('click', function() {
                var checked = $(this).prop('checked'),
                    $items = that.$selectItems.filter(':visible');
                if ($items.length === that.$selectItems.length) {
                    that[checked ? 'checkAll' : 'uncheckAll']();
                } else { // when the filter option is true
                    that.$selectGroups.prop('checked', checked);
                    $items.prop('checked', checked);
                    that.options[checked ? 'onCheckAll' : 'onUncheckAll']();
                    /**
                    that.update();
                    **/
                }
            });
            this.$selectGroups.off('click').on('click', function() {
                var group = $(this).parent().attr('data-group'),
                    $items = that.$selectItems.filter(':visible'),
                    $children = $items.filter('[data-group="' + group + '"]'),
                    checked = $children.length !== $children.filter(':checked').length;
                $children.prop('checked', checked);
                that.updateSelectAll();
                /**
                that.update();
                **/
                that.options.onOptgroupClick({
                    label: $(this).parent().text(),
                    checked: checked,
                    children: $children.get()
                });
            });
            /**1**
            this.$selectItems.off('click').on('click', function() {
            **/
            this.$drop.find('ul').off('click').on('click', 'input[' + this.selectItemName + ']:enabled', function() {
                /**end**/
                that.updateSelectAll();
                /**
                that.update();
                **/
                that.updateOptGroupSelect();
                that.options.onClick({
                    label: $(this).parent().text(),
                    value: $(this).val(),
                    checked: $(this).prop('checked')
                });

                if (that.options.single && that.options.isOpen && !that.options.keepOpen) {
                    that.close();
                }
            });
            /**1.tagsinput**/
            this.$clear.off('click').on('click', function() {
                if (that.$tagsinput) that.$tagsinput.tagsinput('removeAll');
                that.uncheckAll();
                that.update();
                $(this).hide();
                that.$el.triggerHandler('change');
                return false;
            })
            if (this.options.url) {
                this.$drop.find('ul').off('change').on('change', 'input[' + this.selectItemName + ']:enabled', function(e) {
                    if (that.options.single) that.$tagsinput.tagsinput('removeAll');
                    if (e.target.checked) {
                        //添加监测点
                        that.$tagsinput.tagsinput('add', {
                            id: e.target.value,
                            text: e.target.title
                        });
                        //animateFromTo
                        //$(this).animate_from_to(that.addItem);
                    } else {
                        that.$tagsinput.tagsinput('remove', {
                            id: e.target.value,
                            text: e.target.title
                        });
                    }
                    that.updateSelectAll();
                    if (that.options.single) that.close();
                });
                //this.addItem; //animateFromTo钩子
                this.$tagsinputContainer = this.$tagsinput
                    .on('itemRemoved', function(item) {
                        if (item && item.item) {
                            that.$selectItems.filter('input[value=' + item.item.id + ']').removeAttr('checked');
                            //that.$el.find('option[value='+item.item.id+']').remove();
                        };
                    })
                    .on('itemAdded', function(item) {
                        //that.addItem = item.element.get(0); //animateFromTo      
                        //var $options = $('<option value="'+item.item.id+'" selected="selected">'+item.item.text+'</option>');
                        //that.$el.append($options);
                    })
                    .on('removeAll', function() {
                        //that.uncheckAll();
                        //that.$el.empty();
                    })
                    .on('change', function() {
                        //updateMonitorCount();
                    })
                    .tagsinput({
                        onTagExists: function(item, $tag) {
                            //$tag.hide().fadeIn();//添加已经存在的，闪动效果
                        },
                        itemValue: function(item) { //add传入对象时，需定义itemValue方法
                            return (typeof item == 'object') ? item.text : item;
                        }
                    })[0].$container;
                this.$uncheckAll.off().on('click', function() {
                    that.uncheckAll();
                    that.$tagsinput.tagsinput('removeAll');
                });
                this.$checkAll.off().on('click', function() {
                    var items = [];
                    that.$selectItems.filter(':not(:checked)').each(function(){
                        items.push({
                            id: this.value,
                            text: this.title
                        });
                        $(this).attr('checked', true);
                    });
                    //添加监测点
                    that.$tagsinput.tagsinput('adds', items);
                });
                if (this.options.outerBtn)
                    this.$outerBtn.off().on('click', function() {
                        that.options.outerBtnClick();
                    });
            }
            /**end**/
        },

        open: function() {
            if (this.$choice.hasClass('disabled')) {
                return;
            }
            this.options.isOpen = true;
            this.$choice.find('>div').addClass('open');
            /**样式**/
            this.$choice.addClass('isopen');
            /**end**/
            this.$drop.show();
            /**1**/
            if (this.options.url) {
                this.options.onOpen();
                return;
            }
            /**end**/
            // fix filter bug: no results show
            this.$selectAll.parent().show();
            this.$noResults.hide();

            if (this.options.container) {
                var offset = this.$drop.offset();
                this.$drop.appendTo($(this.options.container));
                this.$drop.offset({
                    top: offset.top,
                    left: offset.left
                });
            }
            if (this.options.filter) {
                this.$searchInput.val('');
                this.filter();
            }
            this.options.onOpen();
        },

        close: function() {
            /**全选重置为空**/
            var selects = this.getSelects('text');
            if (!this.options.url && this.options.selectAllToEmpty) {
                if (selects.length === this.$selectItems.length + this.$disableItems.length) {
                    this.uncheckAll();
                }
            }
            /**end**/
            /**选项条目不符合设置提示 && 1**/
            if (this.options.miniSelection && (!this.$selectItems.filter(':checked').length || this.options.url && !this.$tagsinput.tagsinput('items').length)) {
                var $span = this.$choice.find('>span');
                $span.html('<span style="color:red">' + this.options.miniSelectionText + '</span>');
                return false;
            }
            /**end**/
            this.options.isOpen = false;
            this.$choice.find('>div').removeClass('open');
            /**样式**/
            this.$choice.removeClass('isopen');
            /**end**/
            this.$drop.hide();
            if (this.options.container) {
                this.$parent.append(this.$drop);
                this.$drop.css({
                    'top': 'auto',
                    'left': 'auto'
                });
            }
            this.options.onClose();
            /**触发triggerHandler('change')**/
            this.update(true);
            /**end**/
        },

        update: function() {
            var selects = this.getSelects('text'),
                $span = this.$choice.find('>span');
            /**end**/
            /**选中值变更，触发Change事件**/
            var change = false,
                count = 0;

            var elVal = this.$el.val(),
                values = this.getSelects();

            if (!elVal) elVal = []; //当$el无选项时，val为null
            if (elVal.length == values.length && elVal.length == 0) {
                change = false;
            } else if (elVal.length == values.length && elVal.length != 0) {
                for (var i = 0, l = values.length; i < l; i++) {
                    if ($.inArray(values[i], elVal) == -1) {
                        change = true;
                    };
                }
            } else {
                change = true;
            }

            if (change) {
                if (arguments.length) this.$el.triggerHandler('change');
                var texts = selects.join(',');
                $span.removeClass('placeholder').html(texts);
                this.$choice.prop('title', texts);
                if (this.options.url) this.$el.html(this.dataToOptions(this.$tagsinput.tagsinput('items'), true));
            };               

            if (!values.length) {
                this.$choice.prop('title', this.options.placeholder);
            }
            if (values.length && this.options.url) {
                this.$clear.show();
            } else {
                this.$clear.hide();
            }

            //items = this.$tagsinput.tagsinput('items');

            if (selects.length === this.$selectItems.length + this.$disableItems.length && this.options.allSelected) { /**全选**/
                $span.removeClass('placeholder').html(this.options.allSelected);
            } else if (selects.length > this.options.minumimCountSelected && this.options.countSelected) { /**达到简写数量限制**/
                $span.removeClass('placeholder').html(this.options.countSelected
                    .replace('#', selects.length)
                    .replace('%', this.$selectItems.length + this.$disableItems.length));
            } else if (selects.length) { /**有选中**/
                $span.removeClass('placeholder').html(selects.join(', '));
            } else { /**无选中**/
                $span.addClass('placeholder').html(this.options.placeholder);
            }
            // set selects to select
            /**1**/
            if (!this.options.url)
            /**end**/
                this.$el.val(this.getSelects());
        },

        updateSelectAll: function() {
            var $items = this.$selectItems.filter(':visible');
            this.$selectAll.prop('checked', $items.length &&
                $items.length === $items.filter(':checked').length);
            if (this.$selectAll.prop('checked')) {
                this.options.onCheckAll();
            }
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
            var that = this,
                texts = [],
                values = [];
            /**1**
             **/
            if (that.options.url) {
                var items = this.$tagsinput.tagsinput('items'),
                    item;
                for (var i = 0, l = items.length; i < l; i++) {
                    item = items[i];
                    texts.push(item.text);
                    values.push(item.id);
                }
                return type === 'text' ? texts : values;
            }
            /**end**/
            this.$drop.find('input[' + this.selectItemName + ']:checked').each(function() {
                texts.push($(this).parent().text());
                values.push($(this).val());
            });

            if (type === 'text' && this.$selectGroups.length) {
                texts = [];
                this.$selectGroups.each(function() {
                    var html = [],
                        text = $.trim($(this).parent().text()),
                        group = $(this).parent().data('group'),
                        $children = that.$drop.find('[' + that.selectItemName + '][data-group="' + group + '"]'),
                        $selected = $children.filter(':checked');

                    if ($selected.length === 0) {
                        return;
                    }

                    html.push('[');
                    html.push(text);
                    if ($children.length > $selected.length) {
                        var list = [];
                        $selected.each(function() {
                            list.push($(this).parent().text());
                        });
                        html.push(': ' + list.join(', '));
                    }
                    html.push(']');
                    texts.push(html.join(''));
                });
            }
            return type === 'text' ? texts : values;
        },

        setSelects: function(values) {

            /**当传入值为空，或者与全选值相匹配，则视为全选**/
            if (values === '' || values === this.options.selectAllValue) {
                this.checkAll();
                this.$choice.find('span').text(this.options.selectAllText).removeClass('placeholder');
                this.update();
                return;
            }
            if (typeof values == 'string' || typeof values == 'number') {
                values = [values];
            }
            /**end**/
            var that = this;
            this.$selectItems.prop('checked', false);
            $.each(values, function(i, value) {
                /**
                that.$selectItems.filter('[value="' + value + '"]').prop('checked', true);
                **/
                that.$selectItems.filter('[value="' + value + '"]').prop('checked', false).trigger('click');
                /**end**/
            });
            this.$selectAll.prop('checked', this.$selectItems.length ===
                this.$selectItems.filter(':checked').length);
            this.update();
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
            /**
            this.update();
            **/
            this.options.onCheckAll();
        },

        uncheckAll: function() {
            this.$selectItems.prop('checked', false);
            this.$selectGroups.prop('checked', false);
            this.$selectAll.prop('checked', false);
            /**
            this.update();
            **/
            this.options.onUncheckAll();
        },

        focus: function() {
            this.$choice.focus();
            this.options.onFocus();
        },

        blur: function() {
            this.$choice.blur();
            this.options.onBlur();
        },
        /**1.tagsinput**/
        pagerBuilder: function() {
            var that = this;
            //分页粒度
            if (that.$pager) that.$pager.remove();

            that.$pager = $('<select class="pull-left" style="width:50px" />')
            var pagerHtml = '',
                aLengthMenu = [10,50,100,1000],
                iDisplayLength = that.iDisplayLength;
            for (var i = 0, l = aLengthMenu.length; i < l; i++) {
                pagerHtml += '<option name="iDisplayLength" value="' + aLengthMenu[i] + '"' + (iDisplayLength == aLengthMenu[i] ? ' selected="selected"' : '') + '>' + aLengthMenu[i] + '</option>';
            }
            that.$pager.html(pagerHtml).on('change', function(){
                that.iDisplayLength = this.value;
                that.getData(function(data) {
                    that.updateLis(data.data);
                    that.updateChecked();
                    that.paginationBuilder(data);
                    that.pagerBuilder();
                });
            });
            that.$pagination.prepend(that.$pager);
        },
        paginationBuilder: function(data) {
            var that = this;
            //pagination
            that.$pagination.pagination({
                items: data.total,
                iDisplayLength: that.iDisplayLength,
                iDisplayStart: that.iDisplayStart,
                prevText: '<',
                nextText: '>',
                displayedPages: 0,
                edges: 0,
                pInfo:"_PAGE_/_PAGES_",
                cssStyle: 'light-theme row',
                onPageClick: function(iDisplayStart, iDisplayLength, pageNumber, event, self) {
                    that.iDisplayStart = iDisplayStart;
                    that.getData(function(data) {
                        that.updateLis(data.data);
                        that.updateChecked();
                    });
                    that.pagerBuilder();                 
                    return false;
                }
            });
        },
        /**end**/

        refresh: function() {
            /**1**
            this.init();
            **/
            var that = this;
            if (that.options.url) {
                that.getData(function(data) {
                    that.updateLis(data.data);
                    that.updateChecked();
                    that.paginationBuilder(data);
                    that.pagerBuilder();
                });
            } else {
                this.init();
            }
            /**end**/
        },

        /**加载数据**/
        loadData: function(data) {
            this.$parent.remove();
            this.options.initData = data;
            this.init();
        },
        /**end**/

        filter: function() {
            var that = this,
                text = $.trim(this.$searchInput.val()).toLowerCase();
            /**1**/
            if (that.options.url) {
                return;
            }
            /**end**/
            if (text.length === 0) {
                this.$selectItems.parent().show();
                this.$disableItems.parent().show();
                this.$selectGroups.parent().show();
            } else {
                this.$selectItems.each(function() {
                    var $parent = $(this).parent();
                    $parent[$parent.text().toLowerCase().indexOf(text) < 0 ? 'hide' : 'show']();
                });
                this.$disableItems.parent().hide();
                this.$selectGroups.each(function() {
                    var $parent = $(this).parent();
                    var group = $parent.attr('data-group'),
                        $items = that.$selectItems.filter(':visible');
                    $parent[$items.filter('[data-group="' + group + '"]').length === 0 ? 'hide' : 'show']();
                });
                /**bug**
                //Check if no matches found
                if (this.$selectItems.filter(':visible').length) {
                    this.$selectAll.parent().show();
                    this.$noResults.hide();
                } else {
                    this.$selectAll.parent().hide();
                    this.$noResults.show();
                }
            }
            **/
            }
            //Check if no matches found
            if (this.$selectItems.filter(':visible').length) {
                this.$selectAll.parent().show();
                this.$noResults.hide();
            } else {
                this.$selectAll.parent().hide();
                this.$noResults.show();
            }
            /**end**/
            this.updateOptGroupSelect();
            this.updateSelectAll();
        },
        /**1**/
        getData: function(callback) {
            if (this.ajax) {
                this.ajax.abort();
                this.ajax = null;
            }
            var _this = this,
                data = [];

            var iDisplayLength = 10;
            if (_this.iDisplayLength) {
                iDisplayLength = _this.iDisplayLength
            }
            data.push({
                name: 'iDisplayLength',
                value: iDisplayLength
            });

            var iDisplayStart = 0;
            if (_this.iDisplayStart) {
                iDisplayStart = _this.iDisplayStart
            }
            data.push({
                name: 'iDisplayStart',
                value: iDisplayStart
            });

            var name = '';
            if (_this.$searchInput) {
                name = $.trim(_this.$searchInput.val()).toLowerCase()
            }
            data.push({
                name: 'name',
                value: name
            });

            if (typeof _this.options.serverParams == 'function') {
                var contactData = _this.options.serverParams(),
                    item;
                for (var index = 0, length = contactData.length; index < contactData.length; index++) {
                    data.push(contactData[index]);
                }
            }

            this.ajax = $.ajax({
                url: _this.options.url,
                data: data,
                global: false,
                success: function(data) {
                    callback(data);
                    if (data.data.length) {
                        _this.$selectAll.parent().show();
                        _this.$noResults.hide();
                    } else {
                        _this.$selectAll.parent().hide();
                        _this.$noResults.show();
                    }
                }
            });
        }
        /**end**/
    };

    $.fn.multipleSelect = function() {
        var option = arguments[0],
            args = arguments,

            value,
            allowedMethods = [
                'getSelects', 'setSelects',
                'enable', 'disable',
                'checkAll', 'uncheckAll',
                /**加载数据**/
                "loadData",
                "open",
                "close",
                /**end2b**/
                'focus', 'blur',
                'refresh'
            ];

        this.each(function() {
            var $this = $(this),
                data = $this.data('multipleSelect'),
                options = $.extend({}, $.fn.multipleSelect.defaults,
                    $this.data(), typeof option === 'object' && option);

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
                /**1**/
                if (options.url) {
                    var error = false,
                        errorText = 'multipleSelect需依赖插件：';
                    if (!$.fn.tagsinput) {
                        errorText += 'tagsinput ';
                        error = true;
                    }
                    if (!$.fn.pagination) {
                        errorText += 'pagination ';
                        error = true;
                    }
                    if (error) {
                        if (window.console && console.log) {
                            alert(errorText);
                            console.log(errorText)
                        } else {
                            throw new Error(errorText);
                        }
                        return;
                    }
                    data.refresh();
                }
                /**end**/

            }
        });

        return value ? value : this;
    };

    $.fn.multipleSelect.defaults = {
        name: '',
        isOpen: false,
        placeholder: '请选择...',
        clearAll:true,
        clearAllText: '清空',
        selectAll: true,
        selectAllText: '全选',
        allSelected: '',
        /**'全部'**/
        minumimCountSelected: 18,
        countSelected: '已选#个选项', //'选中#个，总%个选项',
        multiple: false,
        multipleWidth: 'auto',
        single: false,
        filter: true,
        /**搜索框阀值**/
        minimumResultsForSearch: 18,
        /**end**/
        /**无匹配选项**/
        noMatchesText: '无匹配选项',
        /**end**/
        width: undefined,
        maxHeight: 250,
        container: null,
        position: 'bottom',
        keepOpen: false,
        /**新增initData**/
        initData: [],
        customParams: false,
        /**end**/
        /**全选值**/
        selectAllValue: '',
        /**end**/
        /**必选设置**/
        miniSelection: false,
        miniSelectionText: '必选一项',
        /**end**/
        /**1**/
        url: null,
        serverParams: null,
        initSelection: [],
        clear: true,
        /**end**/
        /**全选重置为空**/
        selectAllToEmpty: false,
        /**end**/
        /**外部按钮**/
        outerBtn: false,
        outerBtnClick: function() {
            //
        },
        /**end**/

        styler: function() {
            return false;
        },

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
        onFocus: function() {
            return false;
        },
        onBlur: function() {
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