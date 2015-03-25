/*1.新增percent
 *2.支持class标记class=“meter”内部的容器进度条
 *3.新增bubble定位属性
 *4.新增加载100%后显示文字
 *
 *
 *
 *注释：进度回退是无回调callback
 *
 *
 */
(function($) {
  $.fn.formProgress = function(options) {
    var settings = { /*--begin 新增percent与callback--*/
      percent: 'off',
      callback: '',
      /*--end--*/
      speed: 300,
      style: "green",
      bubble: false,
      /***3.新增bubble定位属性***/
      bubblePosition: null,
      /***end3***/
      /***3.新增bubble定位属性***/
      fullPercentText: null,
      /***end3***/
      selector: "",
      minPercent: false,
      message: "Please fill the form fields !"
    };
    if (options) {
      $.extend(settings, options);
    }
    return this.each(function() {
      var obj = $(this);
      /*--begin 新增css--*/
      obj.css('float', 'left');
      /*--end--*/
      var fields = $(settings.selector).not(":radio").length;
      var names = [];
      $(settings.selector + ":radio").each(function() {
        var n = $(this).attr("name");
        if ($.inArray(n, names) < 0) {
          names.push(n);
        }
      });
      fields = fields + names.length;
        /***3.新增bubble定位属性**
      if (settings.bubble && (obj.parent().find(".bubble").length == 0)) {
        obj.parent().append("<div class=\"bubble\"><div class=\"percent\" style=\"color:" + settings.style + "\"></div><div class=\"arrow\"></div><div class=\"arrow-center\"></div></div>");
        */
      if (settings.bubble && (obj.parent().find(".percent").length == 0)) {
        if (settings.bubblePosition == 'center') {
          obj.parent().append("<div class=\"bubblecenter\"><div class=\"percent\"></div></div>");
        } else {
          obj.parent().append("<div class=\"bubble\"><div class=\"percent\" style=\"color:" + settings.style + "\"></div><div class=\"arrow\"></div><div class=\"arrow-center\"></div></div>");
        }
        /***end3***/
      }
      /*--begin 新增percent--
      if(fields.length!=0){
    */
      if ((fields.length != 0) || (settings.percent === 'off')) {
        /*end*/
        var last = obj.attr("data-percent") < 0 ? 0 : obj.attr("data-percent");
        var ratio = obj.parent().width() / 100;
        var inputs = $(settings.selector + "[value!='']").not(":checkbox").not(":radio").length + $(settings.selector + ":checked").length;
        /*--begin 新增percent--
        var percent=Math.round((inputs/fields)*100);
      */
        var percent = (settings.percent === 'off') ? Math.round((inputs / fields) * 100) : settings.percent;
        /*end*/
        var from = (Math.round(((inputs - 1) / fields) * 100)) < 0 ? 0 : Math.round(((inputs - 1) / fields) * 100);
        var bubble = obj.parent().find(".bubble");
        /***3.新增bubble定位属性***/
        var bubblecenter = obj.parent().find(".bubblecenter");
        /***end3***/
        /**2.支持class标记class=“meter”内部的容器进度条**
        obj.removeClass().addClass(settings.style);
        */
        obj.addClass(settings.style);
        /***end2***/
        if (settings.minPercent != "undefined") {
          preventSubmit(settings.selector, settings.minPercent, settings.message);
        }
        if (last > percent) {
          obj.parent().find("." + settings.style).stop().animate({
            width: percent * ratio
          }, settings.speed);
          /***3.新增bubble定位属性**
          if (bubble.length != 0) {
            bubble.find(".percent").empty().append(percent == 0 ? "0%" : percent + "%");
            bubble.stop().animate({
              left: percent * ratio
            }, settings.speed);
          */
          if (settings.bubble) {
            if (settings.bubblePosition == 'center') {
              /***4.新增加载100%后显示文字**
              bubblecenter.find(".percent").empty().append(percent == 0 ? "0%" : percent + "%");
              */
              bubblecenter.find(".percent").empty().append((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
              /***end4***/              
            } else {
              bubble.find(".percent").empty().append((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
              bubble.stop().animate({
                left: percent * ratio
              }, settings.speed);
            }
          /***end3***/
          } else {
            obj.parent().find("." + settings.style).empty().text((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
          }
          obj.attr("data-percent", percent);
          return false;
        } else {
          if (last == percent && percent != 0) {
            return false;
          } else {
            /*--begin 新增callback--
            obj.parent().find("."+settings.style).stop().animate({width:percent*ratio},settings.speed);
            */
            obj.parent().find("." + settings.style).stop().animate({
              width: percent * ratio
            }, settings.speed, function() {
              obj.attr("data-percent", percent);
              if (settings.callback) {
                settings.callback.call(options);
              }
            });
            /*end*/
            /***3.新增bubble定位属性**
            if (bubble.length != 0) {
              bubble.find(".percent").empty().append(percent == 0 ? "0%" : percent + "%");
              bubble.stop().animate({
                left: percent * ratio
              }, settings.speed);
            */
            if (settings.bubble) {
              if (settings.bubblePosition == 'center') {
                bubblecenter.find(".percent").empty().append((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
              } else {
                bubble.find(".percent").empty().append((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
                bubble.stop().animate({
                  left: percent == 0 ? 0 : percent * ratio
                }, settings.speed);
              }
            /***end3***/
            } else {
              obj.parent().find("." + settings.style).empty().text((percent == 100 && settings.fullPercentText) ? settings.fullPercentText : percent + "%");
            }
            if(percent == 100){
              obj.addClass('static');
            }else{              
              obj.removeClass('static');
            }
          }
        }
        obj.attr("data-percent", percent);
      }
      /*--begin 新增percent--
      $(":input").bind("change keyup",function(){
        obj.formProgress(settings);
      });
      */
      if (settings.percent === 'off') {
        $(":input").bind("change keyup", function() {
          obj.formProgress(settings);
        });
      }
      /*end*/

      function preventSubmit(sel, minPercent, msg) {
        var setPercent = minPercent;
        var dispmessage = msg;
        var targetInput = $(sel).parents("form").find("input[type=submit]");
        targetInput.removeAttr("onclick");
        if (percent < setPercent) {
          targetInput.attr("onclick", "alert('" + dispmessage + "'); return false;");
        }
      }
      return false;
    });
  };
})(jQuery);