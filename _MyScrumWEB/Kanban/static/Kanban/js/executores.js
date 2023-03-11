
/* Função que conta quanto campos de executores estão ocultos */
function contar(){
	return document.querySelectorAll('div[hidden=hidden]').length;
}

/* Função que adiciona executores */
$("#add-executor").click(function(){
	if(contar() >= 1){
		comboALiberar = (10 - contar()) + 1;
		$("#executor"+comboALiberar+"").attr("hidden",false);
	}else{alert("Limite de executores atingido")}
});

$("#remove-executor2").click(function(){
	var executor = document.getElementById("id_executor2");
	executor.selectedIndex = 0;
	
	var porcento = document.getElementById("id_porcento2");
	porcento.value = '';

	$("#executor2").attr("hidden", true);

})

$("#remove-executor3").click(function(){
	var executor = document.getElementById("id_executor3");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento3");
	porcento.value = '';
	
	$("#executor3").attr("hidden", true);
});

$("#remove-executor4").click(function(){
	var executor = document.getElementById("id_executor4");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento4");
	porcento.value = '';
	
	$("#executor4").attr("hidden", true);
});

$("#remove-executor5").click(function(){
	var executor = document.getElementById("id_executor5");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento5");
	porcento.value = '';
	
	$("#executor5").attr("hidden", true);
});

$("#remove-executor6").click(function(){
	var executor = document.getElementById("id_executor6");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento6");
	porcento.value = '';
	
	$("#executor6").attr("hidden", true);
});

$("#remove-executor7").click(function(){
	var executor = document.getElementById("id_executor7");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento7");
	porcento.value = '';
	
	$("#executor7").attr("hidden", true);
});

$("#remove-executor8").click(function(){
	var executor = document.getElementById("id_executor8");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento8");
	porcento.value = '';
	
	$("#executor8").attr("hidden", true);
});

$("#remove-executor9").click(function(){
	var executor = document.getElementById("id_executor9");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento9");
	porcento.value = '';
	
	$("#executor9").attr("hidden", true);
});

$("#remove-executor10").click(function(){
	var executor = document.getElementById("id_executor10");
	executor.selectedIndex = 0;

	var porcento = document.getElementById("id_porcento10");
	porcento.value = '';
	
	$("#executor10").attr("hidden", true);
});
