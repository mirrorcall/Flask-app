$(function(){
	$('#btnSignIn').click(function(){
		
		$.ajax({
			url: '/signInUser',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				window.location.replace('/');
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
