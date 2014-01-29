var ws=window.ws;
$(document).ready(function() {

	$(".slider").slider({
		step: 5,
		orientation: "vertical",
		value: 0,
		min: 0,
		max: 255,
		slide: function( evt, ui ) {
//		"values", 0, 255) ;
			ws.send(JSON.stringify({'mqtt':{'topic':'plantes/light','payload':ui.value}}));
		}
	});

//	$( ".slider" ).on( "slidechange", function( event, ui ) {
//		ws.send(JSON.stringify({'mqtt':{'topic':'plantes/light','payload':200}}));	
//	});
});


