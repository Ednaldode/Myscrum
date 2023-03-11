var tarefa_id;

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

//Codigo do Loading
$(document).ready(function() {
  document.getElementById("load").classList.toggle('esconder');
  $("#accordion").css("opacity", "1");
  document.getElementById("collapseOne").classList.toggle('collapse');
  document.getElementById("collapseOne").classList.toggle('collapse');
  $('#buttonCollapse').attr('aria-expanded', 'false');
  $("#load").attr("hidden", true);

});

function removerElementos(select){
  //Removendo todos option atualmente na combo
  while (select.length != 1) {
      select.remove(select.length-1);
  }

  $(select).attr('readonly', 'true');
}

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

$(function(){

  //Buscando cards do fluxo
  var teste = $('.tarefa');

  let contadorMae = 0, contadorManutencao = 0, contadorNegociacao = 0, contadorContrato = 0, contadorEnergia = 0, contadorOrcar = 0, contadorPagar = 0, contadorInstalar = 0, contadorRetorno = 0, contadorLimpar = 0, contadorVistoria = 0, contadorChaves = 0;
  let maeAdiantado = 0, maeAtencao = 0, maeAtrasado = 0, negociacaoAdiantado = 0, negociacaoAtencao = 0, negociacaoAtrasado = 0, contratoAdiantado = 0, contratoAtencao = 0, contratoAtrasado = 0, energiaAdiantado = 0,
      energiaAtencao = 0, energiaAtrasado = 0, orcarAdiantado = 0, orcarAtencao = 0, orcarAtrasado = 0, pagarAdiantado = 0, pagarAtencao = 0, pagarAtrasado = 0, instalarAdiantado = 0, instalarAtencao = 0, instalarAtrasado = 0
      manutencaoAdiantado = 0, manutencaoAtencao = 0, manutencaoAtrasado = 0, limparAdiantado = 0, limparAtencao = 0, limparAtrasado = 0, vistoriaAdiantado = 0, vistoriaAtencao = 0, vistoriaAtrasado = 0, retornoAdiantado = 0, retornoAtencao = 0, retornoAtrasado = 0,
      chavesAdiantado = 0, chavesAtencao = 0, chavesAtrasado = 0, feito = 0;
  
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
    if ($('#statusProcesso' + $(valor).attr('id')).text() == 0){
      contadorMae += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 1 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorNegociacao += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 2 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorContrato += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 3 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorEnergia += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 4 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorOrcar += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 5 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorPagar += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 6 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorInstalar += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 7 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorLimpar += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 8 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorVistoria += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 9 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorChaves += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 10 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorManutencao += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 11 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorRetorno += 1;
    } else if ($('#stat' + $(valor).attr('id')).text() == "Feito"){
      feito += 1;
    } else {
      console.log("Sem agendamento")
    }
    
    atualizarMae($('#idLocacao' + $(valor).attr('id')).text(), $('#statusProcesso' + $(valor).attr('id')).text(), $(valor).attr('id'), $(".progress-bar" + $(valor).attr('id')).attr('aria-valuenow'))

    //Buscando dados no código
    let dataInicial = $('#dataInicial' + $(valor).attr('id')).text();
    let dataFinal = $('#dataFinal' + $(valor).attr('id')).text();

    //Formatando data para jQuery
    let formatarInicial = dataInicial.split('/');
    let formatarFinal= dataFinal.split('/');

    //Colocando data formatada no Date()
    let inicial = new Date(formatarInicial[2] + '-' + formatarInicial[1] + '-' + formatarInicial[0]);
    let final = new Date(formatarFinal[2] + '-' + formatarFinal[1] + '-' + formatarFinal[0]);

    // Adicionando valores para cálculo de atraso
    let prazo = $('#prazo' + $(valor).attr('id')).text();
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
    if ($('#stat' + $(valor).attr('id')).text() == "Feito"){ //Feito
      $(valor).toggleClass('finalizada');

      //Calculando status do prazo / finalizada hoje ou x dias
      if (dataAtual.getTime() == final.getTime()){
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada:" aria-label="100%"> <div style="display: none;"> <span id="finalizada' + $(valor).attr('id') + '">0</span> </div> Hoje </span>');
      } else if ((dataAtual.getTime() - final.getTime()) / 86400000 == 1) {
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"> <span id="finalizada' + $(valor).attr('id') + '">1</span> dia</span>');
      } else{
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"><span id="finalizada' + $(valor).attr('id') + '">' + (dataAtual.getTime() - final.getTime()) / 86400000 + '</span> dias </span>');
      }

    } else if ($('#stat' + $(valor).attr('id')).text() == "A fazer"){ //A fazer
      if (inicial.getTime() >= dataAtual.getTime()){
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');
        //Incrementando variável com quantidade de tarefas
        verificarAtencao($('#statusProcesso' + $(valor).attr('id')).text());
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
        verificarAtraso($('#statusProcesso' + $(valor).attr('id')).text());

        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-danger')
        realizado = 0;

        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Atrasada em:" aria-label="100%"> ↓ <span id="atrasada' + $(valor).attr('id') + '">' + (previsto - realizado).toFixed(2) + '</span> % - <span>' + ((dataAtual.getTime() - inicial.getTime()) / 86400000 + 1) + '</span> dias</span>');


      }
    } else { //Fazendo
      if (realizado > previsto){
        //Adicionando fundo verde para tarefas
        $(valor).toggleClass('adiantada');

        //Incrementando variável com quantidade de tarefas
        verificarAdiantado($('#statusProcesso' + $(valor).attr('id')).text());

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
      } else if ((inicial.getTime() + (prazo * 86400000)) >= dataAtual.getTime()) {
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');

        //Incrementando variável com quantidade de tarefas
        verificarAtencao($('#statusProcesso' + $(valor).attr('id')).text());

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

        //Incrementando variável com quantidade de tarefas
        verificarAtraso($('#statusProcesso' + $(valor).attr('id')).text());

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

  // $(".titulos").html(`
  //   <span title="Adiantados: ${maeAdiantado}\nAvisos: ${maeAtencao}\nAtrasados: ${maeAtrasado}" class="titulo-child afazer">Tarefa Mãe | ${contadorMae}</span>
  //   <span title="Adiantados: ${manutencaoAdiantado}\nAvisos: ${manutencaoAtencao}\nAtrasados: ${manutencaoAtrasado}" class="titulo-child afazer">Manutenção | ${contadorManutencao}</span>
  //   <span title="Adiantados: ${negociacaoAdiantado}\nAvisos: ${negociacaoAtencao}\nAtrasados: ${negociacaoAtrasado}" class="titulo-child fazendo">Negociação | ${contadorNegociacao}</span>
  //   <span title="Adiantados: ${contratoAdiantado}\nAvisos: ${contratoAtencao}\nAtrasados: ${contratoAtrasado}" class="titulo-child feito">Contrato | ${contadorContrato}</span>
  //   <span title="Adiantados: ${energiaAdiantado}\nAvisos: ${energiaAtencao}\nAtrasados: ${energiaAtrasado}" class="titulo-child afazer">Ligação de Energia | ${contadorEnergia}</span>
  //   <span title="Adiantados: ${orcarAdiantado}\nAvisos: ${orcarAtencao}\nAtrasados: ${orcarAtrasado}" class="titulo-child afazer">Orçar | ${contadorOrcar}</span>
  //   <span title="Adiantados: ${pagarAdiantado}\nAvisos: ${pagarAtencao}\nAtrasados: ${pagarAtrasado}" class="titulo-child afazer">Pagar | ${contadorPagar}</span>
  //   <span title="Adiantados: ${instalarAdiantado}\nAvisos: ${instalarAtencao}\nAtrasados: ${instalarAtrasado}" class="titulo-child afazer">Instalar | ${contadorInstalar}</span>
  //   <span title="Adiantados: ${limparAdiantado}\nAvisos: ${limparAtencao}\nAtrasados: ${limparAtrasado}" class="titulo-child feito">Limpar | ${contadorLimpar}</span>
  //   <span title="Adiantados: ${vistoriaAdiantado}\nAvisos: ${vistoriaAtencao}\nAtrasados: ${vistoriaAtrasado}" class="titulo-child afazer">Vistoria Final | ${contadorVistoria}</span>
  //   <span title="Adiantados: ${chavesAdiantado}\nAvisos: ${chavesAtencao}\nAtrasados: ${chavesAtrasado}" class="titulo-child afazer">Entrega de Chaves | ${contadorChaves}</span>
  //   <span title="Finalizados: ${feito}" class="titulo-child afazer">Feito | ${feito}</span>
  //   `);

  $(".titulos").html(`
    <span title="Adiantados: ${maeAdiantado}\nAvisos: ${maeAtencao}\nAtrasados: ${maeAtrasado}" class="titulo-child afazer">Tarefa Mãe | ${contadorMae}</span>
    <span title="Adiantados: ${manutencaoAdiantado}\nAvisos: ${manutencaoAtencao}\nAtrasados: ${manutencaoAtrasado}" class="titulo-child afazer">Manutenção | ${contadorManutencao}</span>
    <span title="Adiantados: ${energiaAdiantado}\nAvisos: ${energiaAtencao}\nAtrasados: ${energiaAtrasado}" class="titulo-child afazer">Ligação de Energia | ${contadorEnergia}</span>
    <span title="Adiantados: ${orcarAdiantado}\nAvisos: ${orcarAtencao}\nAtrasados: ${orcarAtrasado}" class="titulo-child afazer">Orçar | ${contadorOrcar}</span>
    <span title="Adiantados: ${pagarAdiantado}\nAvisos: ${pagarAtencao}\nAtrasados: ${pagarAtrasado}" class="titulo-child afazer">Pagar | ${contadorPagar}</span>
    <span title="Adiantados: ${instalarAdiantado}\nAvisos: ${instalarAtencao}\nAtrasados: ${instalarAtrasado}" class="titulo-child afazer">Instalar | ${contadorInstalar}</span>
    <span title="Adiantados: ${limparAdiantado}\nAvisos: ${limparAtencao}\nAtrasados: ${limparAtrasado}" class="titulo-child feito">Limpar | ${contadorLimpar}</span>
    <span title="Adiantados: ${retornoAdiantado}\nAvisos: ${retornoAtencao}\nAtrasados: ${retornoAtrasado}" class="titulo-child afazer">Retorno | ${contadorRetorno}</span>
    <span title="Finalizados: ${feito}" class="titulo-child afazer">Feito | ${feito}</span>
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
    localStorage.controller1 = 1;
  });

  $("#fluxos").addClass("show-bar").addClass("mostrar");
  $("#sidebarCollapse").click(function(){
    $("#fluxos").toggleClass("show-bar");
    $("#fluxos").toggleClass("hide-bar");
  });

  function verificarAtraso(processo){
    switch(processo){
      case '0':
        maeAtrasado += 1;
        break;
      case '1':
        negociacaoAtrasado += 1;
        break;
      case '2':
        contratoAtrasado += 1;
        break;
      case '3':
        energiaAtrasado += 1;
        break;
      case '4':
        orcarAtrasado += 1;
        break;
      case '5':
        pagarAtrasado += 1;
        break;
      case '6':
        instalarAtrasado += 1;
        break;
      case '7':
        limparAtrasado += 1;
        break;
      case '8':
        vistoriaAtrasado += 1;
        break;
      case '9':
        chavesAtrasado += 1;
        break;
      case '10':
          manutencaoAtrasado += 1;
          break;
      case '11':
          retornoAtrasado += 1;
          break;
      default:
        console.log('Sem status processo');
    }
  }
  function verificarAtencao(processo){
    switch(processo){
      case '0':
        maeAtencao += 1;
        break;
      case '1':
        negociacaoAtencao += 1;
        break;
      case '2':
        contratoAtencao += 1;
        break;
      case '3':
        energiaAtencao += 1;
        break;
      case '4':
        orcarAtencao += 1;
        break;
      case '5':
        pagarAtencao += 1;
        break;
      case '6':
        instalarAtencao += 1;
        break;
      case '7':
        limparAtencao += 1;
        break;
      case '8':
        vistoriaAtencao += 1;
        break;
      case '9':
        chavesAtencao += 1;
        break;
      case '10':
          manutencaoAtencao += 1;
          break;
      case '11':
          retornoAtencao += 1;
          break;
      default:
        console.log('Sem status processo');
    }
  }
  function verificarAdiantado(processo){
    switch(processo){
      case '0':
        maeAdiantado += 1;
        break;
      case '1':
        negociacaoAdiantado += 1;
        break;
      case '2':
        contratoAdiantado += 1;
        break;
      case '3':
        energiaAdiantado += 1;
        break;
      case '4':
        orcarAdiantado += 1;
        break;
      case '5':
        pagarAdiantado += 1;
        break;
      case '6':
        instalarAdiantado += 1;
        break;
      case '7':
        limparAdiantado += 1;
        break;
      case '8':
        vistoriaAdiantado += 1;
        break;
      case '9':
        chavesAdiantado += 1;
        break;
      case '10':
          manutencaoAdiantado += 1;
          break;
      case '11':
          retornoAdiantado += 1;
          break;
      default:
        console.log('Sem status processo');
    }
  }
  
  function atualizarMae(id_locacao, id_status, id_tarefa, porcento){
    switch(id_status){
      case '1':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusNegociacao" + id_locacao ).html(`Negociação: ${porcento}% <br>`)
        } else {
          $("#statusNegociacao" + id_locacao ).html(`Negociação: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '2':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusContrato" + id_locacao ).html(`Contrato: ${porcento}% <br>`)
        } else {
          $("#statusContrato" + id_locacao ).html(`Contrato: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '3':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusEnergia" + id_locacao ).html(`Ligação de Energia: ${porcento}% <br>`)
        } else {
          $("#statusEnergia" + id_locacao ).html(`Ligação de Energia: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '4':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusOrcar" + id_locacao ).html(`Orçar: ${porcento}% <br>`)
        } else {
          $("#statusOrcar" + id_locacao ).html(`Orçar: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '5':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusPagar" + id_locacao ).html(`Pagar: ${porcento}% <br>`)
        } else {
          $("#statusPagar" + id_locacao ).html(`Pagar: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;        
      case '6':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusInstalar" + id_locacao ).html(`Instalar: ${porcento}% <br>`)
        } else {
          $("#statusInstalar" + id_locacao ).html(`Instalar: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '7':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusLimpar" + id_locacao ).html(`Limpar: ${porcento}% <br>`)
        } else {
          $("#statusLimpar" + id_locacao ).html(`Limpar: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '8':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusVistoria" + id_locacao ).html(`Vistoria Final: ${porcento}% <br>`)
        } else {
          $("#statusVistoria" + id_locacao ).html(`Vistoria Final: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '9':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusChaves" + id_locacao ).html(`Entrega de Chaves: ${porcento}% <br>`)
        } else {
          $("#statusChaves" + id_locacao ).html(`Entrega de Chaves: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '10':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusManutencao" + id_locacao ).html(`Manutenção: ${porcento}% <br>`)
        } else {
          $("#statusManutencao" + id_locacao ).html(`Manutenção: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '11':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusRetorno" + id_locacao ).html(`Retorno: ${porcento}% <br>`)
        } else {
          $("#statusRetorno" + id_locacao ).html(`Retorno: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
    }
  }
});

function capturaId(){
  tarefa_id = $('.selecionada').attr("id");
}

function ignoraSelecao(){
  $('.tarefa').removeClass('selecionada');
  $('.tarefa').css("background-color","rgb(255, 255, 255)");
}

var verificarBlocos = $("#listaBloco").html();
var verificarUnidades = $("#listaUnidade").html();


var optionBloco = `<option>Bloco</option>`;
var optionUnidade = `<option>Unidade</option>`;

var selecionadosBlocos = $("#selecionadosBloco").html();
var selecionadosUnidades = $("#selecionadosUnidade").html();


qtdBlocos = verificarBlocos.split(",");
qtdUnidades = verificarUnidades.split(",");

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