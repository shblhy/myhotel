define(["./functions"], function(functions) {
//define(["/static/base/js/functions.js"], function(functions) {
	return {
		Test:function (){
			this.a =1;
			console.log("aaaa");
			functions.base.alertme();
		}
	}
});