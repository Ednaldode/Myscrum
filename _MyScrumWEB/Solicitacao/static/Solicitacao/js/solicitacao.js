/* Função que conta quanto campos de executores estão ocultos */
function contar(){
	console.log(document.querySelectorAll('div[hidden=hidden]').length);
	return document.querySelectorAll('div[hidden=hidden]').length;
}

//Como fazer focus
// $("#text_sim").click(function(){
// if ($('#id_solicitante').val() == "") {
// 	$('#id_solicitante').focus();
// }

//Esconder Linhas com os problemas
document.getElementById( 'linha2' ).style.display = 'none';
document.getElementById( 'linha3' ).style.display = 'none';
document.getElementById( 'linha4' ).style.display = 'none';
document.getElementById( 'linha5' ).style.display = 'none';
document.getElementById( 'linha6' ).style.display = 'none';
document.getElementById( 'linha7' ).style.display = 'none';
document.getElementById( 'linha8' ).style.display = 'none';
document.getElementById( 'linha9' ).style.display = 'none';
document.getElementById( 'linha10' ).style.display = 'none';

//Função para adicionar problemas */
var listaALiberar = 1
$("#add-problema").click(function(){
		listaALiberar += 1 ;
		if (listaALiberar >10) {
			alert("Limite Atingido")
		} else {
			$("#linha"+listaALiberar+"").css("display","flex");
			console.log("exibir" +listaALiberar)
		}
});

$("#remover-problema").click(function(){
	listaALiberar -= 1;
	 // var ambiente = document.getElementById("id_ambiente2");
	 // ambiente.selectedIndex = 0;
	 //
	 // var descricao = document.getElementById("id_descricao2");
	 // descricao.value = '';
	$("#linha2").css("display","none");
})
