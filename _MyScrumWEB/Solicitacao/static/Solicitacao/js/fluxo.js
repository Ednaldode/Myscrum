
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
let analiseAtrasado = 0, analiseAtencao = 0, analiseAdiantado = 0, agendamentoAtrasado = 0, agendamentoAtencao = 0, agendamentoAdiantado = 0, atendimentoAtrasado = 0, atendimentoAtencao = 0, atendimentoAdiantado = 0, quitacaoAtrasado = 0, quitacaoAtencao = 0, quitacaoAdiantado = 0;
function verificarAtraso(processo){
  switch(processo){
    case 'Análise':
      analiseAtrasado += 1;
      break;
    case 'Agendamento':
      agendamentoAtrasado += 1;
      break;
    case 'Atendimento':
      atendimentoAtrasado += 1;
      break;
    case 'Termo de Quitação':
      quitacaoAtrasado += 1;
      break;
    default:
      console.log('Sem status processo');
  }
}
function verificarAtencao(processo){
  switch(processo){
    case 'Análise':
      analiseAtencao += 1;
      break;
    case 'Agendamento':
      agendamentoAtencao += 1;
      break;
    case 'Atendimento':
      atendimentoAtencao += 1;
      break;
    case 'Termo de Quitação':
      quitacaoAtencao += 1;
      break;
    default:
      console.log('Sem status processo');
  }
}
function verificarAdiantado(processo){
  switch(processo){
    case 'Análise':
      analiseAdiantado += 1;
      break;
    case 'Agendamento':
      agendamentoAdiantado += 1;
      break;
    case 'Atendimento':
      atendimentoAdiantado += 1;
      break;
    case 'Termo de Quitação':
      quitacaoAdiantado += 1;
      break;
    default:
      console.log('Sem status processo');
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
  
  let contadorAnalise = 0;
  let listaPAnalise = $("#problemasAnalise").attr("title").substr(1, ($("#problemasAnalise").attr("title").length - 2)).split(", ");
  let listaFAnalise = $("#problemasAnalise").text().substr(1, ($("#problemasAnalise").text().length - 2)).split(", ");

  let contadorAgendamento = 0;
  let listaPAgendamento = $("#problemasAgendamento").attr("title").substr(1, ($("#problemasAgendamento").attr("title").length - 2)).split(", ");
  let listaFAgendamento = $("#problemasAgendamento").text().substr(1, ($("#problemasAgendamento").text().length - 2)).split(", ");

  let contadorAtendimento = 0;
  let listaPAtendimento = $("#problemasAtendimento").attr("title").substr(1, ($("#problemasAtendimento").attr("title").length - 2)).split(", ");
  let listaFAtendimento = $("#problemasAtendimento").text().substr(1, ($("#problemasAtendimento").text().length - 2)).split(", ");

  let contadorTermo = 0;
  let listaPTermo = $("#problemasTermo").attr("title").substr(1, ($("#problemasTermo").attr("title").length - 2)).split(", ");
  let listaFTermo = $("#problemasTermo").text().substr(1, ($("#problemasTermo").text().length - 2)).split(", ");

  let contadorConcluido = 0;
  let listaPConcluido = $("#problemasConcluido").attr("title").substr(1, ($("#problemasConcluido").attr("title").length - 2)).split(", ");
  let listaFConcluido = $("#problemasConcluido").text().substr(1, ($("#problemasConcluido").text().length - 2)).split(", ");

  let contadorGarantia = 0;
  let listaPGarantia = $("#problemasGarantia").attr("title").substr(1, ($("#problemasGarantia").attr("title").length - 2)).split(", ");
  let listaFGarantia = $("#problemasGarantia").text().substr(1, ($("#problemasGarantia").text().length - 2)).split(", ");

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
    if ($('#statusProcesso' + $(valor).attr('id')).text() == "Análise"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFAnalise[contadorAnalise]}/${listaPAnalise[contadorAnalise]}`);
      contadorAnalise += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == "Agendamento"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFAgendamento[contadorAgendamento]}/${listaPAgendamento[contadorAgendamento]}`);
      contadorAgendamento += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == "Atendimento"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFAtendimento[contadorAtendimento]}/${listaPAtendimento[contadorAtendimento]}`);
      contadorAtendimento += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == "Termo de Quitação"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFTermo[contadorTermo]}/${listaPTermo[contadorTermo]}`);
      contadorTermo += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == "Concluído"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFConcluido[contadorConcluido]}/${listaPConcluido[contadorConcluido]}`);
      contadorConcluido += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == "Fora de Garantia"){
      $('#problemas' + $(valor).attr('id')).text(`${listaFGarantia[contadorGarantia]}/${listaPGarantia[contadorGarantia]}`);
      contadorGarantia += 1;
    } else {
      console.log("Sem agendamento")
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
    if ($("#statusProcesso" + $(valor).attr('id')).text() == 'Concluído'){
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

    } else if ($("#statusProcesso" + $(valor).attr('id')).text() == 'Fora de Garantia'){
      //Adicionando fundo cinza para tarefas rejeitadas
      $(valor).toggleClass('garantia');

      //Calculando status do prazo / finalizada hoje ou x dias
      if (dataAtual.getTime() == final.getTime()){
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada:" aria-label="100%"> <div style="display: none;"> <span id="finalizada' + $(valor).attr('id') + '">0</span> </div> Hoje </span>');
      } else if ((dataAtual.getTime() - final.getTime()) / 86400000 == 1) {
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"> <span id="finalizada' + $(valor).attr('id') + '">1</span> dia</span>');
      } else{
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"><span id="finalizada' + $(valor).attr('id') + '">' + (dataAtual.getTime() - final.getTime()) / 86400000 + '</span> dias </span>');
      }
    } else { //Fazendo
      if (realizado > previsto){
        //Adicionando fundo verde para tarefas
        $(valor).toggleClass('adiantada');
        verificarAdiantado($("#statusProcesso" + $(valor).attr('id')).text())
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
      } else if ((inicial.getTime() + (30 * 86400000)) >= dataAtual.getTime()) {
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');
        verificarAtencao($("#statusProcesso" + $(valor).attr('id')).text())
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
      } else {
        //Adicionando fundo vermelho para tarefas
        $(valor).toggleClass('atrasada');
        verificarAtraso($("#statusProcesso" + $(valor).attr('id')).text())
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
    <span title="Adiantados: ${analiseAdiantado}\nAvisos: ${analiseAtencao}\nAtrasados: ${analiseAtrasado}" class="titulo-child afazer">Análise | ${qtdProcessos[0].replace("[", "")}</span>
    <span title="Adiantados: ${agendamentoAdiantado}\nAvisos: ${agendamentoAtencao}\nAtrasados: ${agendamentoAtrasado}" class="titulo-child fazendo">Agendamento | ${qtdProcessos[1]}</span>
    <span title="Adiantados: ${atendimentoAdiantado}\nAvisos: ${atendimentoAtencao}\nAtrasados: ${atendimentoAtrasado}" class="titulo-child feito">Atendimento | ${qtdProcessos[2]}</span>
    <span title="Adiantados: ${quitacaoAdiantado}\nAvisos: ${quitacaoAtencao}\nAtrasados: ${quitacaoAtrasado}" class="titulo-child afazer">Termo de Quitação | ${qtdProcessos[3]}</span>
    <span title="Concluído: ${qtdProcessos[4]}" class="titulo-child fazendo">Concluído | ${qtdProcessos[4]}</span>
    <span title="Fora de Garantia: ${qtdProcessos[5].replace("]", "")}" class="titulo-child feito">Fora de Garantia | ${qtdProcessos[5].replace("]", "")}</span>
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
    localStorage.controller1 = 5;
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

var verificarProprietarios = $("#listaProprietarios").html();
var verificarBlocos = $("#listaBloco").html();
var verificarUnidades = $("#listaUnidade").html();
var verificarContatos = $("#listaContatos").html();
var verificarEmails = $("#listaEmails").html();

var optionProprietario = `<option>Proprietário</option>`;
var optionBloco = `<option>Bloco</option>`;
var optionUnidade = `<option>Unidade</option>`;
var optionContato = `<option>Contato</option>`;
var optionEmail = `<option>E-mail</option>`;

var selecionadosProprietarios = $("#selecionadosProprietario").html();
var selecionadosBlocos = $("#selecionadosBloco").html();
var selecionadosUnidades = $("#selecionadosUnidade").html();
var selecionadosContato = $("#selecionadosContato").html();
var selecionadosEmail = $("#selecionadosEmail").html();

qtdProprietarios = verificarProprietarios.split(",");
qtdBlocos = verificarBlocos.split(",");
qtdUnidades = verificarUnidades.split(",");
qtdContatos = verificarContatos.split(",");
qtdEmails = verificarEmails.split(",");

// Proprietários -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
var proprietariosSelecionados = []
if (selecionadosProprietarios != undefined){
  qtdSelecionados = selecionadosProprietarios.split(",")
  for (i = 0; i < qtdSelecionados.length - 1; i++) {
    proprietariosSelecionados.push(qtdSelecionados[i].substr(2, (qtdSelecionados[i].length - 3)));
  }
  proprietariosSelecionados.push(qtdSelecionados[qtdSelecionados.length - 1].substr(2, (qtdSelecionados[qtdSelecionados.length - 1].length - 4)));
}

if (proprietariosSelecionados[0] != ""){
  for (i = 0; i < qtdProprietarios.length - 1; i++) {
  proprietariosSelecionados.includes(qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))) ? optionProprietario += `<option selected>${qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))}</option>` : optionProprietario += `<option>${qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))}</option>`;
  }
  proprietariosSelecionados.includes(qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))) ? optionProprietario += `<option selected>${qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))}</option>`: optionProprietario += `<option>${qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))}</option>`;
  $("#proprietario").html(optionProprietario);
} else{
  for (i = 0; i < qtdProprietarios.length - 1; i++) {
  proprietariosSelecionados.includes(qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))) ? optionProprietario += `<option>${qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))}</option>` : optionProprietario += `<option>${qtdProprietarios[i].substr(2, (qtdProprietarios[i].length - 3))}</option>`;
  }
  proprietariosSelecionados.includes(qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))) ? optionProprietario += `<option>${qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))}</option>`: optionProprietario += `<option>${qtdProprietarios[qtdProprietarios.length - 1].substr(2, (qtdProprietarios[qtdProprietarios.length - 1].length - 4))}</option>`;
  $("#proprietario").html(optionProprietario);
}
// Blocos -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
var blocosSelecionados = []
if (selecionadosBlocos != undefined){
  qtdSelecionados = selecionadosBlocos.split(",")
  for (i = 0; i < qtdSelecionados.length - 1; i++) {
    blocosSelecionados.push(qtdSelecionados[i].substr(2, (qtdSelecionados[i].length - 3)));
  }
  blocosSelecionados.push(qtdSelecionados[qtdSelecionados.length - 1].substr(2, (qtdSelecionados[qtdSelecionados.length - 1].length - 4)));
}

if (blocosSelecionados[0] != ""){
  for (i = 0; i < qtdBlocos.length - 1; i++) {
    blocosSelecionados.includes(qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))) ? optionBloco += `<option selected>${qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))}</option>` : optionBloco += `<option>${qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))}</option>`;
  }
  blocosSelecionados.includes(qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))) ? optionBloco += `<option selected>${qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))}</option>`: optionBloco += `<option>${qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))}</option>`;
  $("#bloco").html(optionBloco);
} else{
  for (i = 0; i < qtdBlocos.length - 1; i++) {
    blocosSelecionados.includes(qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))) ? optionBloco += `<option>${qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))}</option>` : optionBloco += `<option>${qtdBlocos[i].substr(2, (qtdBlocos[i].length - 3))}</option>`;
  }
  blocosSelecionados.includes(qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))) ? optionBloco += `<option>${qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))}</option>`: optionBloco += `<option>${qtdBlocos[qtdBlocos.length - 1].substr(2, (qtdBlocos[qtdBlocos.length - 1].length - 4))}</option>`;
  $("#bloco").html(optionBloco);
}

// Unidades -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
var unidadesSelecionados = []
if (selecionadosUnidades != undefined){
  qtdSelecionados = selecionadosUnidades.split(",")
  for (i = 0; i < qtdSelecionados.length - 1; i++) {
    unidadesSelecionados.push(qtdSelecionados[i].substr(2, (qtdSelecionados[i].length - 3)));
  }
  unidadesSelecionados.push(qtdSelecionados[qtdSelecionados.length - 1].substr(2, (qtdSelecionados[qtdSelecionados.length - 1].length - 4)));
}

console.log()

if (unidadesSelecionados[0] != ""){
  for (i = 0; i < qtdUnidades.length - 1; i++) {
    unidadesSelecionados.includes(qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))) ? optionUnidade += `<option selected>${qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))}</option>` : optionUnidade += `<option>${qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))}</option>`;
  }
  unidadesSelecionados.includes(qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))) ? optionUnidade += `<option selected>${qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))}</option>`: optionUnidade += `<option>${qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))}</option>`;
  $("#unidade").html(optionUnidade);
} else{
  for (i = 0; i < qtdUnidades.length - 1; i++) {
    unidadesSelecionados.includes(qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))) ? optionUnidade += `<option>${qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))}</option>` : optionUnidade += `<option>${qtdUnidades[i].substr(2, (qtdUnidades[i].length - 3))}</option>`;
  }
  unidadesSelecionados.includes(qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))) ? optionUnidade += `<option>${qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))}</option>`: optionUnidade += `<option>${qtdUnidades[qtdUnidades.length - 1].substr(2, (qtdUnidades[qtdUnidades.length - 1].length - 4))}</option>`;
  $("#unidade").html(optionUnidade);
}
// Contato -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
var contatosSelecionados = []
if (selecionadosContato != undefined){
  qtdSelecionados = selecionadosContato.split(",")
  for (i = 0; i < qtdSelecionados.length - 1; i++) {
    contatosSelecionados.push(qtdSelecionados[i].substr(2, (qtdSelecionados[i].length - 3)));
  }
  contatosSelecionados.push(qtdSelecionados[qtdSelecionados.length - 1].substr(2, (qtdSelecionados[qtdSelecionados.length - 1].length - 4)));
}

if (contatosSelecionados[0] != ""){
  for (i = 0; i < qtdContatos.length - 1; i++) {
    contatosSelecionados.includes(qtdContatos[i].substr(2, (qtdContatos[i].length - 3))) ? optionContato += `<option selected>${qtdContatos[i].substr(2, (qtdContatos[i].length - 3))}</option>` : optionContato += `<option>${qtdContatos[i].substr(2, (qtdContatos[i].length - 3))}</option>`;
  }
  contatosSelecionados.includes(qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))) ? optionContato += `<option selected>${qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))}</option>`: optionContato += `<option>${qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))}</option>`;
  $("#contato").html(optionContato);
} else{
  for (i = 0; i < qtdContatos.length - 1; i++) {
    contatosSelecionados.includes(qtdContatos[i].substr(2, (qtdContatos[i].length - 3))) ? optionContato += `<option>${qtdContatos[i].substr(2, (qtdContatos[i].length - 3))}</option>` : optionContato += `<option>${qtdContatos[i].substr(2, (qtdContatos[i].length - 3))}</option>`;
  }
  contatosSelecionados.includes(qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))) ? optionContato += `<option>${qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))}</option>`: optionContato += `<option>${qtdContatos[qtdContatos.length - 1].substr(2, (qtdContatos[qtdContatos.length - 1].length - 4))}</option>`;
  $("#contato").html(optionContato);
}

// E-mails -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
var emailsSelecionados = []
if (selecionadosEmail != undefined){
  qtdSelecionados = selecionadosEmail.split(",")
  for (i = 0; i < qtdSelecionados.length - 1; i++) {
    emailsSelecionados.push(qtdSelecionados[i].substr(2, (qtdSelecionados[i].length - 3)));
  }
  emailsSelecionados.push(qtdSelecionados[qtdSelecionados.length - 1].substr(2, (qtdSelecionados[qtdSelecionados.length - 1].length - 4)));
}

if (emailsSelecionados[0] != ""){
  for (i = 0; i < qtdEmails.length - 1; i++) {
    emailsSelecionados.includes(qtdEmails[i].substr(2, (qtdEmails[i].length - 3))) ? optionEmail += `<option selected>${qtdEmails[i].substr(2, (qtdEmails[i].length - 3))}</option>` : optionEmail += `<option>${qtdEmails[i].substr(2, (qtdEmails[i].length - 3))}</option>`;
  }
  emailsSelecionados.includes(qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))) ? optionEmail += `<option selected>${qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))}</option>`: optionEmail += `<option>${qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))}</option>`;
  $("#email").html(optionEmail);
} else{
  for (i = 0; i < qtdEmails.length - 1; i++) {
    emailsSelecionados.includes(qtdEmails[i].substr(2, (qtdEmails[i].length - 3))) ? optionEmail += `<option>${qtdEmails[i].substr(2, (qtdEmails[i].length - 3))}</option>` : optionEmail += `<option>${qtdEmails[i].substr(2, (qtdEmails[i].length - 3))}</option>`;
  }
  emailsSelecionados.includes(qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))) ? optionEmail += `<option>${qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))}</option>`: optionEmail += `<option>${qtdEmails[qtdEmails.length - 1].substr(2, (qtdEmails[qtdEmails.length - 1].length - 4))}</option>`;
  $("#email").html(optionEmail);
}
