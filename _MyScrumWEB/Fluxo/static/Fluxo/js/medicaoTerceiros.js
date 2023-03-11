
var tarefa_id;
// $("#loader").show();

// 
function exibirTarefa(id_tarefa){
  url = '/kanban/exibir/tarefa/'+id_tarefa

  $.ajax({
    type: 'GET',
    url: url,
    dataType: 'json',
    beforeSend: function (){
      $("#ModalEditarTarefa").modal("show");
    },
    success: function (data){
      $("#ModalEditarTarefa .modal-content").html(data.html_form);
    },

  });
}
// 
let elaboracaoAtrasado = 0, elaboracaoAtencao = 0, elaboracaoAdiantado = 0, validacaoAtrasado = 0, validacaoAtencao = 0, validacaoAdiantado = 0, documentacaoAtrasado = 0, documentacaoAtencao = 0, documentacaoAdiantado = 0, nfAtrasado = 0, nfAtencao = 0, nfAdiantado = 0, tituloAtrasado = 0, tituloAtencao = 0, tituloAdiantado = 0;
function verificarAtraso(processo){
  switch(processo){
    case '1':
      elaboracaoAtrasado += 1;
      break;
    case '2':
      validacaoAtrasado += 1;
      break;
    case '3':
      documentacaoAtrasado += 1;
      break;
    case '4':
      nfAtrasado += 1;
      break;
    case '5':
      tituloAtrasado += 1;
      break;
    default:
      console.log('Sem medição');
  }
}
function verificarAtencao(processo){
  switch(processo){
    case '1':
      elaboracaoAtencao += 1;
      break;
    case '2':
      validacaoAtencao += 1;
      break;
    case '3':
      documentacaoAtencao += 1;
      break;
    case '4':
      nfAtencao += 1;
      break;
    case '5':
      tituloAtencao += 1;
      break;      
    default:
      console.log('Sem medição');
  }
}
function verificarAdiantado(processo){
  switch(processo){
    case '1':
      elaboracaoAdiantado += 1;
      break;
    case '2':
      validacaoAdiantado += 1;
      break;
    case '3':
      documentacaoAdiantado += 1;
      break;
    case '4':
      nfAdiantado += 1;
      break;
    case '5':
      tituloAdiantado += 1;
      break;
    default:
      console.log('Sem medição');
  }
}
// 
  //Codigo do Loading
  $(document).ready(function() {
    document.getElementById("load").classList.toggle('esconder');
    $("#accordion").css("opacity", "1");
    document.getElementById("collapseOne").classList.toggle('collapse');
    document.getElementById("collapseOne").classList.toggle('collapse');
    $('#buttonCollapse').attr('aria-expanded', 'false');
    $("#load").attr("hidden", true);

});
// 
function removerElementos(select){
  //Removendo todos option atualmente na combo
  while (select.length != 1) {
      select.remove(select.length-1);
  }

  $(select).attr('readonly', 'true');
}
// 
$('.clearAll').on('click', function() {
  $("#centrocusto").val( $('option:contains("Centros de custo")').val() );

  var $status = $("#status").select2();
  $status.val(null).trigger("change");

  var $departamento = $("#departamento").select2();
  $departamento.val(null).trigger("change");

  var $processo = $("#processo").select2();
  $processo.val(null).trigger("change");

  var $autoridade = $("#autoridade").select2();
  $autoridade.val(null).trigger("change");

  var $responsavel = $("#responsavel").select2();
  $responsavel.val(null).trigger("change");

  var $pessoa = $("#pessoa").select2();
  $pessoa.val(null).trigger("change");

  var $executor = $("#executor").select2();
  $executor.val(null).trigger("change");

  var $impedimento = $("#impedimento").select2();
  $impedimento.val(null).trigger("change");
});
// 

// 

