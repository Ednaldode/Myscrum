
/* Função que conta quanto campos de executores estão ocultos */
function contar(){
	return document.querySelectorAll('div[hidden=hidden]').length;
}

$("#add-executor").click(function(){
	if(contar() >= 1){
		comboALiberar = (10 - contar()) + 1;
		$("#executor"+comboALiberar+"").attr("hidden",false);
	}else{alert("Limite de executores atingido")}
});

$("#remove-executor2").click(function(){
	$("#executor2").attr("hidden", true);
	$("#select2-id_executor2-container").attr("title", "---------")
	document.getElementById('select2-id_executor2-container').innerHTML="---------"
})

$("#remove-executor3").click(function(){
	$("#executor3").attr("hidden", true);
	$("#select2-id_executor3-container").attr("title", "---------")
	document.getElementById('select2-id_executor3-container').innerHTML="---------"
});

$("#remove-executor4").click(function(){
	$("#executor4").attr("hidden", true);
	$("#select2-id_executor4-container").attr("title", "---------")
	document.getElementById('select2-id_executor4-container').innerHTML="---------"
});

$("#remove-executor5").click(function(){
	$("#executor5").attr("hidden", true);
	$("#select2-id_executor5-container").attr("title", "---------")
	document.getElementById('select2-id_executor5-container').innerHTML="---------"
});

$("#remove-executor6").click(function(){
	$("#executor6").attr("hidden", true);
	$("#select2-id_executor6-container").attr("title", "---------")
	document.getElementById('select2-id_executor6-container').innerHTML="---------"
});

$("#remove-executor7").click(function(){
	$("#executor7").attr("hidden", true);
	$("#select2-id_executor7-container").attr("title", "---------")
	document.getElementById('select2-id_executor7-container').innerHTML="---------"
});

$("#remove-executor8").click(function(){
	$("#executor8").attr("hidden", true);
	$("#select2-id_executor8-container").attr("title", "---------")
	document.getElementById('select2-id_executor8-container').innerHTML="---------"
});

$("#remove-executor9").click(function(){
	$("#executor9").attr("hidden", true);
	$("#select2-id_executor9-container").attr("title", "---------")
	document.getElementById('select2-id_executor9-container').innerHTML="---------"
});

$("#remove-executor10").click(function(){
	$("#executor10").attr("hidden", true);
	$("#select2-id_executor10-container").attr("title", "---------")
	document.getElementById('select2-id_executor10-container').innerHTML="---------"
});
