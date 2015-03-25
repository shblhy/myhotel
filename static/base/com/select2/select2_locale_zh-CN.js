/**
 * Select2 Chinese translation
 */
(function ($) {
    "use strict";
    $.extend($.fn.select2.defaults, {
        formatNoMatches: function () { return "无可选项"; },
        formatInputTooShort: function (input, min) { var n = min - input.length; return "请输入" + n + "个字符筛选";},
        formatInputTooLong: function (input, max) { var n = input.length - max; return "请删除" + n + "个字符";},
        formatSelectionTooBig: function (limit) { return "最多选择" + limit + "项"; },
        formatLoadMore: function (pageNumber) { return "加载结果中..."; },
        formatSearching: function () { return "查询中..."; }
    });
})(jQuery);