$(function(){

  //Buscando cards do fluxo
  var teste = $('.tarefa');
  
  let contadorElaboracao = 0;
  let contadorValicacao = 0;
  let contadorDocumentacao = 0;
  let contadorNF = 0;
  let contadorTitulo = 0;
  let contadorFeito = 0;

  //Reconhecendo e formatando data atual
  let data = new Date();
  let dia = data.getDate();
  let mes = data.getMonth();
  let ano = data.getFullYear();

  //Adicionar 0 para dias/meses 1 e 9
  function formatarData(data){
    let dataFormatada
    if(data >= 0 && data <= 9){
      dataFormatada = data.toString();
      dataFormatada = '0' + dataFormatada;
    } else{
      dataFormatada = data.toString();
    }
    return dataFormatada;
  }
  
  //Guardando data atual formatada em variável
  let dataAtual = new Date(formatarData(ano) + '-' + formatarData(mes + 1) + '-' + formatarData(dia));

  //Percorrendo cada tarefa criada no kanban
  //indice = id / valor = conteúdo
  $.each(teste, function(indice, valor){
    // Adicionando quantidade finalizados/problemas
    if ($('#idMedicao' + $(valor).attr('id')).text() == "1" && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorElaboracao += 1;
    } else if ($('#idMedicao' + $(valor).attr('id')).text() == "2" && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorValicacao += 1;
    } else if ($('#idMedicao' + $(valor).attr('id')).text() == "3" && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorDocumentacao += 1;
    } else if ($('#idMedicao' + $(valor).attr('id')).text() == "4" && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorNF += 1;
    } else if ($('#idMedicao' + $(valor).attr('id')).text() == "5" && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorTitulo += 1;
    } else if ($('#stat' + $(valor).attr('id')).text() == "Feito"){
      contadorFeito += 1;
    } else {
      console.log("ID medicao incorreto")
    }

    //Buscando dados no código
    let dataInicial = $('#dataInicial' + $(valor).attr('id')).text().split('/');
    let dataFinal = $('#dataFinal' + $(valor).attr('id')).text().split('/');

    //Colocando data formatada no Date()
    let inicial = new Date(dataInicial[2] + '-' + dataInicial[1] + '-' + dataInicial[0]);
    let final = new Date(dataFinal[2] + '-' + dataFinal[1] + '-' + dataFinal[0]);

    // Adicionando valores para cálculo de atraso
    let realizado = $(".progress-bar" + $(valor).attr('id')).attr('aria-valuenow');
    let previsto;

    let diaUtil = 0
    for (i = inicial.getTime(); i <= final.getTime() ; i += 86400000){
      i += 86400000;
      diaSemana = new Date(i);
      if ( (diaSemana.getDay() > 0) && (diaSemana.getDay() < 6) ) {
        diaUtil += 1;
      }
      i -= 86400000;
    }
    previsto = (100 * (dataAtual.getTime() - (inicial.getTime()) + 86400000) / 86400000) / diaUtil;
    let previstoDiario = 100 / diaUtil;
    let diasAdiantado = (realizado - previsto) / previstoDiario;

    if (inicial.getTime() > dataAtual.getTime()){
      previsto = 0;
    } else if (final.getTime() - dataAtual.getTime() == 0 || final.getTime() < dataAtual.getTime()){
      previsto = 100;
    }

    //Verificando status das tarefas e adicionando cores de fundo
    // if ($("#statusProcesso" + $(valor).attr('id')).text() == 'Concluído' || $("#statusProcesso" + $(valor).attr('id')).text() == 'Fora de Garantia'){ //Concluído
    if ($("#stat" + $(valor).attr('id')).text() == 'Feito'){
      //Adicionando fundo cinza para tarefas finalizadas
      $(valor).toggleClass('finalizada');

      //Calculando status do prazo / finalizada hoje ou x dias
      if (dataAtual.getTime() == final.getTime()){
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada:" aria-label="100%"> <div style="display: none;"> <span id="finalizada' + $(valor).attr('id') + '">0</span> </div> Hoje </span>');
      } else if ((dataAtual.getTime() - final.getTime()) / 86400000 == 1) {
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"> <span id="finalizada' + $(valor).attr('id') + '">1</span> dia</span>');
      } else{
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"><span id="finalizada' + $(valor).attr('id') + '">' + (dataAtual.getTime() - final.getTime()) / 86400000 + '</span> dias </span>');
      }

    } else if ($("#stat" + $(valor).attr('id')).text() == 'Fazendo'){ //Fazendo
      if (realizado > previsto){ //Adiantado
        //Adicionando fundo verde para tarefas
        $(valor).toggleClass('adiantada');
        verificarAdiantado($("#idMedicao" + $(valor).attr('id')).text())
        //Adicionando cor verde ao status do prazo
        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-success')

        //Adicionando fundo verde para barra de progresso
        $('.progress-bar' + $(valor).attr('id')).css('background', '#03F40F')

        //Calculando status do prazo
        if (diasAdiantado >= 0 && diasAdiantado < 2){
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Adiantada em:" aria-label="100%"> ↑ <span id="adiantada' + $(valor).attr('id') + '">' + (realizado - previsto).toFixed(2) + '</span> % - <span>' + diasAdiantado.toFixed(2) + '</span> dia</span>');
        } else {
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Adiantada em:" aria-label="100%"> ↑ <span id="adiantada' + $(valor).attr('id') + '">' + (realizado - previsto).toFixed(2) + '</span> % - <span>' + diasAdiantado.toFixed(2) + '</span> dias</span>');
        }
      } else if ((inicial.getTime() + ($('#statusPrazo' + $(valor).attr('id')).text() * 86400000)) >= dataAtual.getTime()) { //Atenção
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');
        verificarAtencao($("#idMedicao" + $(valor).attr('id')).text())
        //Adicionando fundo amarelo para barra de progresso
        $('.progress-bar' + $(valor).attr('id')).css('background', 'yellow')

        //Adicionando cor amarela ao status do prazo
        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-warning')

        //Calculando status do prazo / inicia hoje ou x dias
        if (inicial.getTime() == dataAtual.getTime()){
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Iniciada:" aria-label="100%"> <div style="display: none;"> <span id="atencao' + $(valor).attr('id') + '">0</span> </div>Hoje </span>');
        } else {
          if ((inicial.getTime() - dataAtual.getTime()) / 86400000 == -1){
            $('#statusPrazo' + $(valor).attr('id')).html('<span title="Iniciada há:" aria-label="100%"> <span id="atencao' + $(valor).attr('id') + '">1</span> dia</span>');
          } else {
            $('#statusPrazo' + $(valor).attr('id')).html('<span title="Iniciada há:" aria-label="100%"><span id="atencao' + $(valor).attr('id') + '">' + (dataAtual.getTime() - inicial.getTime()) / 86400000 + '</span> dias</span>');
          }
        }
      } else { //Atrasado
        //Adicionando fundo vermelho para tarefas
        $(valor).toggleClass('atrasada');
        verificarAtraso($("#idMedicao" + $(valor).attr('id')).text())
        //Adicionando fundo vermelho para barra de progresso
        $('.progress-bar' + $(valor).attr('id')).css('background', 'red')

        //Adicionando cor vermelha ao status do prazo
        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-danger')

        //Calculando status do prazo
        if ((final.getTime() - dataAtual.getTime()) / 86400000 == -1){
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Atrasada em:" aria-label="100%"> ↓ <span id="atrasada' + $(valor).attr('id') + '">' + (previsto - realizado).toFixed(2) + '</span> % - <span>1</span> dia</span>');
        } else {
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Atrasada em:" aria-label="100%"> ↓ <span id="atrasada' + $(valor).attr('id') + '">' + (previsto - realizado).toFixed(2) + '</span> % - <span>' + (dataAtual.getTime() - final.getTime()) / 86400000 + '</span> dias</span>');
        }
      }
    } else {
      if (inicial.getTime() >= dataAtual.getTime()){
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');

        //Incrementando variável com quantidade de tarefas
        verificarAtencao($("#idMedicao" + $(valor).attr('id')).text())        
        
        //Adicionando cor amarela ao status do prazo
        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-warning')
        //Calculando status do prazo / inicia hoje ou x dias
        if (inicial.getTime() == dataAtual.getTime()){
          $('#statusPrazo' + $(valor).attr('id')).html('<span title="Inicia:" aria-label="100%"> <div style="display: none;"> <span id="atencao' + $(valor).attr('id') + '">0</span> </div> Hoje </span>');
        } else {
          if ((inicial.getTime() - dataAtual.getTime()) / 86400000 == 1){
            $('#statusPrazo' + $(valor).attr('id')).html('<span title="Inicia em:" aria-label="100%"> <span id="atencao' + $(valor).attr('id') + '">1</div> dia</span>');
          } else {
            $('#statusPrazo' + $(valor).attr('id')).html('<span title="Inicia em:" aria-label="100%"><span id="atencao' + $(valor).attr('id') + '">' + (inicial.getTime() - dataAtual.getTime()) / 86400000 + '</span> dias</span>');
          }
        }
      } else {
        //Adicionando fundo vermelho para tarefas
        $(valor).toggleClass('atrasada');

        //Incrementando variável com quantidade de tarefas
        verificarAtraso($("#idMedicao" + $(valor).attr('id')).text())

        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-danger')
        realizado = 0;

        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Atrasada em:" aria-label="100%"> ↓ <span id="atrasada' + $(valor).attr('id') + '">' + (previsto - realizado).toFixed(2) + '</span> % - <span>' + ((dataAtual.getTime() - inicial.getTime()) / 86400000 + 1) + '</span> dias</span>');
      }
    }


    //Adicionando executores
    //Separa executores da tarefa
    let executor = $("#executores" + $(valor).attr('id')).html().split(",");
    listaExecutor = []
    for(i=0; i<10; i++){
      if(executor[i] != "None"){
        listaExecutor.push(executor[i])
      }
    }

    //Verifica se há 1 ou 2 executores na tarefa
    for (let i = 0; i < listaExecutor.length; i++){
      if (i <= 1){
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs p-icone executor mr-1" title="Executor: ' + listaExecutor[i] +'"><img id="imgExecutor' + $(valor).attr('id') + i + '" class="rounded-circle" style="width: 100%; height: 100%"></span>');
        $("#imgExecutor" + $(valor).attr('id') + i).attr("src", "../../media/usuarios/" + listaExecutor[i] + "/perfil/" + listaExecutor[i] + ".png").on("error", function(){
          $("#imgExecutor" + $(valor).attr('id') + i).attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
        });
      }
    }

    if (listaExecutor.length > 2){
      if ((parseInt(listaExecutor.length) - 2) == 1){
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 2) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 3) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 4) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + "\nExecutor: " + listaExecutor[5] + "\n" + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 5) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + "\nExecutor: " + listaExecutor[5] + "\nExecutor: " + listaExecutor[6] + "\n" + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 6) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + "\nExecutor: " + listaExecutor[5] + "\nExecutor: " + listaExecutor[6] + "\nExecutor: " + listaExecutor[7] + "\n" + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 7) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + "\nExecutor: " + listaExecutor[5] + "\nExecutor: " + listaExecutor[6] + "\nExecutor: " + listaExecutor[7] + "\nExecutor: " + listaExecutor[8] + "\n" + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else if ((parseInt(listaExecutor.length) - 2) == 8) {
        $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + listaExecutor[2] + "\nExecutor: " + listaExecutor[3] + "\nExecutor: " + listaExecutor[4] + "\nExecutor: " + listaExecutor[5] + "\nExecutor: " + listaExecutor[6] + "\nExecutor: " + listaExecutor[7] + "\nExecutor: " + listaExecutor[8] + "\nExecutor: " + listaExecutor[9] + '" style="font-size: 12px;">+' + (parseInt(listaExecutor.length) - 2) + '</span>');
      } else {
      $("#imagensExecutores" + $(valor).attr('id')).html("Executores inválidos");
      }
     }

    //Removendo circulo/imagem de pendencia se não houver
    let pessoaImpedimento = $("#impedimento" + $(valor).attr('id')).attr('title');
    $("#impedimento" + $(valor).attr('id')).prop('title', 'Impedimento: ' + pessoaImpedimento);
    if (pessoaImpedimento == '' || pessoaImpedimento == 'None'){
      $("#impedimento" + $(valor).attr('id')).hide();
      $('#problemas' + $(valor).attr('id')).css('margin', 'auto 0 auto auto');
    } else {
        $("#imgImpedimento" + $(valor).attr('id')).attr("src", "../../media/usuarios/" + pessoaImpedimento + "/perfil/" + pessoaImpedimento + ".png").on("error", function(){
          $("#imgImpedimento" + $(valor).attr('id')).attr("src", "../../media/usuarios/Padrão/perfil/Padrão.png");
        });
    }

  });

  //Adicionando quantidade de tarefas em cada coluna
  qtdProcessos = $("#qtdProcessos").html().split(",")
  $(".titulos").html(`
    <span title="Adiantados: ${elaboracaoAdiantado}\nAvisos: ${elaboracaoAtencao}\nAtrasados: ${elaboracaoAtrasado}" class="titulo-child afazer">Elaboração | ${contadorElaboracao}</span>
    <span title="Adiantados: ${validacaoAdiantado}\nAvisos: ${validacaoAtencao}\nAtrasados: ${validacaoAtrasado}" class="titulo-child fazendo">Validação | ${contadorValicacao}</span>
    <span title="Adiantados: ${documentacaoAdiantado}\nAvisos: ${documentacaoAtencao}\nAtrasados: ${documentacaoAtrasado}" class="titulo-child feito">Documentação | ${contadorDocumentacao}</span>
    <span title="Adiantados: ${nfAdiantado}\nAvisos: ${nfAtencao}\nAtrasados: ${nfAtrasado}" class="titulo-child afazer">Nota Fiscal | ${contadorNF}</span>
    <span title="Adiantados: ${tituloAdiantado}\nAvisos: ${tituloAtencao}\nAtrasados: ${tituloAtrasado}" class="titulo-child afazer">Título a Pagar | ${contadorTitulo}</span>
    <span title="Feitos: ${contadorFeito}" class="titulo-child feito">Feito | ${contadorFeito}</span>
    `);

