/*
 * utf-8 编码
 */
// define(["address"], function() {
define([], function() {
 	if (typeof (functions) == 'undefined') {
 		functions = {};
 	}

 	functions.base = { 		
 		alertme:function (){
 			alert('alerttest');
 		},
 		consoleme:function (){
 			console.log('consoletest');
 		},
 		set_all_aclick:function (){
		/*
		 * 当a标记的href指向javascript:void(0)且data-href属性不为空时，ajax请求data-href指向的页面，获取内容填充于div main
		 */
		 $('a').each(function(){
		 	if ($(this).attr("href")=="javascript:void(0)" && $(this).data("href")){
		 		if (!$(this).data('clickfunc')){
		 			$(this).attr('data-clickfunc',1);
				 	$(this).click(
					 	function() {
					 		//console.log('a click on '+$(this).text());
					 		functions.base.load_page($(this).data("href"));
					 			/*var _this = $(this);利用按钮获知页面加载状态
					 			var set_loading=function(){
						 				_this.attr('data-loading',1);
						 		};
						 		var stop_loading=function(){
						 				_this.attr('data-loading',0);
						 		};
					 			if (!_this.data('loading')){
						 			unctions.base.load_page($(this).data("href"),null,set_loading,null,stop_loading,null);
					 			}*/
					 			/*$.ajax({
					 				url:$(this).data("href"),
					 				dataType:"html",
					 				success:function(page){
					 					$("div#main").html(page);
					 				}
					 			});*/
			 		});}}
		 });
		},
		load_page : function(target, page_container,funcbefore,funcbeforeparms,funcdone,funcdoneparams){
			//console.log('load_page:'+target);
			if (!page_container){
				$page_container = $("#main");
			}else{
				$page_container = $("#" + page_container);
			}
			/*hishref = window.location.href;
			var anchor_filter = new RegExp('#');
			 if (anchor_filter.test(hishref)) { //当前地址与将抵达地址相同时，取消动作
               	if (hishref.split("#")[1] == target)
               		return false;
            }*/
			//$.address.value(target);
			$.ajax({
				url: target,
				before : function() {
					if (typeof(funcbefore)=="function"){
						funcbefore(funcbeforeparms);
					}
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
				},
				success: function(data, textStatus, xhr) {
					if (xhr.responseText.indexOf("<!DOCTYPE") == 0 || xhr.responseText.indexOf("<!doctype") == 0) {
						//$("html").html(xhr.responseText);
						//$("html").html('');
						document.write(xhr.responseText);
					}
					else{
						$page_container.html('');
						$page_container.html(data);
					}
				},
				complete: function(xhr) {
				}
			})
			.fail(function(data) {
				if (data.status=500){
					$('html').html("");
					$('html').html(data.responseText);
				}
				})
			.done(function(data, status, xhr) {
				if (typeof(funcbefore)=="function"){
					funcdone(funcdoneparams);
				}
			})
			.always(function() {
					//
				})
		},
		load_anchor:function(){
			//继续加载锚点指向页面
            var nowhref = window.location.href;
            var anchor_filter = new RegExp('#');
            if (anchor_filter.test(nowhref)) { //连接并带有锚点
                functions.base.load_page(nowhref.split("#")[1]);
            }
		}
	}
	functions.basefunc = {
		group_array : function(array) {
			var dataObject = {};
			for(var index in array){
				if(dataObject[array[index].name])
					dataObject[array[index].name] += ',';
				else
					dataObject[array[index].name] = '';

				dataObject[array[index].name] += array[index].value;
			}
			array = [];
			for(var index in dataObject){
				array.push({
					"name":index,
					"value":dataObject[index]
				});
			}
			return array;
		}
	}
	return functions;
});
