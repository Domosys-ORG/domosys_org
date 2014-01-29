$(document).ready(function() {
//if (!String.prototype.trim) {
//    String.prototype.trim = function() { return this.replace(/^\s+|\s+$/, ''); };
//}
	var alertbox = $("#alert");
	alertbox.hide();
	var html = $("#alert-body").html();
 	if ($.trim(html) != "") {
		alertbox.show();
		alertbox.fadeIn("fast");
		setTimeout( (function(){alertbox.fadeOut(1000)}), 2000);
	}
window.alert = function (message) {
	$("#alert-body").html(message);
	alertbox.show();
	alertbox.fadeIn("fast");
	setTimeout( (function(){alertbox.fadeOut(1000)}), 2000);	
	setTimeout( (function(){$("#alert-body").html("")}), 5000);
}
});