// Script para selecionar as tarefas para transporte ao serem clicadas -----------------------
  $('.tarefa').mousedown(function(){
    var tarefa = $(this);
    var fundo = tarefa.css("background-color");
    var branco = "rgb(255, 255, 255)";
    var selecionada = "#fff";
    if(fundo==branco){
      tarefa.css("background-color",selecionada);
      tarefa.addClass("selecionada");
    } else if(fundo==selecionada){
      tarefa.css("background-color",branco);
      tarefa.removeClass("selecionada");
    }
  });

  $('.bt_expandir').click(function(e){
    e.preventDefault();
    capturaId();
    ignoraSelecao();
    var mostrar = tarefa_id+"_mostrar"; //pega apenas o primeiro
    var display = $('#'+mostrar).css("display");
    if(display=='none'){
      $(this).toggleClass('rodar');
      $('#'+mostrar).show('slow');
    } else {
      $(this).toggleClass('rodar');
      $('#'+mostrar).hide('slow');
    }
  });

  $('.bt_editar').click(function(e){
    e.preventDefault();
    capturaId();
    ignoraSelecao();
    localStorage.controller1 = 7;
  });

  $("#fluxos").addClass("show-bar").addClass("mostrar");
  $("#sidebarCollapse").click(function(){
    $("#fluxos").toggleClass("show-bar");
    $("#fluxos").toggleClass("hide-bar");
  });
});

function capturaId(){
  tarefa_id = $('.selecionada').attr("id");
}

function ignoraSelecao(){
  $('.tarefa').removeClass('selecionada');
  $('.tarefa').css("background-color","rgb(255, 255, 255)");
}