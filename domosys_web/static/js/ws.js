$(document).ready(function(){
//	function strencode( data ) {
//		return unescape( encodeURIComponent( JSON.stringify( data ) ) );
//	}
//	function strdecode( data ) {
//		console.log('strdecode:' + data);
//		return JSON.parse( decodeURIComponent( escape ( data ) ) );
//	}

function start_ws(){
	window.ws = new WebSocket("ws://green:8080/ws");
	ws=window.ws;
	ws.onopen = function(evt) {
		$('#socket-button').addClass("on");
		$('#socket-button').removeClass("off");
		alert("Websocket : connection établie", "error");
		$('div#socket.console-body').children().remove();
	}
	ws.onclose = function(evt) {
		$('#socket-button').addClass("off");
		$('#socket-button').removeClass("on");
		$('#socket-button').addClass("error");
		setTimeout( (function(){$('#socket-button').removeClass("error");}), 1000);
		alert("Websocket : Connection indisponible", "error");
		console.log("Client Disconnected");
	}
	ws.onmessage = function(evt) {
		logConsole('socket', evt.data);
		try {
			json = $.parseJSON(evt.data);
			fkey = Object.keys(json)[0];
			logConsole(fkey, JSON.stringify(json[fkey]));
			if (fkey == 'mqtt') {
				var mqtt_widget = $('#'+json['mqtt']['topic'].split('/').slice(1).join('-'));
//				console.log("mqtt_widget: "+$(mqtt_widget).attr('class'));
				var mqtt_caption = $(mqtt_widget).find(".mqtt-caption");
//				console.log("mqtt_caption: "+$(mqtt_caption).attr('class'));
				if ($(mqtt_caption).hasClass("ui-buttonset")) {
					var radiobut = $(mqtt_caption).find('#'+json['mqtt']['payload']);
//					console.log('radiobut.id='+$(radiobut).attr('id'));
					if($(radiobut).attr('checked')!='checked'){
						$(mqtt_caption).show();
						logConsole('logs', "radiobut: "+$(radiobut).attr('id')+" clicked");
						console.log('radiobut#'+$(radiobut).attr('id'));
						$(radiobut).click();
						setTimeout( (function(){$(mqtt_caption).hide();}), 2000);
					}
					console.log("radiobut: "+$(radiobut).attr('checked'));
				} else if ($(mqtt_caption).hasClass("slider")) {
//					console.log("slider: "+$(mqtt_caption).attr('class'));
					$(mqtt_caption).show();
					logConsole('logs',$(mqtt_widget).attr('id') + ": slider set value: " + parseInt(json['mqtt']['payload']));
					$(mqtt_caption).slider( "option", "value", json['mqtt']['payload']);
					setTimeout( (function(){$(mqtt_caption).hide();}), 20000);
				}
			}
		} catch(e) {
			alert(evt.data);
		}
			
//		alert('Messaged ' + evt.data);
//		console.log(evt.data);//JSON.parse(evt.data));
	}
}
// Initial Websocket Start
if(!window.ws){
	start_ws();
}
function logConsole(console_id, text) {
	$("<div />").text(text).appendTo('div#'+console_id+'.console-body');
	tailScroll('div#'+console_id+'.console-body');
}
function tailScroll(id, max_lines=100) {
	var height = $(id).get(0).scrollHeight;
	$(id).animate({scrollTop: height }, 10);
	if ($(id).children().length > max_lines) {
		$(id).children("div").eq(0).remove();
	}
//	console.log(id+$(id).children().length);
}
$('#socket-button').click( function() {
	if(!window.ws){
		start_ws();
	}else{
		alert('Déjà connecté');
	}
});
$("a#socket.footer.tab.on").click(function(){
//	ws.send("socket test "+$('div#socket.console-body').children().length);
	ws.send(JSON.stringify({'redis':{'key':'test','value':'100'}}));
});
var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	}
});
$(document).ajaxStart(function () {
    $('body').addClass('wait');
}).ajaxComplete(function () {
    $('body').removeClass('wait');
});

$("#home.header-button").click(function(){
	if ($("#general.container").children("#config-container").length) {
		$("#config-container").hide();
		$("#home.container").show();
		$("#home.header-button").addClass('page-active');
		$("#config.header-button").removeClass('page-active');
	}
});
$("#config.header-button").click(function(){
	if ($("#general.container").children("#config-container").length) {
		$("#config-container").show();
		$("#home.container").hide();
		$("#config.header-button").addClass('page-active');
		$("#home.header-button").removeClass('page-active');
	}else{
		$.ajax({
			type: "GET",
			url: "/config/",
			data: {
				'method': 'init',
			},
			success: function(data) {
				$("#general.container").append(data);
				$("#home.container").hide();
				$("#config-container").show();
				$( "#config.accordion" ).accordion();
//				$.getScript('static/js/config.js');
			}
		});
	}
	});

}); // document.ready

