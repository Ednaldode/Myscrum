
/* Função que conta quanto campos de executores estão ocultos */
function contar(){
	return document.querySelectorAll('div[hidden=hidden]').length;
}

/* Função que exibe campos de executores que estiverem selecionado */
$(document).ready(function() {
	for (var i = 1; i < 10; i++) {
		executor = 'id_executor' + i
		select = document.getElementById(executor);
		if(select.selectedIndex != 0){
			executor = "#executor" + i;
			$(executor).removeAttr("hidden");
		}
	 }
});

/* Função que adiciona executores */
$("#add-executor").click(function(){
	if(contar() >= 1){
		comboALiberar = (10 - contar()) + 1;
		executor = "#executor" + comboALiberar
		$(executor).removeAttr("hidden");
	} else {
		alert("Limite de executores atingido")}
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

$(function(){
	// Traz imagens dos executores na retrospectiva
	let executor = ($("#id_executor1  option:selected").text() + "," + $("#id_executor2  option:selected").text() + "," + $("#id_executor3  option:selected").text() + "," + $("#id_executor4  option:selected").text() + "," + $("#id_executor5  option:selected").text() + "," + $("#id_executor6  option:selected").text() + "," + $("#id_executor7  option:selected").text() + "," + $("#id_executor8  option:selected").text() + "," + $("#id_executor9  option:selected").text() + "," + $("#id_executor10  option:selected").text()).split(",");

	// Verifica se há 1 ou 2 executores na tarefa e altera imagens dos executores
	for (let i = 0; i < executor.length; i++){
	  if(executor[i] != "---------"){
		if (i <= 10){
		  $("#imagensExecutores").html($("#imagensExecutores").html() + ' <span class="col-xs p-icone executor mr-1" title="Executor: ' + executor[i] +'"><img id="imgExecutor' + i + '" class="rounded-circle" style="height:45px;width:45px;"></span>');
		  $("#imgExecutor" + i).attr("src", "../../media/usuarios/" + executor[i] + "/perfil/" + executor[i] + ".png").on("error", function(){
			$("#imgExecutor" + i).attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
		  });
		}
	  }
	}

	// Altera imagens da autoridade e responsável
	let pessoaResponsavel = $("#id_responsavel  option:selected").text();
	$("#imgResponsavel").attr("src", "../../media/usuarios/" + pessoaResponsavel + "/perfil/" + pessoaResponsavel + ".png").on("error", function(){
	  $("#imgResponsavel").attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
	});
	$("#rResponsavel").prop('title', 'Responsável: ' + pessoaResponsavel);
	let pessoaAutoridade = $("#id_autoridade  option:selected").text();
	$("#imgAutoridade").attr("src", "../../media/usuarios/" + pessoaAutoridade + "/perfil/" + pessoaAutoridade + ".png").on("error", function(){
	  $("#imgAutoridade").attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
	});
	$("#rAutoridade").prop('title', 'Autoridade: ' + pessoaAutoridade);
  });
