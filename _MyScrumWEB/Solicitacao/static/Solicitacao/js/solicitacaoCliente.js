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

//Esconder pessoa contato
document.getElementById( 'labelContato' ).style.display = 'none';
document.getElementById( 'id_pessoaContato' ).style.display = 'none';
document.getElementById( 'cpfContato' ).style.display = 'none';
document.getElementById( 'rgContato' ).style.display = 'none';
document.getElementById( 'emailContato' ).style.display = 'none';

//Função do sim e não do texto clicavel
$("#text_sim").click(function(){
	$("#id_pessoaContato").val($("#id_solicitante").val())
	$("#id_cpf_contato").val($("#id_cpf_solicitante").val())
	$("#id_rg_contato").val($("#id_rg_solicitante").val())
	$("#id_email_contato").val($("#id_email_solicitante").val())
//
	// document.getElementById( 'labelContato' ).style.display = 'inline';
	// document.getElementById( 'id_pessoaContato' ).style.display = 'inline';
	// document.getElementById( 'cpfContato' ).style.display = 'inline';
	// document.getElementById( 'rgContato' ).style.display = 'inline';
	// document.getElementById( 'emailContato' ).style.display = 'inline';
	document.getElementById( 'textContato' ).style.display = 'none';
	document.getElementById( 'textContato1' ).style.display = 'none';
	document.getElementById( 'textSeparar' ).style.display = 'none';
	document.getElementById( 'text_sim' ).style.display = 'none';
	document.getElementById( 'text_nao' ).style.display = 'none';
});

$("#text_nao").click(function(){
	document.getElementById( 'labelContato' ).style.display = 'inline';
	document.getElementById( 'id_pessoaContato' ).style.display = 'inline';
	document.getElementById( 'cpfContato' ).style.display = 'inline';
	document.getElementById( 'rgContato' ).style.display = 'inline';
	document.getElementById( 'emailContato' ).style.display = 'inline';
	document.getElementById( 'textContato' ).style.display = 'none';
	document.getElementById( 'textContato1' ).style.display = 'none';
	document.getElementById( 'textSeparar' ).style.display = 'none';
	document.getElementById( 'text_sim' ).style.display = 'none';
	document.getElementById( 'text_nao' ).style.display = 'none';
});

// Função para adicionar problemas */
$("#add-problema").click(function(){
	if(contar() >= 1){
		comboALiberar = (10 - contar()) + 1;
		$("#problema"+comboALiberar+"").attr("hidden",false);
		console.log("exibir" +comboALiberar)
	}else{alert("Limite atingido")}
});

$("#remove-problema2").click(function(){
	 var ambiente = document.getElementById("id_ambiente2");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao2");
	 descricao.value = '';
	$("#problema2").attr("hidden", true);
})

$("#remove-problema3").click(function(){
	 var ambiente = document.getElementById("id_ambiente3");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao3");
	 descricao.value = '';
	$("#problema3").attr("hidden", true);
})

$("#remove-problema4").click(function(){
	 var ambiente = document.getElementById("id_ambiente4");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao4");
	 descricao.value = '';
	$("#problema4").attr("hidden", true);
})

$("#remove-problema5").click(function(){
	 var ambiente = document.getElementById("id_ambiente5");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao5");
	 descricao.value = '';
	$("#problema5").attr("hidden", true);
})

$("#remove-problema6").click(function(){
	 var ambiente = document.getElementById("id_ambiente6");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao6");
	 descricao.value = '';
	$("#problema6").attr("hidden", true);
})

$("#remove-problema7").click(function(){
	 var ambiente = document.getElementById("id_ambiente7");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao7");
	 descricao.value = '';
	$("#problema7").attr("hidden", true);
})

$("#remove-problema8").click(function(){
	 var ambiente = document.getElementById("id_ambiente8");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao8");
	 descricao.value = '';
	$("#problema8").attr("hidden", true);
})

$("#remove-problema9").click(function(){
	 var ambiente = document.getElementById("id_ambiente9");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao9");
	 descricao.value = '';
	$("#problema9").attr("hidden", true);
})

$("#remove-problema10").click(function(){
	 var ambiente = document.getElementById("id_ambiente10");
	 ambiente.selectedIndex = 0;

	 var descricao = document.getElementById("id_descricao10");
	 descricao.value = '';
	$("#problema10").attr("hidden", true);
})

//Função para filtrar os blocos
$("#id_empreendimento").change(function(){
	var empreendimento = document.getElementById("id_bloco");
	empreendimento.selectedIndex = 0;
})

// Função para selecionar os blocos
// var empreen = {
// 	'leJardin': {
// 		'Cannes',
// 		'Lyon',
// 		'Bourdeaux',
// 	}
//
// 	'villaHelvetia': {
// 		'I',
// 		'II',
// 		'III',
// 	},
// 	'vistaVerde': {
// 		'I',
// 		'II',
// 		'III',
// 		'IV',
// 		'V',
// 		'VI',
// 		'VII',
// 	},
// 	'grandVille': {
// 		'A',
// 		'B',
// 		'C',
// 		'D',
// 	},
// 	'belvedere': {
// 		'A',
// 		'B',
// 		'C',
// 	},
// 	'duettoDMariah': {
// 		'A',
// 		'B',
// 	},
// 	'imagine': {
// 		'A',
// 	}
//  'loftEkkoHouse': {
// 	  'A',
// 	}
// 	'montisResidence': {
// 		'A',
// 	}
// 	'parqueArvores': {
// 		'A',
// 		'B',
// 		'C',
// 		'D',
// 		'E',
// 		'F',
// 		'G',
// 		'H',
// 		'I',
// 		'J',
// 		'K',
// 	},
// 	'parqueFlores': {
// 		'A',
// 		'B',
// 		'C',
// 		'D',
// 		'E',
// 		'F',
// 		'G',
// 		'H',
// 		'I',
// 		'J',
// 		'K',
// 	},
// 	'parquePassaros': {
// 		'A',
// 		'B',
// 		'C',
// 		'D',
// 		'E',
// 		'F',
// 		'G',
// 		'H',
// 		'I',
// 		'J',
// 	},
// 	'vilagioDAmore': {
// 		'A',
// 		'B',
// 		'C',
// 		'D',
// 		'E',
// 	'villaUnita': {
// 		'II',
// 		'IV',
// 		},
// 		'terceiro'
// 	}
// }
