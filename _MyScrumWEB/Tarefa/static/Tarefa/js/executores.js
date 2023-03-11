
/* Função que conta quanto campos de executores estão ocultos */
function contar(){
	return document.querySelectorAll('div[hidden=hidden]').length;
}

/* Função que exibe campos de executores que estiverem selecionado */
$(document).ready(function() {
	for (var i = 2; i < 10; i++) {
		executor = 'id_executor' + i
		select = document.getElementById(executor);
		if(select.selectedIndex != 0){
			executor = "#executor" + i;
			$(executor).removeAttr("hidden");
		}
	 }
});

$(function(){
	// Traz imagens dos executores na retrospectiva
	let executor = ($("#id_executor1  option:selected").text() + "," + $("#id_executor2  option:selected").text() + "," + $("#id_executor3  option:selected").text() + "," + $("#id_executor4  option:selected").text() + "," + $("#id_executor5  option:selected").text() + "," + $("#id_executor6  option:selected").text() + "," + $("#id_executor7  option:selected").text() + "," + $("#id_executor8  option:selected").text() + "," + $("#id_executor9  option:selected").text() + "," + $("#id_executor10  option:selected").text()).split(",");
	let executores = 0;
	// Verifica se há 1 ou 2 executores na tarefa e altera imagens dos executores
	for (let i = 0; i < executor.length; i++){
	  if(executor[i] != "---------"){
		  executores += 1;
		if (i <= 1){
		  $("#imagensExecutores").html($("#imagensExecutores").html() + ' <span class="col-xs p-icone executor mr-1" title="Executor: ' + executor[i] +'"><img id="imgExecutor' + i + '" class="rounded-circle" style="height:45px;width:45px;"></span>');
		  $("#imgExecutor" + i).attr("src", "../../media/usuarios/" + executor[i] + "/perfil/" + executor[i] + ".png").on("error", function(){
			$("#imgExecutor" + i).attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
		  });
		}
	  }
	}

	if (executores > 2){
		if ((parseInt(executores) - 2) == 1){
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 2) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 3) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 4) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 5) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 6) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 7) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\nExecutor: " + executor[8] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else if ((parseInt(executores) - 2) == 8) {
		  $("#imagensExecutores").html($("#imagensExecutores").html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\nExecutor: " + executor[8] + "\nExecutor: " + executor[9] + '" style="font-size: 12px;">+' + (parseInt(executores) - 2) + '</span>');
		} else {
		$("#imagensExecutores").html("Executores inválidos");
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
  