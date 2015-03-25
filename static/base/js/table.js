define(["dataTable", "functions", "fileupload", "tipped_plugin", "bootstrap", "address"], function(dataTable) {
	return {
		Table: function(containerName, options) {
			var _this = this;
			//定义Table对象
			this.$table = $('#' + containerName);
			this.options = options;
			this.init = false;//是否执行过drawTable
			
			this.search = function() {
				this.queryParams = this.getCondition();
				this.$table.fnClearTable();
			};
			this.destroy = function() {
				if (this.init){
					this.$table.fnDestroy();
					this.$table.empty();
				}
			};
			this.loadData = function(data) {
				this.$table.fnClearTable();
				this.$table.fnAddData(data);
			};

			this.getCondition = function() {
				if (this.options.getCondition) {
					return this.options.getCondition();
				} else {
					var dataArray = $('#' + this.$table.attr('data-search')).serializeArray();
					var res = window.functions.basefunc.group_array(dataArray);
					return res 
				}
			};
			this.getTable = function(){
				//使用现有参数获取表格数据并绘制
				this.queryParams = this.getCondition();
				var array = [];
				for (var key in this.queryParams) {
					array.push(key + "=" + this.queryParams[key]);
				}
				console.log(_this.options.sAjaxSource + array.join("&"));
				$.ajax({
					url: _this.options.sAjaxSource +"?"+ array.join("&"),
					type: "get",
					dataType: "json",
					global: false,
					success: function(data) {
						var queryData = false;
						_this.destroy();
						_this.options.initData = data;
						_this.drawTable();
					}
				});
			};
			
			this.queryParams = this.getCondition();
			
			this.defaultRowCallback = function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
				/*todo默认行回调，一段待修改的烂代码*/
				//转换操作数据格式
				options = _this.options;
				options.actions = options.actions || [];
				var actionsArray = {};
				for (var ii in options.actions) {
					actionsArray[options.actions[ii].type] = options.actions[ii];
				}
				var $actions = $('td:last', nRow),actionIndex = null;

				//判断最后一列sTitle为空或为操作则为操作列
				if (options.aoColumns[options.aoColumns.length - 1].sTitle == "" || options.aoColumns[options.aoColumns.length - 1].sTitle == "操作")
					actionIndex = options.aoColumns.length - 1;
				else
					return;
				//操作列无操作符，返回
				if (!aData[actionIndex])
					return;

				//更多操作 容器
				var $moreActionWrapper = $('<span class="dropdown"><a class="dropdown-toggle" href="javascript:void(0)" data-hover="dropdown" data-toggle="dropdown"><i title="更多" class="icon-more icon-color" ></i></a><ul class="dropdown-menu pull-right"></ul></span>');
				var $moreAction = $moreActionWrapper.find('.dropdown-menu');

				var hasAction = false,
					keepAction = [],
					actions = aData[actionIndex].split(',');
					
				for (var index in actions) {					
					//可以定义默认复杂的操作，默认情况下，定义了详情、编辑、删除，三个操作。
					var $action = _this.get_action_item(nRow, aData, iDisplayIndex, iDisplayIndexFull, actionsArray, actions[index],$moreAction);
					keepAction.push($action);
					$moreAction.append($action);
					}
				//普通操作容器无操作 则不追加
				if (keepAction.length) {
					$actions.empty();
					for (var index in keepAction) {
						$actions.append(keepAction[index]);
					}
				}
				//更多操作容器无操作 则不追加
				if ($moreAction.children().get(0))
					$actions.append($moreActionWrapper);
			}

			this.drawTable = function() {
				//在数据齐全的情况下绘制表格，无需重新查询
				//todo
				var _this = this;

				var bServerSide = options.sAjaxSource ? true : false;
				var defaults = {
					"buttons": [],
					"aaSorting": [],
					"bSortClasses": false,

					"asStripeClasses": ['odd', 'even'],
					"bPaginate": true,
					"bServerSide": bServerSide,
					"bLengthChange": true,
					"bSort": true,
					"bInfo": true,

					"aLengthMenu": [15, 30, 60],
					"iDisplayLength": 30,
					"iDisplayStart": 0,
					"trHighlight": true,

                    //"sScrollX": "100%",
                    "bAutoWidth": true,

					"checkboxSelect": true,
					"fnDrawCallback": function(a) {
						$('.dropdown-toggle').dropdownHover().dropdown();
					},
					"sServerCallback": {
						'ready': function() {},
						'fail': function(xhr, error, thrown) {},
						'done': function(json, status) {
							if (json.rows) {
								return {
									//'sEcho' : json.sEcho,
									'iTotalRecords': json.total,
									'iTotalDisplayRecords': json.total,
									'aaData': json.rows
								}
							} else {
								return json;
							}
						},
						'always': function(XHR, TS) {}
					},
					"fnInitComplete": function() {
						//_this.init = false;
					},
					"fnServerParams": function(aoData) {
						var aLen = aoData.length;
						for (var i =0;i< aLen;i++){//清理mDataProp
							if (aoData[aLen-parseInt(i)-1].name.substring(0,9) =="mDataProp"){
								aoData.splice(aLen-parseInt(i)-1,1);
							};
						}
						var conditions = _this.queryParams;
						if (conditions[0]==null){
							for (var index in conditions)		
								aoData.push({"name":index,"value":conditions[index]});
						}
						else{
							for (var index in conditions)
								aoData.push(conditions[index]);
						}
						//保存地址栏历史记录以便回退
						/*(目前关闭该功能更)
						if (!_this.init && options.sAjaxSource && options.address == true) {
							if ($.address.path()) {
								$.address.value($.address.path() + '?' + $.map(aoData, function(item, index) {
									return item.name + '=' + item.value;
								}).join('&'));
							}
						}*/

					},
					"fnCreatedRow": options.fnCreatedRow?options.fnCreatedRow :_this.defaultCreatedRow,
					"fnRowCallback": options.fnRowCallback?options.fnRowCallback :_this.defaultRowCallback,
					
				};
				var option = {};
				option = $.extend(true, defaults, options);
				//buttons
				var buttons = [];
				if (option.buttons) {
					var btn = option.buttons;
					newButtons = []
					for (var index in btn) {
						/*todo 增删导出导入，待优化的代码*/
						switch (btn[index].type) {
							case 'del':
								var del = $.extend(true, {
									"text": "删除",
									"type": "del",
									"url": btn[index].url,
									"btnClass": "small-margin-right",
									"fn": {
										"click": function(oSettings) {
											var url = $(this).attr('href');
											var values = oSettings.oInstance.fnGetSelected();
											if (values && values.length) {
												$.ajax({
													url: url,
													type: 'post',
													dataType: 'script',
													data: {
														ids: values.join(',')
													},
													success: function() {
														_this.$table.fnClearTable();
													}
												});
											}
											return false;
										}
									}
								}, btn[index]);
								buttons.push(del);
								break;
							case 'add':
								var add = $.extend(true, {
									"text": "新增",
									"type": "add",
									"url": btn[index].url,
									"btnClass": "small-margin-right"
								}, btn[index]);
								buttons.push(add);
								break;
							case 'export':
								var _export = $.extend(true, {
									"text": "导出",
									"type": "export",
									"url": btn[index].url,
									"btnClass": "btn pull-right",
									"fn": {
										"click": function(oSettings) {
											var url = $(this).attr('href');
											var res = []
											for (var v in _this.queryParams){
												res.push(_this.queryParams[v].name + '=' + _this.queryParams[v].value);
											}
											window.open(url +'?' + res.join('&'));
											return false;
										}
									}
								}, btn[index]);
								buttons.push(_export);
								break;
							case 'import':
								var _import = $.extend(true, {
									"text": "导入",
									"type": "import",
									"html": "<span class='btn btn-success fileinput-button'><i class='icon-add icon-white'></i><span>" + btn[index].text + "</span><input id='fileupload' type='file' name='file'></span>"
								}, btn[index]);
								_this.uploadUrl = btn[index].url;
								for(var indexx in btn[index]){
									if(typeof btn[index][indexx] == 'function'){
										_this.uploadCallback = btn[index][indexx];
										break;
									}
								}
								buttons.push(_import);
								break;
							default:
								var other = $.extend(true, {
									"btnClass": "btn small-margin-right"
								}, btn[index]);
								buttons.push(other);
						}
					}
				}
				option.buttons = buttons;
				_this.table = _this.$table.dataTable(option);
				this.init = true;
				if (_this.uploadUrl)
					_this.render_import();
				functions.base.set_all_aclick();
			};
			
			this.render_import = function(){
				$('#fileupload').fileupload({
					url: _this.uploadUrl,
					dataType: 'json',
					add: function(e, data) {
						var uploadErrors = [];
						var acceptFileTypes = /(\.)(csv)$/i;
						if (!acceptFileTypes.test(data.originalFiles[0]['name'])) {
							uploadErrors.push('上传文件类型不支持');
						}
						if (data.originalFiles[0]['size'] > 512000) { //5120 / 1024 kb/m = 5m
							uploadErrors.push('上传文件大于5M');
						}
						if (uploadErrors.length > 0) {
							var info = '';
							for (var index in uploadErrors) {
								if (uploadErrors[index])
									info += '<span style="color:red;font-weight:bold;">' + uploadErrors[index] + '</span><br>';
							}
							Tipped.create('#fileupload', info, {
								skin: 'white',
								hideOnClickOutside: true,
								showOn: false,
								hideOn: false,
								closeButton: true,
								hook: 'topmiddle',
								maxWidth: 190,
								stem: false,
								offset: {
									x: 0
								}
							}).show();
						} else {
							data.submit();
						}
					},
					done: function(e, data) {
						//_this.$table.fnClearTable();
						if(_this.uploadCallback){//外部传入回调函数
							_this.uploadCallback.call(e, _this.$table, data);
						}else{//外部无回调函数，默认操作
							//
						}
					},
					progressall: function(e, data) {}
				})
			};
			
			this.get_action_item = function(nRow, aData, iDisplayIndex, iDisplayIndexFull,actionsArray,action,$moreAction){
				var actionItem = actionsArray[action];
				if (!actionItem) return;
				if (action == "delete") {
					var url = actionItem ? actionItem.url : 'javascript:void(0)';
					var $action = $('<a class="small-margin-right" href="' + url + '"><i title="删除"  class="icon-delete icon-color"></i></a>').click(function() {
						url = $(this).attr('href');
						var index = _this.$table.fnFindCellRowIndexes(aData[0], 0);
						if (index.length) {
							if (confirm("确认执行删除")){
								$.ajax({
									url: url,
									type: 'post',
									dataType: 'script',
									data: {
										ids : aData[0]
									},
									success: function(XMLHttpRequest, textStatus) {
										_this.$table.fnDeleteRow(index[0]);
									}
								});
							}
						}
						return false;
					})
				}else{
						var $action;
						//增加额外参数
						var dataParams = '',data = actionItem.data;
						if (data) {
							for (var iii in data) {
								if (dataParams) dataParams = dataParams + '&';
								dataParams += (iii + '=' + data[iii]);
							}
						}
						
						if (actionItem.style == 'restful') {
							var url = actionItem.url + '/' + aData[0] + (actionItem.urlSuffix ? '/' + actionItem.urlSuffix : '') + (dataParams ? '?' + dataParams : '');
						} else if (actionItem.url) {
							var url = actionItem.url + '?' + (actionItem.paramName || 'id') + '=' + aData[0] + (dataParams ? '&' + dataParams : '');
						}
	
						var target = actionItem.target ? 'target="' + actionItem.target + ' "' : '';
						if (target == "target=data- "){
							target = "data-"
						}
						if (typeof action == "string") {
							(function(actionsArray) {
	
								//是否隐性操作符 追加到 更多
								if (actionsArray.container == 'more') {
									//组装a连接
									$action = $('<li><a ' + target + 'href="' + (url || 'javascript:void(0)') + '">' + actionsArray.text + '</a></li>');
								} else {
									//组装a连接
									$action = $('<a ' + target + ' class="small-margin-right" href="' + (url || 'javascript:void(0)') + '">' + (actionsArray.iconClass ? '<i title=' + actionsArray.text + ' class="' + actionsArray.iconClass + '"></i>' : actionsArray.text) + '</a>');
								}
	
								$action.click(function() {
									var __this = this;
									var url = $(this).attr('href');
									if (typeof actionsArray.click == "function") {
										actionsArray.click.call(this, {
											table: _this.$table,
											url: url,
											moreAction: $moreAction,
											aData: aData
										});
										return false;
									} else if (actionsArray.ajax == true) { //删除等异步操作
										if(!$(__this).hasClass('disable')){
											$(__this).addClass('disable').html('<img title="'+actionsArray.text+'中..." src="/static/images/operator/loading.gif" >');
											$.ajax({
												url: url,
	                        					dataType : "json",
												global:false,
												success: function(data, status, xhr) {
													if($(__this).is(':visible')){
														if (typeof actionsArray.success == "function") {
															actionsArray.success(data, status, xhr);
														}else{
															_this.$table.fnUpdate(data, iDisplayIndex);
														}
			                                        }
												}
											});
										}
										return false;
									}
								});
							})(actionItem)
						}
				}
				return $action;
			}
			
			this.defaultRowCallbackBak = function(nRow, aData, iDisplayIndex, iDisplayIndexFull) {
				/*todo默认行回调，一段待修改的烂代码*/
				//转换操作数据格式
				options = _this.options;
				options.actions = options.actions || [];
				var actionsArray = {};
				for (var ii in options.actions) {
					actionsArray[options.actions[ii].type] = options.actions[ii];
				}
				var $actions = $('td:last', nRow),actionIndex = null;

				//判断最后一列sTitle为空则为操作列
				if (options.aoColumns[options.aoColumns.length - 1].sTitle == "" || options.aoColumns[options.aoColumns.length - 1].sTitle == "操作")
					actionIndex = options.aoColumns.length - 1;
				else
					return;
				//操作列无操作符，返回
				if (!aData[actionIndex])
					return;

				//更多操作 容器
				var $moreActionWrapper = $('<span class="dropdown"><a class="dropdown-toggle" href="javascript:void(0)" data-hover="dropdown" data-toggle="dropdown"><i title="更多" class="icon-more icon-color" ></i></a><ul class="dropdown-menu pull-right"></ul></span>');
				var $moreAction = $moreActionWrapper.find('.dropdown-menu');

				var hasAction = false,
					keepAction = [],
					actions = aData[actionIndex].split(',');
					
				for (var index in actions) {
					//可以定义默认复杂的操作
					
				}
				//普通操作容器无操作 则不追加
				if (keepAction.length) {
					$actions.empty();
					for (var index in keepAction) {
						$actions.append(keepAction[index]);
					}
				}
				//更多操作容器无操作 则不追加
				if ($moreAction.children().get(0))
					$actions.append($moreActionWrapper);
			}

		}
	}
});