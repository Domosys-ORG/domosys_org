var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	}
});

$("#config.accordion").find(".config").each(function() {
	$(this).children().each(function() {
//		console.log($(this).attr('id') + ' clicked');
		$(this).bind('click',function() {
			var caption_id = $(this).attr('id')
			var caption_type = $(this).attr('class')
			var configurl = "config/"+caption_type+"/"+caption_id
			console.log(configurl);
			$.ajax({
				type: "GET",
				url: configurl,
				data: {
					'method': $(this).attr('class'),
				},
				success: function(data) {
//					$("#config-container").append(data);
					$("#config.form").html(data);
					$('#post-config.bouton').click( function(e) {
						e.preventDefault();
						var strform = $('#form-config').serialize();
//						console.log("strform: "+strform);
						$.post( 
							configurl, 
							strform,
							function(data) {
								$("#config-container").html(data);
								$( "#config.accordion" ).accordion();
//								console.log(data);
							});
					});
					$('#delete-config.bouton').click( function(e) {
						e.preventDefault();
						var strform = $('#form-config').serialize();
						strform = strform + "&action=delete";
						console.log("strform: "+strform);
						$.post( 
							configurl, 
							strform,
							function(data) {
								$("#config-container").html(data);
								$( "#config.accordion" ).accordion();
								console.log("retrieve from: '#"+caption_id+"."+caption_type+"'");
							});
					});
				}
			});
		});
	});
});

