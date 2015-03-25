/* Default class modification */
$.extend( $.fn.dataTableExt.oStdClasses, {
	"sWrapper": "dataTables_wrapper form-inline"
} );

/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
	return {
		"iStart":         oSettings._iDisplayStart,
		"iEnd":           oSettings.fnDisplayEnd(),
		"iLength":        oSettings._iDisplayLength,
		"iTotal":         oSettings.fnRecordsTotal(),
		"iFilteredTotal": oSettings.fnRecordsDisplay(),
		"iPage":          oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
		"iTotalPages":    oSettings._iDisplayLength === -1 ?
			0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
	};
};

/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
	"bootstrap": {
		"fnInit": function( oSettings, nPaging, fnDraw ) {
			var oLang = oSettings.oLanguage.oPaginate;
			var fnClickHandler = function ( e ) {
				e.preventDefault();
				if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
					fnDraw( oSettings );
				}
			};

			$(nPaging).addClass('pagination').append(
				'<ul>'+
					'<li class="first disabled"><a href="#">'+oLang.sFirst+'</a></li>'+
					'<li class="prev disabled"><a href="#">'+oLang.sPrevious+'</a></li>'+
					'<li class="next disabled"><a href="#">'+oLang.sNext+'</a></li>'+
					'<li class="last disabled"><a href="#">'+oLang.sLast+' </a></li>'+
				'</ul>'
			);
			var els = $('a', nPaging);
			$(els[0]).bind( 'click.DT', { action: "first" }, fnClickHandler );
			$(els[1]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
			$(els[2]).bind( 'click.DT', { action: "next" }, fnClickHandler );
			$(els[3]).bind( 'click.DT', { action: "last" }, fnClickHandler );
		},

		"fnUpdate": function ( oSettings, fnDraw ) {
			var iListLength = 5;
			var oPaging = oSettings.oInstance.fnPagingInfo();
			var an = oSettings.aanFeatures.p;
			var i, ien, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

			if ( oPaging.iTotalPages < iListLength) {
				iStart = 1;
				iEnd = oPaging.iTotalPages;
			}
			else if ( oPaging.iPage <= iHalf ) {
				iStart = 1;
				iEnd = iListLength;
			} else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
				iStart = oPaging.iTotalPages - iListLength + 1;
				iEnd = oPaging.iTotalPages;
			} else {
				iStart = oPaging.iPage - iHalf + 1;
				iEnd = iStart + iListLength - 1;
			}

			for ( i=0, ien=an.length ; i<ien ; i++ ) {
				// 移除数字页码
				$('li:gt(1)', an[i]).filter(':not(:last)').filter(':not(:last)').remove();
				// 首页
				var $first = $('li:first', an[i]);
				// 上一页
				var $prev = $('li:eq(1)', an[i]);
				// 下一页
				var $next = $('li', an[i]).filter(':not(:last)').filter(':last');
				// 尾页
				var $last = $('li:last', an[i]);

				// Add the new list items and their event handlers
				for ( j=iStart ; j<=iEnd ; j++ ) {
					sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
					$('<li '+sClass+'><a href="#">'+j+'</a></li>')
						.insertBefore( $next[0] )
						.bind('click', function (e) {
							e.preventDefault();
							oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
							fnDraw( oSettings );
						} );
				}

				// 翻页启用/禁用状态
				if ( oPaging.iPage === 0 ) {
					$first.addClass('disabled');
					$prev.addClass('disabled');
				} else {
					$first.removeClass('disabled');
					$prev.removeClass('disabled');
				}

				if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
					$last.addClass('disabled');
					$next.addClass('disabled');
				} else {
					$last.removeClass('disabled');
					$next.removeClass('disabled');
				}
			}
		}
	}
} );


/*
 * TableTools Bootstrap compatibility
 * Required TableTools 2.1+
 */
if ( $.fn.DataTable.TableTools ) {
	// Set the classes that TableTools uses to something suitable for Bootstrap
	$.extend( true, $.fn.DataTable.TableTools.classes, {
		"container": "DTTT btn-group",
		"buttons": {
			"normal": "btn",
			"disabled": "disabled"
		},
		"collection": {
			"container": "DTTT_dropdown dropdown-menu",
			"buttons": {
				"normal": "",
				"disabled": "disabled"
			}
		},
		"print": {
			"info": "DTTT_print_info modal"
		},
		"select": {
			"row": "active"
		}
	} );

	// Have the collection use a bootstrap compatible dropdown
	$.extend( true, $.fn.DataTable.TableTools.DEFAULTS.oTags, {
		"collection": {
			"container": "ul",
			"button": "li",
			"liner": "a"
		}
	} );
}
/*全局参数设定*/
$.extend(true, $.fn.dataTable.defaults, {
	"fnInitComplete":function(oSettings){//初始完
		var oTable = oSettings.oInstance;
		//鼠标滑过高亮
		oTable.on('mouseenter','td', function() {
	        var iCol = $('td', this.parentNode).addClass( 'highlighted' ).index(this);
	        $('td:nth-child('+(iCol+1)+')', oTable.find('tr')).addClass( 'highlighted' );
	    }).on('mouseleave','td', function() {
	        oTable.find('td.highlighted').removeClass('highlighted');
	    });
	    /*需调整，不能与columnFilter共用
	    //显示/隐藏列
	    $('<span>显示隐藏第一列</span>').click(function(){
		    var bVis = oTable.fnSettings().aoColumns[1].bVisible;
	   		oTable.fnSetColumnVis( 1, bVis ? false : true );	    	
	    }).insertBefore(oTable);
		*/
	},
	"sDom": "<''<''b><''f>> t <'tableFooter'<''l><''pi>>",//布局<div class=""><div class=""></div><div class="">筛选</div></div>表格<div class=""><div class="">页数</div><div class="">分页/信息</div></div>

	/***Feature enablement***/
    "bPaginate": true, //开启-分页
    "bLengthChange": true, //开启-分页菜单
    "bFilter": true, //开启-过滤
    "bSort": true, //开启-排序
    "bInfo": true, //开启-信息
    "bAutoWidth": true, //开启-自适应宽度
    
	"sServerMethod":"post",//请求方式
	"sPaginationType": "bootstrap",//详细分页组，可以支持直接跳转到某页

	"bProcessing": false//显示加载中
 });