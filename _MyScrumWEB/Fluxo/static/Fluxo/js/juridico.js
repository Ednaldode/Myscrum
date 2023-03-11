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

  let contadorMae = 0, contadorPrincipal = 0, contadorDefesa = 0, contadorReplica = 0, contadorAudiencia = 0, contadorFinais = 0, contadorSentenca = 0, contadorRecurso2 = 0, contadorRecurso3 = 0;
  let maeAdiantado = 0, maeAtencao = 0, maeAtrasado = 0, principalAdiantado = 0, principalAtencao = 0, principalAtrasado = 0, defesaAdiantado = 0, defesaAtencao = 0, defesaAtrasado = 0, replicaAdiantado = 0, replicaAtencao = 0, replicaAtrasado = 0, audienciaAdiantado = 0,
      audienciaAtencao = 0, audienciaAtrasado = 0, finaisAdiantado = 0, finaisAtencao = 0, finaisAtrasado = 0, sentencaAdiantado = 0, sentencaAtencao = 0, sentencaAtrasado = 0, recurso2Adiantado = 0, recurso2Atencao = 0, recurso2Atrasado = 0,
      recurso3Adiantado = 0, recurso3Atencao = 0, recurso3Atrasado = 0, feito = 0;
  
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
    if ($('#statusProcesso' + $(valor).attr('id')).text() == 1 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorMae += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 2 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorPrincipal += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 3 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorDefesa += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 4 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorReplica += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 5 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorAudiencia += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 6 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorFinais += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 7 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorSentenca += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 8 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorRecurso2 += 1;
    } else if ($('#statusProcesso' + $(valor).attr('id')).text() == 9 && $('#stat' + $(valor).attr('id')).text() != "Feito"){
      contadorRecurso3 += 1;
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

  $(".titulos").html(`
    <span title="Processo Judicial" class="titulo-child afazer">
      <span title="Adiantados: ${maeAdiantado}\nAvisos: ${maeAtencao}\nAtrasados: ${maeAtrasado}">Mãe | ${contadorMae}</span>
    </span>

    <span title="Autor expõe os fatos que o levaram a entrar com a ação, bem como quais\n dos seus direitos foram violados, e o seu pedido." class="titulo-child afazer">
      <span title="Adiantados: ${principalAdiantado}\nAvisos: ${principalAtencao}\nAtrasados: ${principalAtrasado}">Petição Inicial | ${contadorPrincipal}</span>
    </span>
      
    <span title="Nela, o réu pode alegar várias matérias para se defender." class="titulo-child fazendo">
      <span title="Adiantados: ${defesaAdiantado}\nAvisos: ${defesaAtencao}\nAtrasados: ${defesaAtrasado}">Defesa | ${contadorDefesa}</span>
    </span>

    <span title="Esse é o nome da manifestação por meio do qual o autor contrapõe\nos argumentos que o réu alegou em sua contestação." class="titulo-child feito">
      <span title="Adiantados: ${replicaAdiantado}\nAvisos: ${replicaAtencao}\nAtrasados: ${replicaAtrasado}">Réplica | ${contadorReplica}</span>
    </span>

    <span title="Nesse momento, o juiz convoca as partes para que indiquem\nquais provas pretendem produzir para corroborara sua versão\ndos fatos." class="titulo-child afazer">
      <span title="Adiantados: ${audienciaAdiantado}\nAvisos: ${audienciaAtencao}\nAtrasados: ${audienciaAtrasado}">Audiência | ${contadorAudiencia}</span>
    </span>
    
    <span title="Depois que todas as provas foram devidamente autorizadas, produzidas e juntadas no processo, o juiz chamará \nas partes para, em última chance, argumentarem sobre elas. Essa será a última vez que elas poderão se manifestar\nno processo antes da sentença." class="titulo-child afazer">
     <span title="Adiantados: ${finaisAdiantado}\nAvisos: ${finaisAtencao}\nAtrasados: ${finaisAtrasado}">Alegações Finais | ${contadorFinais}</span>
    </span>

    <span title="É nesse ato que, depois de analisar todos os argumentos e provas, o juiz toma\na sua decisão final." class="titulo-child afazer>
      <span title="Adiantados: ${sentencaAdiantado}\nAvisos: ${sentencaAtencao}\nAtrasados: ${sentencaAtrasado}">Sentença | ${contadorSentenca}</span>
    </span>

    <span title="Ainda que a sentença seja a decisão final do juiz, ainda é possível recorrer\ncontra essa decisão." class="titulo-child afazer">
      <span title="Adiantados: ${recurso2Adiantado}\nAvisos: ${recurso2Atencao}\nAtrasados: ${recurso2Atrasado}">Recurso 2ª Instância | ${contadorRecurso2}</span>
    </span>

    <span title="Ainda que a sentença seja a decisão final do juiz, ainda é possível recorrer\ncontra essa decisão." class="titulo-child feito">
      <span title="Adiantados: ${recurso3Adiantado}\nAvisos: ${recurso3Atencao}\nAtrasados: ${recurso3Atrasado}">Recurso 3ª Instância | ${contadorRecurso3}</span>
    </span>

    <span title="Fim do Processo" class="titulo-child afazer">
      <span title="Finalizados: ${feito}">Feito | ${feito}</span>
    </span>
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
        principalAtrasado += 1;
        break;
      case '2':
        defesaAtrasado += 1;
        break;
      case '3':
        replicaAtrasado += 1;
        break;
      case '4':
        audienciaAtrasado += 1;
        break;
      case '5':
        finaisAtrasado += 1;
        break;
      case '6':
        sentencaAtrasado += 1;
        break;
      case '7':
        recurso2Atrasado += 1;
        break;
      case '8':
        recurso3Atrasado += 1;
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
        principalAtencao += 1;
        break;
      case '2':
        defesaAtencao += 1;
        break;
      case '3':
        replicaAtencao += 1;
        break;
      case '4':
        audienciaAtencao += 1;
        break;
      case '5':
        finaisAtencao += 1;
        break;
      case '6':
        sentencaAtencao += 1;
        break;
      case '7':
        recurso2Atencao += 1;
        break;
      case '8':
        recurso3Atencao += 1;
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
        principalAdiantado += 1;
        break;
      case '2':
        defesaAdiantado += 1;
        break;
      case '3':
        replicaAdiantado += 1;
        break;
      case '4':
        audienciaAdiantado += 1;
        break;
      case '5':
        finaisAdiantado += 1;
        break;
      case '6':
        sentencaAdiantado += 1;
        break;
      case '7':
        recurso2Adiantado += 1;
        break;
      case '8':
        recurso3Adiantado += 1;
        break;
      default:
        console.log('Sem status processo');
    }
  }
  
  function atualizarMae(id_locacao, id_status, id_tarefa, porcento){
    switch(id_status){
      case '2':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusPeticao" + id_locacao ).html(`Petição Inicial: ${porcento}% <br>`)
        } else {
          $("#statusPeticao" + id_locacao ).html(`Petição Inicial: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '3':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusDefesa" + id_locacao ).html(`Defesa: ${porcento}% <br>`)
        } else {
          $("#statusDefesa" + id_locacao ).html(`Defesa: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '4':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusReplica" + id_locacao ).html(`Réplica: ${porcento}% <br>`)
        } else {
          $("#statusReplica" + id_locacao ).html(`Réplica: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '5':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusAudiencia" + id_locacao ).html(`Audiência: ${porcento}% <br>`)
        } else {
          $("#statusAudiencia" + id_locacao ).html(`Audiência: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '6':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusFinais" + id_locacao ).html(`Finais: ${porcento}% <br>`)
        } else {
          $("#statusFinais" + id_locacao ).html(`Finais: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '7':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusSentenca" + id_locacao ).html(`Sentença: ${porcento}% <br>`)
        } else {
          $("#statusSentenca" + id_locacao ).html(`Sentença: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;        
      case '8':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusRecurso2" + id_locacao ).html(`Recurso 2: ${porcento}% <br>`)
        } else {
          $("#statusRecurso2" + id_locacao ).html(`Recurso 2: <i class="fas fa-check" style="color: green"></i> <br>`)
        }
        break;
      case '9':
        if($("#stat" + id_tarefa).text() == "A fazer" || $("#stat" + id_tarefa).text() == "Fazendo"){
          $("#statusRecurso3" + id_locacao ).html(`Recurso 3: ${porcento}% <br>`)
        } else {
          $("#statusRecurso3" + id_locacao ).html(`Recurso 3: <i class="fas fa-check" style="color: green"></i> <br>`)
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