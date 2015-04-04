var require = {
	waitSeconds : 60,
	baseUrl : '/static/base/js/',
	paths : {
		/***javascript-ext***/
		"javascriptExt" : '../com/javascript-ext',
		"table" : '../js/table',
		/***bootstrap.js***/
		"bootstrap" : '../com/bootstrap-modified',		
		"form": '../com/jquery.form',
		"functions": 'functions',		
		//datatables
		"dataTable_src" : '../com/datatables/jquery.dataTables',
		"colVis" : '../com/datatables/ColVis',
		"dataTable" : '../com/datatables/FixedHeader',
		"fileupload" : '../com/fileupload/jquery.fileupload.min',
		"tipped_plugin" : '../com/tipped/tipped',
		//"address" : '../com/address/jquery.address-1.5.min',
		"jquery.ui.widget" : '../com/fileupload/jquery.ui.widget.min',
		"excanvas" : '../com/tipped/excanvas.min',
		"spinners" : '../com/tipped/spinners.min',
		//"dataTable", "functions", "fileupload", "tipped_plugin", "bootstrap", "address"
	},
	shim : {
		"form": 	{
			deps : ['jquery']
		},
		'spinners' : {
			deps : ['excanvas']
		},
		'tipped_plugin' : {
			deps : ['spinners']
		},
		//
		'dataTable' : {
			deps : ['colVis']
		},
		//
		'colVis' : {
			deps : ['dataTable_src']
		},
	},
	callback : function() {
		//回调
	}
}