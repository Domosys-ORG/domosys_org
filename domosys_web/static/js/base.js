var ws=window.ws;
$(document).tooltip;
$(document).ready(function() {
$(function() {
		
	$( "#navbar.accordion" ).accordion();

	var navbar = $("#navbar");
	navbar.hide();
	$("#navshow").show();
	$("#navhide").click(function() {
		$(navbar).animate({width: 0}, 200, function() {
			$(navbar).hide();
			$("#navshow").show();
		});
	
	});
	$("#navshow").click(function() {
		$(navbar).show().animate({width: 200}, 200);
		$("#navshow").hide();
	});

	var footmenu = $("#footer-menu");
	$("#footshow").hide();
	$("#foothide").click(function() {
		$(footmenu).animate({height: 0}, 200, function() {
			$(footmenu).hide();
			$("#footshow").show();
		});
	
	});
	$("#footshow").click(function() {
		$(footmenu).show().animate({height: 184}, 200);
		$("#footshow").hide();
	});

	$( "#tabs" ).tabs();

	$(".mqtt-widget.light.slide").append('<span class="mqtt-button light"></span><div class="mqtt-caption slider" style="display:none;"></div>');
	$(".mqtt-widget").hover(
		function(){
			$(this).children(".mqtt-caption").show();
			$(this).css('z-index', 1000);
//			var widget_left = $(this).position().left;
//			var caption_width = $(this).children(".mqtt-caption").width();
//			var button_width = $(this).children(".mqtt-button").width();
//			console.log('widget_left: ' + widget_left + ' caption_width: ' + caption_width + ' button_width: ' + button_width);
//			if (caption_width > button_width) {
//				var new_left = widget_left - (caption_width / 2 - button_width/2) | 0;
//				console.log(new_left);
//				$(this).css('left', new_left)
//			}
		},function() {
			$(this).children(".mqtt-caption").hide();
			$(this).css('z-index', 100);
//			var widget_left = $(this).position().left;
//			var caption_width = $(this).children(".mqtt-caption").width();
//			var button_width = $(this).children(".mqtt-button").width();
//			console.log('widget_left: ' + widget_left + ' caption_width: ' + caption_width + ' button_width: ' + button_width);
//			if (caption_width > button_width) {
//				var new_left = widget_left + (caption_width / 2 - button_width/2) | 0;
//				console.log(new_left);
//				$(this).css('left', new_left)
//			}
		});
	$(".mqtt-button.light").button( {
		icons: {
			primary:"ui-icon-lightbulb", 
//			secondary:"ui-icon ui-icon-triangle-1-s"
		},
	});
	$(".slider").slider({
		range: 'min',
		step: 5,
		orientation: "vertical",
		value: 0,
		min: 0,
		max: 255,
		slide: function( evt, ui ) {
			console.log($(this).parent().attr('id').replace('-','/'));
			ws.send(JSON.stringify({'mqtt':{'topic':$(this).parent().attr('id').replace('-','/'),'payload':ui.value}}));
		}});
	
	$(".mqtt-widget.vmc").append('<span class="mqtt-button vmc"></span>');
	$(".mqtt-widget.vmc").append('<div class="mqtt-caption offonhigh" style="display:none;"></div>');
	$(".mqtt-caption.offonhigh").append('<input type="radio" id="off" name="offonhigh"><label for="off">OFF</label>');
	$(".mqtt-caption.offonhigh").append('<input type="radio" id="on" name="offonhigh"><label for="on">ON</label>');
	$(".mqtt-caption.offonhigh").append('<input type="radio" id="high" name="offonhigh"><label for="high">HIGH</label>');
	$(".mqtt-caption.offonhigh").buttonset();
	$(".mqtt-button.vmc").button( {
		icons: {
			primary:"ui-icon-gear", 
//			secondary:"ui-icon ui-icon-triangle-1-s"
		}});
	$(".mqtt-caption.offonhigh :radio").click(function() {
		ws.send(JSON.stringify({'mqtt':{'topic':$(this).parent().parent().attr('id').replace('-','/'),'payload':$(this).attr('id')}}));
//		console.log($(this).parent().parent().attr('id').replace('-','/')+':'+$(this).attr('id'));
	});
	$(".mqtt-button").each(function() {
		$(this).attr('title', $(this).parent().attr('id').replace('-','/'));
		});
//	 style="display:none;"
	});
	console.log("caption_width: " + $(".mqtt-widget.vmc").find(".mqtt-caption").width());

	$("#general.container").find("form").each(function(){
		var frm = $(this);
		frm.submit(function () {
			$.ajax({
				type: frm.attr('method'),
				url: frm.attr('action'),
				data: frm.serialize(),
				success: function (data) {
//					$("#SOME-DIV").html(data);
					logConsole('logs', data);
				},
				error: function(data) {
					logConsole('logs', "Something bad in POST request");
//					$("#MESSAGE-DIV").html("Something went wrong!");
				}
			});
			return false;
		});
	});
});

