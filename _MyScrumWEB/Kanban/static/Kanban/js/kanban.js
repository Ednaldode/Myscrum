// (function(a,b){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r|s)|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-|)|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))window.location=b})(navigator.userAgent||navigator.vendor||window.opera,"m_kanban");
var tarefa_id;
$("#loader").show();
$(function(){

  //Buscando cards do kanban
  var teste = $('.tarefa');

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

  //Criando variáveis para armazenamento de quantidade de tarefas (A Fazer(Atrasada e Aviso), Fazendo(Adiantada, Atrasada e Aviso) e Feito(Finalizada))
  let aFazerAtrasada = 0;
  let aFazerAviso = 0;
  let fazendoAdiantada = 0;
  let fazendoAtrasada = 0;
  let fazendoAviso = 0;
  let feitoFinalizada = 0;

  //Percorrendo cada tarefa criada no kanban
  //indice = id / valor = conteúdo
  $.each(teste, function(indice, valor){
    //Buscando dados no código
    let dataInicial = $('#dataInicial' + $(valor).attr('id')).text();
    let dataFinal = $('#dataFinal' + $(valor).attr('id')).text();
    let status = $('#status' + $(valor).attr('id')).text();
    let statusPrazo = $('#statusPrazo' + $(valor).attr('id')).text();

    //Formatando data para jQuery
    let formatarInicial = dataInicial.split('/');
    let formatarFinal= dataFinal.split('/');

    //Colocando data formatada no Date()
    let inicial = new Date(formatarInicial[2] + '-' + formatarInicial[1] + '-' + formatarInicial[0]);
    let final = new Date(formatarFinal[2] + '-' + formatarFinal[1] + '-' + formatarFinal[0]);

    let id = $(valor).attr('id');
    let prazo = $('#prazo' + $(valor).attr('id')).text();
    let porcentagem = $(".progress-bar" + $(valor).attr('id')).attr('aria-valuenow');

    let realizado = porcentagem;
    let previsto

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

    // Verificando se tarefa é mãe/filho
    if($("#is_mae_filho" + $(valor).attr('id')).html() == 0 || ($("#is_mae_filho" + $(valor).attr('id')).html() == 1 && $("#processo" + $(valor).attr('id')).html() == 'Processo Cível')){
      $("#is_mae_filho" + $(valor).attr('id')).attr('title', 'Tarefa Mãe').html(`<i class="fas fa-female" style="color: pink;"></i>`).show()
    } else if ($("#is_mae_filho" + $(valor).attr('id')).html() > 0){
      $("#is_mae_filho" + $(valor).attr('id')).attr('title', 'Tarefa Filho').html(`<i class="fas fa-baby" style="color: #cecece;"></i>`).show()
      if($("#is_id_filho" + $(valor).attr('id')).html() > 0){
        let id_filho = $("#is_id_filho" + $(valor).attr('id')).html();
        $("#statusFilhos" + id_filho).html($("#statusFilhos" + id_filho).html() + `
          <span>${$("#descricao" + $(valor).attr('id')).html()}: ${
            status == 'Feito' ? 
              `<i class="fas fa-check" style="color: green"></i>`
            :
              porcentagem != undefined ? 
                `${porcentagem}%`
              :
                `0%`
            }
          </span>
        `);
      } else if($("#is_id_juridico" + $(valor).attr('id')).html() > 0) {
        let id_filho = $("#is_id_juridico" + $(valor).attr('id')).html();
        let status = $("#descricao" + $(valor).attr('id')).html().split(':')
        $("#statusFilhos" + id_filho).html($("#statusFilhos" + id_filho).html() + `
          <span>${status[0]}: ${
            status == 'Feito' ? 
              `<i class="fas fa-check" style="color: green"></i>`
            :
              porcentagem != undefined ? 
                `${porcentagem}%`
              :
                `0%`
            }
          </span>
        `);
      } else if($("#is_id_locacao" + $(valor).attr('id')).html() > 0) {
        let id_filho = $("#is_id_locacao" + $(valor).attr('id')).html();
        let status = $("#descricao" + $(valor).attr('id')).html().split(':')
        $("#statusFilhos" + id_filho).html($("#statusFilhos" + id_filho).html() + `
          <span>${status[0]}: ${
            status == 'Feito' ? 
              `<i class="fas fa-check" style="color: green"></i>`
            :
              porcentagem != undefined ? 
                `${porcentagem}%`
              :
                `0%`
            }
          </span>
        `);
      }
    }

    //Verificando status das tarefas e adicionando cores de fundo
    if (status == 'Feito'){ //Feito
      //Adicionando fundo cinza para tarefas finalizadas
      $(valor).toggleClass('finalizada');

      //Incrementando variável com quantidade de tarefas
      feitoFinalizada += 1;

      //Calculando status do prazo / finalizada hoje ou x dias
      if (dataAtual.getTime() == final.getTime()){
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada:" aria-label="100%"> <div style="display: none;"> <span id="finalizada' + $(valor).attr('id') + '">0</span> </div> Hoje </span>');
      } else if ((dataAtual.getTime() - final.getTime()) / 86400000 == 1) {
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"> <span id="finalizada' + $(valor).attr('id') + '">1</span> dia</span>');
      } else{
        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Finalizada há:" aria-label="100%"><span id="finalizada' + $(valor).attr('id') + '">' + (dataAtual.getTime() - final.getTime()) / 86400000 + '</span> dias </span>');
      }

    } else if (status == 'A fazer' || status == 'A Fazer'){ //A fazer
      if (inicial.getTime() >= dataAtual.getTime()){
        //Adicionando fundo amarelo para tarefas
        $(valor).toggleClass('aviso');

        //Incrementando variável com quantidade de tarefas
        aFazerAviso += 1;
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
        aFazerAtrasada += 1;

        $('#statusPrazo' + $(valor).attr('id')).toggleClass('text-danger')
        realizado = 0;

        $('#statusPrazo' + $(valor).attr('id')).html('<span title="Atrasada em:" aria-label="100%"> ↓ <span id="atrasada' + $(valor).attr('id') + '">' + (previsto - realizado).toFixed(2) + '</span> % - <span>' + ((dataAtual.getTime() - inicial.getTime()) / 86400000 + 1) + '</span> dias</span>');


      }
    } else { //Fazendo
      if (realizado > previsto){
        //Adicionando fundo verde para tarefas
        $(valor).toggleClass('adiantada');

        //Incrementando variável com quantidade de tarefas
        fazendoAdiantada += 1;

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
        fazendoAviso += 1;

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
        fazendoAtrasada += 1;

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
    //Verifica se há 1 ou 2 executores na tarefa

    for (let i = 0; i < executor.length; i++){
       if (i <= 1){
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs p-icone executor mr-1" title="Executor: ' + executor[i] +'"><img id="imgExecutor' + $(valor).attr('id') + i + '" class="rounded-circle" style="width: 100%; height: 100%"></span>');
         $("#imgExecutor" + $(valor).attr('id') + i).attr("src", "../media/usuarios/" + executor[i] + "/perfil/" + executor[i] + ".png").on("error", function(){
           $("#imgExecutor" + $(valor).attr('id') + i).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
         });
       }
     }

    if (executor.length > 2){
       if ((parseInt(executor.length) - 2) == 1){
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 2) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 3) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 4) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 5) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 6) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 7) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\nExecutor: " + executor[8] + "\n" + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else if ((parseInt(executor.length) - 2) == 8) {
         $("#imagensExecutores" + $(valor).attr('id')).html($("#imagensExecutores" + $(valor).attr('id')).html() + " " + '<span class="col-xs align-self-center maisExecutores" title="Executor: ' + executor[2] + "\nExecutor: " + executor[3] + "\nExecutor: " + executor[4] + "\nExecutor: " + executor[5] + "\nExecutor: " + executor[6] + "\nExecutor: " + executor[7] + "\nExecutor: " + executor[8] + "\nExecutor: " + executor[9] + '" style="font-size: 12px;">+' + (parseInt(executor.length) - 2) + '</span>');
       } else {
       $("#imagensExecutores" + $(valor).attr('id')).html("Executores inválidos");
     }
     }

    // Adicionando peso ao tamanho
    let tamanho = $("#peso" + $(valor).attr('id')).text();
    let peso;
    if (tamanho == "Baby"){
      peso = "0.33"
    } else if (tamanho == "PP"){
      peso = "1"
    } else if (tamanho == "P"){
      peso = "3"
    } else if (tamanho == "M"){
      peso = "5"
    } else if (tamanho == "G"){
      peso = "8"
    } else if (tamanho == "GG"){
      peso = "13"
    } else if (tamanho == "EG"){
      peso = "21"
    } else if (tamanho == "Gigante"){
      peso = "34"
    } else if (tamanho == "Gigante 1"){
      peso = "55"
    } else if (tamanho == "Gigante 2"){
      peso = "89"
    } else if (tamanho == "Gigante 3"){
      peso = "144"
    } else if (tamanho == "Gigante 4"){
      peso = "233"
    } else {
      peso = "377"
    }
    $("#peso" + $(valor).attr('id')).text(tamanho + ' - ' + peso)

    //Adicionando imagem de Responsável e autoridade
    let pessoaResponsavel = $("#responsavel" + $(valor).attr('id')).attr('title');
    $("#imgResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaResponsavel + "/perfil/" + pessoaResponsavel + ".png").on("error", function(){
      $("#imgResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
    });
    $("#responsavel" + $(valor).attr('id')).prop('title', 'Responsável: ' + pessoaResponsavel);

    let pessoaAutoridade = $("#autoridade"  + $(valor).attr('id')).attr('title');
    $("#imgAutoridade" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaAutoridade + "/perfil/" + pessoaAutoridade + ".png").on("error", function(){
      $("#imgAutoridade" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
    });
    $("#autoridade" + $(valor).attr('id')).prop('title', 'Autoridade: ' + pessoaAutoridade);

    //Removendo circulo/imagem de pendencia se não houver
    let pessoaImpedimento = $("#impedimento" + $(valor).attr('id')).attr('title');
    $("#impedimento" + $(valor).attr('id')).prop('title', 'Impedimento: ' + pessoaImpedimento);
    if (pessoaImpedimento == '' || pessoaImpedimento == 'None'){
      $("#impedimento" + $(valor).attr('id')).hide();
    } else {
        $("#imgImpedimento" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaImpedimento + "/perfil/" + pessoaImpedimento + ".png").on("error", function(){
          $("#imgImpedimento" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
        });
    }

    //Removendo ícone de anexo se não houver
    let anexo1 = $("#anexo1" + $(valor).attr('id')).text();
    if (anexo1 == '' || anexo1 == 'None'){
      $("#anexo" + $(valor).attr('id')).hide();
    }

    //Removendo ícone de Retrospectiva se não houver
    let retrospectiva1 = $("#retrospectiva1" + $(valor).attr('id')).text();
    if (retrospectiva1 == '' || retrospectiva1 == 'None' || retrospectiva1 == '0'){
      $("#retrospectiva" + $(valor).attr('id')).hide();
    }

    //Removendo ícone de 5w2h se não houver
    let r5w2h1 = $("#r5w2h1" + $(valor).attr('id')).text();
    if (r5w2h1 == 'None' || r5w2h1 == '0'){
      $("#r5w2h" + $(valor).attr('id')).hide();
    }
  });

  //Adicionando quantidade de tarefas em cada coluna
  $(".titulos").html(`
    <span title="Atrasada(s): ${aFazerAtrasada}\nAtenção: ${aFazerAviso}" class="titulo-child afazer">A fazer | ${aFazerAtrasada + aFazerAviso}</span>
    <span title="Adiantada(s): ${fazendoAdiantada}\nAtrasada(s): ${fazendoAtrasada}\nAtenção: ${fazendoAviso}" class="titulo-child fazendo">Fazendo | ${fazendoAdiantada + fazendoAtrasada + fazendoAviso}</span>
    <span title="Finalizada(s): ${feitoFinalizada}" class="titulo-child feito">Feito | ${feitoFinalizada}</span>`);

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
    // $("#"+tarefa_id+"_modal").modal();
  });
});

function capturaId(){
  tarefa_id = $('.selecionada').attr("id");
}

function ignoraSelecao(){
  $('.tarefa').removeClass('selecionada');
  $('.tarefa').css("background-color","rgb(255, 255, 255)");
}
