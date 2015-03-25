/*
 *1.调用 $.xhrPool.abortAllAjaxs() 终止所有请求
 *2.错误结果处理
 *
 *
 *
 */


(function($) {
	/***1.调用 $.xhrPool.abortAllAjaxs() 终止所有请求***/
	$.xhrPool = []; // 数组保存未完成请求
	$.xhrPool.abortAllAjaxs = function() { // 终止请求函数
		$(this).each(function(idx, xhr) {
			// 若在请求状态，则可以终止
			if (xhr && xhr.readystate != 4) {
				xhr.abort();
			}
		});
		$.xhrPool.length = 0;
	};
	/***end2***/

	$.ajaxSetup({
		beforeSend: function(xhr, ajaxObj) {
			/***1.调用 $.xhrPool.abortAllAjaxs() 终止所有请求***/
			// 在发送全局请求前将请求保存在数组，只保存可中断【即 abortable 未定义 || abortable 为true】的请求
			if (typeof ajaxObj.abortable == 'undefined' || ajaxObj.abortable == true) {
				$.xhrPool.push(xhr);
			}
			/***end2***/

			//备份ajaxObj function
			var fn = {};
			$.each(ajaxObj, function(i, j) {
				if (typeof j == 'function') {
					fn[i] = j;
				}
			});

			//如果没声明type，默认get
			if (!ajaxObj.type) {
				ajaxObj.type = 'get';
			}
			//请求前处理
			if (fn.before) {
				fn.before();
			}

			ajaxObj = $.extend(ajaxObj, {
				error: function(XMLHttpRequest, textStatus, errorThrown) {
					var fullPage = /<!DOCTYPE/i;
					var contentPage = /<\//i;
					var errorPage = /errorpage.css/i;
					if (fullPage.test(XMLHttpRequest.responseText)) { //整个页面	
						/**1.BUG：谷歌浏览器容易脚本出错**/
						var newDoc = document.open("text/html", "replace");
						newDoc.write(XMLHttpRequest.responseText);
						newDoc.close();
						/******2.截取body内部代码******
								var rx = /<body[^>]*>([\s\S]+?)<\/body>/i;
								var body = rx.exec(XMLHttpRequest.responseText);
								if (body) body = body[1];
								$('body').html(body);
								/**3.超时返回登录页面处理
								document.location.reload();
							**/
					} else if (errorPage.test(XMLHttpRequest.responseText) || XMLHttpRequest.status == 200 && contentPage.test(XMLHttpRequest.responseText) ) { //500 404 403 400 错误页面 或者 由302重定向返回的200页面
						functions.render_html(XMLHttpRequest.responseText, null, XMLHttpRequest);
					} else if (XMLHttpRequest.responseText) { //非页面代码，提示错误信息
						if (XMLHttpRequest.status != 500) { //500不打印
							//错误提示						
							if (noty) {
								noty({
									text: XMLHttpRequest.responseText,
									type: 'error',
									dismissQueue: true,
									layout: 'top'
								});
							} else {
								alert(XMLHttpRequest.responseText);
							}
						}
					}
					/***end2***/

					//调用备份ajaxObj function
					if (fn.error) {
						fn.error(XMLHttpRequest, textStatus, errorThrown);
					}
				},
				success: function(data, textStatus, xhr) {
					//调用备份ajaxObj function
					if (fn.success) {
						fn.success(data, textStatus, xhr);
					}
				},
				complete: function(xhr) {

					/***1.调用 $.xhrPool.abortAllAjaxs() 终止所有请求***/
					// 若有请求完成，在数组里删除
					var index = $.inArray(xhr, $.xhrPool);
					if (index > -1) {
						$.xhrPool.splice(index, 1);
					}
					/***end2***/

					//调用备份ajaxObj function
					if (fn.complete) {
						fn.complete(xhr);
					}
				}
			});
		}
	});
})(jQuery);