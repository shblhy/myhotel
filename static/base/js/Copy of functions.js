/*
 * utf-8 编码
 */
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
		 $('a').click(
		 	function() {
		 		if ($(this).attr("href")=="javascript:void(0)" && $(this).data("href")){
		 			$.ajax({
		 				url:$(this).data("href"),
		 				dataType:"html",
		 				success:function(page){
		 					$("div#main").html(page);
		 				}
		 			});
		 		}
		 	});
		},
		load_page : function(target, page_container){
			if (!page_container){
				$page_container = $("#main");
			}else{
				$page_container = $("#" + page_container);
			}

			$.ajax({
				url: target,
				before : function() {
				},
				error : function(XMLHttpRequest, textStatus, errorThrown) {
				},
				success: function(data, textStatus, xhr) {
					$page_container.html(data);
				},
				complete: function(xhr) {
				}
			})
			.fail(function() {
					//
				})
			.done(function(data, status, xhr) {

			})
			.always(function() {
					//
				})
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
