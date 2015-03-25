/*1.增加标题容器
 *2.insertOption方法，数据格式：[{name:'',value:'',selected:false,optgroup:false}]；addOption方法，数据格式：[{name:'a',children:[{name:'',value:'',selected:false}]}]
 *3.新增清空方法clearOption
 *4.BUG:双击不应在el源列表有移出动作
 *5.新增方法setVal，传入ID或value，如：["a","b","c"]
 *6.新增方法getVal/getName，输出 ('all'或数组 如：["a","b","c"])/('全部'或字符串 如：'a,b,c') ; val/name 只输出数组
 *
 *
 * multiselect2side jQuery plugin
 *
 * Copyright (c) 2010 Giovanni Casassa (senamion.com - senamion.it)
 *
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 *
 * http://www.senamion.com
 *
 */

(function($)
{
	// SORT INTERNAL
	function internalSort(a, b) {
		var compA = $(a).text().toUpperCase();
		var compB = $(b).text().toUpperCase();
		return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
	};

	var methods = {
		init : function(options) {
			var o = {
				selectedPosition: 'right',
				moveOptions: true,
				labelTop: '置顶',
				labelBottom: '置底',
				labelUp: '上移',
				labelDown: '下移',
				labelSort: '顺排',
				/*1.增加标题容器----*/
				leftContainer:'',
				/*--end--*/
				labelsx: '可选',
				/*1.增加标题容器----*/
				rightContainer:'',
				/*--end--*/
				labeldx: '已选',
				maxSelected: -1,
				autoSort: false,
				autoSortAvailable: false,
				search: false,
				caseSensitive: false,
				delay: 200,
				optGroupSearch: false,
				minSize: 6
			};

			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (options)
					$.extend(o, options);

				if (!data)
					el.data('multiselect2side', o);

				var	originalName = $(this).attr("name");
				if (originalName.indexOf('[') != -1)
					originalName = originalName.substring(0, originalName.indexOf('['));

				var	nameDx = originalName + "ms2side__dx";
				var	nameSx = originalName + "ms2side__sx";
				var size = $(this).attr("size");
				// SIZE MIN
				if (size < o.minSize) {
					$(this).attr("size", "" + o.minSize);
					size = o.minSize;
				}

				// UP AND DOWN
				var divUpDown =
						"<div class='ms2side__updown'>" +
							"<p class='SelSort' title='按顺序排列'>" + o.labelSort + "</p>" +
							"<p class='MoveTop' title='排在首位'>" + o.labelTop + "</p>" +
							"<p class='MoveUp' title='上移一位'>" + o.labelUp + "</p>" +
							"<p class='MoveDown' title='下移一位'>" + o.labelDown + "</p>" +
							"<p class='MoveBottom' title='排在底部'>" + o.labelBottom + "</p>" +
						"</div>";

				// INPUT TEXT FOR SEARCH OPTION
				var	leftSearch = false, rightSearch = false;
				// BOTH SEARCH AND OPTGROUP SEARCH
				if (o.search != false && o.optGroupSearch != false) {
					var ss = 
						/*--1.增加标题容器--
						//搜索框添加标记
						o.optGroupSearch + "<select class='small' ><option value=__null__> </option></select> " +
						o.search + "<input class='small' type='text' /><a href='#'> </a>";
						*/
						o.optGroupSearch + "<select class='small' ><option value=__null__>全部</option></select> " +
						o.search + "<input class='small searchInput' type='text' /><a href='#'> </a>";
						/*--1.end--*/

					if (o.selectedPosition == 'right')
						leftSearch = ss;
					else
						rightSearch = ss;
				}
				else if (o.search != false) {
					/*--1.增加标题容器--
					//搜索框添加标记
					var	ss = o.search + "<input type='text' /><a href='#'> </a>";
					*/
					var	ss = o.search + "<input class='searchInput' type='text' /><a href='#'> </a>";
					/*--1.end--*/

					if (o.selectedPosition == 'right')
						leftSearch = ss;
					else
						rightSearch = ss;
				}
				else if (o.optGroupSearch != false) {
					/*--1.增加标题容器--
					//搜索框添加标记
					var	ss = o.optGroupSearch + "<select><option value=__null__></option></select>";
					*/
					var	ss = o.optGroupSearch + "<select><option value=__null__>全部</option></select>";
					/*--1.end--*/

					if (o.selectedPosition == 'right')
						leftSearch = ss;
					else
						rightSearch = ss;
				}

				// CREATE NEW ELEMENT (AND HIDE IT) AFTER THE HIDDED ORGINAL SELECT
				var htmlToAdd = 
					"<div class='ms2side__div'>" +
							((o.selectedPosition != 'right' && o.moveOptions) ? divUpDown : "") +
						"<div class='ms2side__select'>" +
							/*1.增加标题容器--((o.labelsx || leftSearch != false) ? ("<div class='ms2side__header'>" + (leftSearch != false ? leftSearch : o.labelsx) + "</div>") : "")--*/(o.leftContainer?("<div class='ms2side__header'>" + o.leftContainer + "</div>"):((o.labelsx || leftSearch != false) ? ("<div class='ms2side__header'>" + (leftSearch != false ? leftSearch : o.labelsx) + "</div>") : ""))/*--end--*/ +
							"<select title='" + o.labelsx + "' name='" + nameSx + "' id='" + nameSx + "' size='" + size + "' multiple='multiple' ></select>" +
						"</div>" +
						"<div class='ms2side__options'>" +
							((o.selectedPosition == 'right')
							?
							("<p class='AddOne' title='添加选中'>&rsaquo;</p>" +
							"<p class='AddAll' title='添加全部'>&raquo;</p>" +
							"<p class='RemoveOne' title='移除选中'>&lsaquo;</p>" +
							"<p class='RemoveAll' title='移除全部'>&laquo;</p>")
							:
							("<p class='AddOne' title='添加选中'>&lsaquo;</p>" +
							"<p class='AddAll' title='添加全部'>&laquo;</p>" +
							"<p class='RemoveOne' title='移除选中'>&rsaquo;</p>" +
							"<p class='RemoveAll' title='移除全部'>&raquo;</p>")
							) +
						"</div>" +
						"<div class='ms2side__select'>" +
							/*1.增加标题容器--((o.labeldx || rightSearch != false) ? ("<div class='ms2side__header'>" + (rightSearch != false ? rightSearch : o.labeldx) + "</div>") : "")--*/(o.rightContainer?("<div class='ms2side__header'>" + o.rightContainer + "</div>"):((o.labeldx || rightSearch != false) ? ("<div class='ms2side__header'>" + (rightSearch != false ? rightSearch : o.labeldx) + "</div>") : ""))/*--end--*/ +
							"<select title='" + o.labeldx + "' name='" + nameDx + "' id='" + nameDx + "' size='" + size + "' multiple='multiple' ></select>" +
						"</div>" +
						((o.selectedPosition == 'right' && o.moveOptions) ? divUpDown : "") +
					"</div>";
				el.after(htmlToAdd).hide();

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");
				var	leftSel = (o.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
				var	rightSel = (o.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);
				// HEIGHT DIV
				var	heightDiv = $(".ms2side__select").eq(0).height();

				// SELECT optgroup
				var searchSelect = $();

				// SEARCH INPUT
				/*--1.增加标题容器--
				//搜索框添加标记
				var searchInput = $(this).next().find("input:text");
				*/
				var searchInput = $(this).next().find("input:text.searchInput");
				/*--1.end--*/
				var	removeFilter = searchInput.next().hide();
				var	toid = false;
				var searchV = false;


				// SELECT optgroup - ADD ALL OPTGROUP AS OPTION
				if (o.optGroupSearch != false) {
					var	lastOptGroupSearch = false;

					searchSelect = $(this).next().find("select").eq(0);

					el.children("optgroup").each(function() {
						if (searchSelect.find("[value='" + $(this).attr("label") + "']").size() == 0)
							searchSelect.append("<option value='" + $(this).attr("label") + "'>" + $(this).attr("label") + "</option>");
					});
					searchSelect.change(function() {
						var	sEl = $(this);

						if (sEl.val() != lastOptGroupSearch) {

							// IF EXIST SET SEARCH TEXT TO VOID
							if (searchInput.val() != "") {
								clearTimeout(toid);
								removeFilter.hide();
								searchInput.val("");//.trigger('keyup');
								searchV = "";
								// fto();
							}

							setTimeout(function() {
								if (sEl.val() == "__null__") {
									els = el.find("option:not(:selected)");
								}
								else
									els = el.find("optgroup[label='" + sEl.val() + "']").children("option:not(:selected)");

								// REMOVE ORIGINAL ELEMENTS AND ADD OPTION OF OPTGROUP SELECTED
								leftSel.find("option").remove();
								els.each(function() {
									leftSel.append($(this).clone());
								});
								lastOptGroupSearch = sEl.val();
								leftSel.trigger('change');
							}, 100);
						}
					});
				}


				// SEARCH FUNCTION
				var	fto = function() {
					var	els = leftSel.children();
					var	toSearch = el.find("option:not(:selected)");

					// RESET OptGroupSearch
					lastOptGroupSearch = "__null__";
					searchSelect.val("__null__");

					if (searchV == searchInput.val())
						return;

					searchInput
						.addClass("wait")
						.removeAttr("style");

					searchV = searchInput.val();

					// A LITTLE TIMEOUT TO VIEW WAIT CLASS ON INPUT ON IE
					setTimeout(function() {
						leftSel.children().remove();
						if (searchV == "") {
							toSearch.clone().appendTo(leftSel).removeAttr("selected");
							removeFilter.hide();
						}
						else {
							toSearch.each(function() {
								var	myText = $(this).text();

								if (o.caseSensitive)
									find = myText.indexOf(searchV);
								else
									find = myText.toUpperCase().indexOf(searchV.toUpperCase());

								if (find != -1)
									$(this).clone().appendTo(leftSel).removeAttr("selected");
							});

							if (leftSel.children().length == 0)
								searchInput.css({'border': '1px red solid'});

							removeFilter.show();
							leftSel.trigger('change');
						}
						leftSel.trigger('change');
						searchInput.removeClass("wait");
					}, 5);
				};


				// REMOVE FILTER ON SEARCH FUNCTION
				removeFilter.click(function() {
					clearTimeout(toid);
					searchInput.val("");
					fto();
					return false;
				});

				// ON CHANGE TEXT INPUT
				searchInput.keyup(function() {
					clearTimeout(toid);
					toid = setTimeout(fto, o.delay);
				});


				// CENTER MOVE OPTIONS AND UPDOWN OPTIONS
				$(this).next().find('.ms2side__options, .ms2side__updown').each(function(){
					var	top = ((heightDiv/2) - ($(this).height()/2));
					if (top > 0)
						$(this).css('padding-top',  top + 'px' );
				})

				// MOVE SELECTED OPTION TO RIGHT, NOT SELECTED TO LEFT
				$(this).find("option:selected").clone().appendTo(rightSel); // .removeAttr("selected");
				$(this).find("option:not(:selected)").clone().appendTo(leftSel);

				// SELECT FIRST LEFT ITEM AND DESELECT IN RIGHT (NOT IN IE6)
				if (!($.browser.msie && $.browser.version == '6.0')) {
					leftSel.find("option").eq(0).attr("selected", true);
					rightSel.children().removeAttr("selected");
				}

				// ON CHANGE SORT SELECTED OPTIONS
				var	nLastAutosort = 0;
				if (o.autoSort)
					allSel.change(function() {
						var	selectDx = rightSel.find("option");

						if (selectDx.length != nLastAutosort) {
							// SORT SELECTED ELEMENT
							selectDx.sort(internalSort);
							// FIRST REMOVE FROM ORIGINAL SELECT
							el.find("option:selected").remove();
							// AFTER ADD ON ORIGINAL AND RIGHT SELECT
							selectDx.each(function() {
								rightSel.append($(this).clone());
								$(this).appendTo(el).attr("selected", true);
								//el.append($(this).attr("selected", true));		HACK IE6
							});
							nLastAutosort = selectDx.length;
						}
					});

				// ON CHANGE SORT AVAILABLE OPTIONS (NOT NECESSARY IN ORIGINAL SELECT)
				var	nLastAutosortAvailable = 0;
				if (o.autoSortAvailable)
					allSel.change(function() {
						var	selectSx = leftSel.find("option");

						if (selectSx.length != nLastAutosortAvailable) {
							// SORT SELECTED ELEMENT
							selectSx.sort(internalSort);
							// REMOVE ORIGINAL ELEMENTS AND ADD SORTED
							leftSel.find("option").remove();
							selectSx.each(function() {
								leftSel.append($(this).clone());
							});
							nLastAutosortAvailable = selectSx.length;
						}
					});

				// ON CHANGE REFRESH ALL BUTTON STATUS
				allSel.change(function() {
					// HACK FOR IE6 (SHOW AND HIDE ORIGINAL SELECT)
					if ($.browser.msie && $.browser.version == '6.0')
						el.show().hide();
					var	div = $(this).parent().parent();
					var	selectSx = leftSel.children();
					var	selectDx = rightSel.children();
					var	selectedSx = leftSel.find("option:selected");
					var	selectedDx = rightSel.find("option:selected");

					if (selectedSx.size() == 0 ||
							(o.maxSelected >= 0 && (selectedSx.size() + selectDx.size()) > o.maxSelected))
						div.find(".AddOne").addClass('ms2side__hide');
					else
						div.find(".AddOne").removeClass('ms2side__hide');

					// FIRST HIDE ALL
					div.find(".RemoveOne, .MoveUp, .MoveDown, .MoveTop, .MoveBottom, .SelSort").addClass('ms2side__hide');
					if (selectDx.size() > 1)
						div.find(".SelSort").removeClass('ms2side__hide');
					if (selectedDx.size() > 0) {
						div.find(".RemoveOne").removeClass('ms2side__hide');
						// ALL SELECTED - NO MOVE
						if (selectedDx.size() < selectDx.size()) {	// FOR NOW (JOE) && selectedDx.size() == 1
							if (selectedDx.val() != selectDx.val())	// FIRST OPTION, NO UP AND TOP BUTTON
								div.find(".MoveUp, .MoveTop").removeClass('ms2side__hide');
							if (selectedDx.last().val() != selectDx.last().val())	// LAST OPTION, NO DOWN AND BOTTOM BUTTON
								div.find(".MoveDown, .MoveBottom").removeClass('ms2side__hide');
						}
					}

					if (selectSx.size() == 0 ||
							(o.maxSelected >= 0 && selectSx.size() >= o.maxSelected))
						div.find(".AddAll").addClass('ms2side__hide');
					else
						div.find(".AddAll").removeClass('ms2side__hide');

					if (selectDx.size() == 0)
						div.find(".RemoveAll").addClass('ms2side__hide');
					else
						div.find(".RemoveAll").removeClass('ms2side__hide');
				});

				// DOUBLE CLICK ON LEFT SELECT OPTION
				leftSel.dblclick(function () {
					$(this).find("option:selected").each(function(i, selected){

						if (o.maxSelected < 0 || rightSel.children().size() < o.maxSelected) {
							$(this).remove().appendTo(rightSel);
							/***4.BUG:双击不应在el源列表有移出动作**
							el.find("[value='" + $(selected).val() + "']").remove().appendTo(el).attr("selected", true);
							*/
							el.find("[value='" + $(selected).val() + "']").attr("selected", true);
							/***end**/
						}
					});
					$(this).trigger('change');
				});

				// DOUBLE CLICK ON RIGHT SELECT OPTION
				rightSel.dblclick(function () {
					$(this).find("option:selected").each(function(i, selected){
						$(this).remove().appendTo(leftSel);
						/***4.BUG:双击不应在el源列表有移出动作**
						el.find("[value='" + $(selected).val() + "']").removeAttr("selected").remove().appendTo(el);
						*/
						el.find("[value='" + $(selected).val() + "']").removeAttr("selected");
						/***end**/
					});
					$(this).trigger('change');

					// TRIGGER CHANGE AND VALUE NULL FORM OPTGROUP SEARCH (IF EXIST)
					searchSelect.val("__null__").trigger("change");
					// TRIGGER CLICK ON REMOVE FILTER (IF EXIST)
					removeFilter.click();
				});

				// CLICK ON OPTION
				$(this).next().find('.ms2side__options').children().click(function () {
					if (!$(this).hasClass("ms2side__hide")) {
						if ($(this).hasClass("AddOne")) {
							leftSel.find("option:selected").each(function(i, selected){
								$(this).remove().appendTo(rightSel);
								el.find("[value='" + $(selected).val() + "']").remove().appendTo(el).attr("selected", true);
							});
						}
						else if ($(this).hasClass("AddAll")) {	// ALL SELECTED
							// TEST IF HAVE A FILTER OR A SELECT OPTGROUP
							if (removeFilter.is(":visible") || (searchSelect.length > 0 && searchSelect.val() != "__null__"))
								leftSel.children().each(function(i, selected){
									$(this).remove().appendTo(rightSel);
									el.find("[value='" + $(selected).val() + "']").remove().appendTo(el).attr("selected", true);
								});
							else {
								leftSel.children().remove().appendTo(rightSel);
								el.find('option').attr("selected", true);
								// el.children().attr("selected", true); -- PROBLEM WITH OPTGROUP
							}
						}
						else if ($(this).hasClass("RemoveOne")) {
							rightSel.find("option:selected").each(function(i, selected){
								$(this).remove().appendTo(leftSel);
								el.find("[value='" + $(selected).val() + "']").remove().appendTo(el).removeAttr("selected");
							});
							// TRIGGER CLICK ON REMOVE FILTER (IF EXIST)
							removeFilter.click();
							// TRIGGER CHANGE AND VALUE NULL FORM OPTGROUP SEARCH (IF EXIST)
							searchSelect.val("__null__").trigger("change");
						}
						else if ($(this).hasClass("RemoveAll")) {	// ALL REMOVED
							rightSel.children().appendTo(leftSel);
							rightSel.children().remove();
							el.find('option').removeAttr("selected");
							//el.children().removeAttr("selected"); -- PROBLEM WITH OPTGROUP
							// TRIGGER CLICK ON REMOVE FILTER (IF EXIST)
							removeFilter.click();
							// TRIGGER CHANGE AND VALUE NULL FORM OPTGROUP SEARCH (IF EXIST)
							searchSelect.val("__null__").trigger("change");
						}
					}

					leftSel.trigger('change');
				});

				// CLICK ON UP - DOWN
				$(this).next().find('.ms2side__updown').children().click(function () {
					var	selectedDx = rightSel.find("option:selected");
					var	selectDx = rightSel.find("option");

					if (!$(this).hasClass("ms2side__hide")) {
						if ($(this).hasClass("SelSort")) {
							// SORT SELECTED ELEMENT
							selectDx.sort(internalSort);
							// FIRST REMOVE FROM ORIGINAL SELECT
							el.find("option:selected").remove();
							// AFTER ADD ON ORIGINAL AND RIGHT SELECT
							selectDx.each(function() {
								rightSel.append($(this).clone().attr("selected", true));
								el.append($(this).attr("selected", true));
							});
						}
						else if ($(this).hasClass("MoveUp")) {
							var	prev = selectedDx.first().prev();
							var	hPrev = el.find("[value='" + prev.val() + "']");

							selectedDx.each(function() {
								$(this).insertBefore(prev);
								el.find("[value='" + $(this).val() + "']").insertBefore(hPrev);	// HIDDEN SELECT
							});
						}
						else if ($(this).hasClass("MoveDown")) {
							var	next = selectedDx.last().next();
							var	hNext = el.find("[value='" + next.val() + "']");

							selectedDx.each(function() {
								$(this).insertAfter(next);
								el.find("[value='" + $(this).val() + "']").insertAfter(hNext);	// HIDDEN SELECT
							});
						}
						else if ($(this).hasClass("MoveTop")) {
							var	first = selectDx.first();
							var	hFirst = el.find("[value='" + first.val() + "']");

							selectedDx.each(function() {
								$(this).insertBefore(first);
								el.find("[value='" + $(this).val() + "']").insertBefore(hFirst);	// HIDDEN SELECT
							});
						}
						else if ($(this).hasClass("MoveBottom")) {
							var	last = selectDx.last();
							var	hLast = el.find("[value='" + last.val() + "']");

							selectedDx.each(function() {
								last = $(this).insertAfter(last);	// WITH last = SAME POSITION OF SELECTED OPTION AFTER MOVE
								hLast = el.find("[value='" + $(this).val() + "']").insertAfter(hLast);	// HIDDEN SELECT
							});
						}
					}

					leftSel.trigger('change');
				});

				// HOVER ON OPTION
				$(this).next().find('.ms2side__options, .ms2side__updown').children().hover(
					function () {
						$(this).addClass('ms2side_hover');
					},
					function () {
						$(this).removeClass('ms2side_hover');
					}
				);

				// UPDATE BUTTON ON START
				leftSel.trigger('change');
				// SHOW WHEN ALL READY
				$(this).next().show();
			});
		},
		destroy : function( ) {
			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;

				el.show().next().remove();
			});
		}/***2.insertOption方法，数据格式：[{name:'',value:'',selected:false,optgroup:false}]；addOption方法，数据格式：[{name:'a',children:[{name:'',value:'',selected:false}]}]**,		
		addOption : function(options) {
			var oAddOption = {
				name: false,
				value: false,
				selected: false
			};

			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;
				if (options)
					$.extend(oAddOption, options);

				var	strEl = "<option value='" + oAddOption.value + "' " + (oAddOption.selected ? "selected" : "") + " >" + oAddOption.name + "</option>";

				el.append(strEl);

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");
				var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
				var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

				if (oAddOption.selected)
					rightSel.append(strEl).trigger('change');
				else
					leftSel.append(strEl).trigger('change');
			});
		}*/,		
		insertOption : function(options) {
			var oAddOption = {
				id: false,
				text: false,
				name: false,
				value: false,
				selected: false,
				optgroup: false
			};

			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;

				//分组列表
				var searchSelect = el.next().find("select").eq(0);

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");
				var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
				var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

				//将ojbect -> array
				if (!(options instanceof Array)) {
					option = options;
					options = [];
					options.push(option);
				};
				
				var strEl = '';
				for(option in options){
					if (option)
						$.extend(oAddOption, options[option]);						

					if(oAddOption.optgroup){//有组名

						var hasOptgroup = el.find("[label='" + oAddOption.optgroup + "']");
						if(hasOptgroup.size() == 0){//不存在组名
							var newOption = "<option value='" + (oAddOption.value ? oAddOption.value : oAddOption.id) + "' " + (oAddOption.selected ? "selected" : "") + " >" + (oAddOption.name ? oAddOption.name : oAddOption.text) + "</option>";
							el.append($('<optgroup/>').attr('label',oAddOption.optgroup).append(newOption));		

							//组名列表添加组名
							if(searchSelect.length){
								searchSelect.append("<option value='" + oAddOption.optgroup + "'>" + oAddOption.optgroup + "</option>");
							}
						}else{//存在组名
							var newOption = "<option value='" + (oAddOption.value ? oAddOption.value : oAddOption.id) + "' " + (oAddOption.selected ? "selected" : "") + " >" + (oAddOption.name ? oAddOption.name : oAddOption.text) + "</option>";
							hasOptgroup.append(newOption);	
						}

					}else{//无分组
						strEl += "<option value='" + (oAddOption.value ? oAddOption.value : oAddOption.id) + "' " + (oAddOption.selected ? "selected" : "") + " >" + (oAddOption.name ? oAddOption.name : oAddOption.text) + "</option>";

					}
				};
				el.append(strEl);

				var cloneEl = el.clone();
				cloneEl.find("option:not(:selected)").remove().appendTo(leftSel);
				cloneEl.find("option").removeAttr("selected").appendTo(rightSel);
				//设置分组列表值
				searchSelect.val("__null__").trigger('change');
			});
		},
		addOption : function(options) {
			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;

				var selectAll = false;
				if((options instanceof Array) && ((options[0].id == 'all') || (options[0].value == 'all'))){
					selectAll = ( options[0].selected ? options[0].selected : false)
					options = options[0].children;
				}

				//分组列表
				var searchSelect = el.next().find("select").eq(0);

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");
				var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
				var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

				for(index in options){
					var strEl = '';
					var optgroupName = (options[index].name ? options[index].name : $.trim(options[index].text ? options[index].text : ''));

					var hasOptgroup = el.find("[label='" + optgroupName + "']");
					if(hasOptgroup.size() == 0){//不存在组名
						for(optionIndex in options[index].children){
							strEl += "<option value='" + (options[index].children[optionIndex].value ? options[index].children[optionIndex].value : options[index].children[optionIndex].id) + "' " + (options[index].children[optionIndex].selected ? "selected" : "") + " >" + (options[index].children[optionIndex].name ? options[index].children[optionIndex].name : options[index].children[optionIndex].text) + "</option>";
						}
						el.append($('<optgroup/>').attr('label',optgroupName).append(strEl));		

						//组名列表添加组名
						if(searchSelect.length){
							searchSelect.append("<option value='" + optgroupName + "'>" + optgroupName + "</option>");
						}
					}else{//存在组名
						for(optionIndex in options[index].children){
							strEl += "<option value='" + (options[index].children[optionIndex].value ? options[index].children[optionIndex].value : options[index].children[optionIndex].id) + "' " + (options[index].children[optionIndex].selected ? "selected" : "") + " >" + (options[index].children[optionIndex].name ? options[index].children[optionIndex].name : options[index].children[optionIndex].text) + "</option>";
						}
						hasOptgroup.append(strEl);	
					}
				};

				//清空已选项
				allSel.empty();

				if(selectAll){
					el.find('option').clone().removeAttr("selected").appendTo(rightSel);
				}else{
					el.find("option:not(:selected)").clone().appendTo(leftSel);
					el.find("option:selected").clone().removeAttr("selected").appendTo(rightSel);					
				}
				//设置分组列表值
				searchSelect.val("__null__").trigger('change');
			})
		}/***end2**//***3.新增清空方法clearOption**/,
		clearOption : function(){
			return this.each(function(){
				var el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");

				//empty all select
				el.empty();
				allSel.empty();
				//假如select有三个
				if(el.next().find("select").length >= 3){
					var searchSelect = el.next().find("select").eq(0);
					searchSelect.empty().append('<option value=__null__>全部</option></select>');
				}
			})
		}/***end3***//***5.新增方法setVal，传入ID或value，如：["a","b","c"]**/,
		setVal : function(values){

			return this.each(function () {
				var	el = $(this);
				var data = el.data('multiselect2side');

				if (!data)
					return;

				// ELEMENTS
				var allSel = el.next().children(".ms2side__select").children("select");
				var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
				var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);
				var searchSelect = el.next().find("select").eq(0);

				//将ojbect -> array
				if (!(values instanceof Array)) {
					value = values;
					values = [];
					values.push(value);
				};

				//清空已选项
				var allOptions = el.find(':selected');
				allOptions.removeAttr('selected');
				allSel.empty();

				if((values.length == 1) && values[0] == 'all'){
					//复制选项到右边
					var selectOption = el.find('option');
					rightSel.append(selectOption.clone()).trigger('change');	
					//给源select 的option选项设置选中属性
					selectOption.attr("selected", true);
				}else{
					for(value in values){
						var selectOption = el.find("[value='" + values[value] + "']");

						if(selectOption.size()){
							//复制选项到右边
							rightSel.append(selectOption.clone()).trigger('change');	
							//给源select 的option选项设置选中属性
							selectOption.attr("selected", true);
						}
					}
					leftSel.append(el.find("option:not(:selected)").clone()).trigger('change');		
				}
				//设置分组列表值
				searchSelect.val("__null__").trigger('change');
			})
		}
		/***end5***//***6.新增方法getVal/getName，输出 ('all'或数组 如：["a","b","c"])/('全部'或字符串 如：'a,b,c') ; val/name 只输出数组**/,
		getVal : function(){
			var	el = $(this);
			var data = el.data('multiselect2side');

			if (!data)
				return;

			// ELEMENTS
			var allSel = el.next().children(".ms2side__select").children("select");
			var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
			var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

			//if($(this).find("option").length && !leftSel.find("option").length){
				//return 'all';
			//}else{
				var val = [];
				$.each(rightSel.find("option"),function(i,j){
					val.push(j.value);
				})
				return val;
			//}			
		},
		val : function(){

			var	el = $(this);
			var data = el.data('multiselect2side');

			if (!data)
				return;

			// ELEMENTS
			var allSel = el.next().children(".ms2side__select").children("select");
			var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
			var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);
			
			var val = [];
			$.each(rightSel.find("option"),function(i,j){
				val.push(j.value);
			})
			return val;	
		},
		getName : function(){

			var	el = $(this);
			var data = el.data('multiselect2side');

			if (!data)
				return;

			// ELEMENTS
			var allSel = el.next().children(".ms2side__select").children("select");
			var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
			var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

			if($(this).find("option").length && !leftSel.find("option").length){
				return '全部';
			}else{
				var text = '';
				$.each(rightSel.find("option"),function(i,j){
					text += ($(j).text() + '，');
				})
				text = text.slice(0,text.length-1);
				return text;
			}			
		},
		name : function(){

			var	el = $(this);
			var data = el.data('multiselect2side');

			if (!data)
				return;

			// ELEMENTS
			var allSel = el.next().children(".ms2side__select").children("select");
			var	leftSel = (data.selectedPosition == 'right') ? allSel.eq(0) : allSel.eq(1);
			var	rightSel = (data.selectedPosition == 'right') ? allSel.eq(1) : allSel.eq(0);

			var text = '';
			$.each(rightSel.find("option"),function(i,j){
				text += ($(j).text() + '，');
			})
			text = text.slice(0,text.length-1);
			return text;
		}
		/***end6***/
	};

  $.fn.multiselect2side = function( method ) {
    if ( methods[method] ) {
      return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
    } else if ( typeof method === 'object' || ! method ) {
      return methods.init.apply( this, arguments );
    } else {
      $.error( 'Method ' +  method + ' does not exist on jQuery.multiselect2side' );
    }    
  };

})(jQuery);