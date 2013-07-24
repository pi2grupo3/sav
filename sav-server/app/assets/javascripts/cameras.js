
$(document).ready(function(){
	$("#go-left").live("click", function(){
		
		var current_position = $(".badge-success").text()-1;
		$(".badge").each(function(){
					
			if($(this).text() == current_position){
				$(this).addClass(".badge-success");
			}		
		});		
	});
});
