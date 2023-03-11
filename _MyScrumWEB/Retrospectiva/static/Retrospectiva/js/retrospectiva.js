// (function(a,b){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r|s)|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-|)|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))window.location=b})(navigator.userAgent||navigator.vendor||window.opera,"m_kanban");
var tarefa_id;
$("#loader").show();
$(function(){

  //Buscando cards do kanban
  var teste = $('.tarefa');

  //Criando variáveis para armazenamento de quantidade de tarefas (A Fazer(Atrasada e Aviso), Fazendo(Adiantada, Atrasada e Aviso) e Feito(Finalizada))
  let foiBom = 0;
  let podeMelhorar = 0;
  let deveMelhorar = 0;

  //Percorrendo cada tarefa criada no kanban
  //indice = id / valor = conteúdo
  $.each(teste, function(indice, valor){
    //Buscando dados no código
    let status = $('#retrospec' + $(valor).attr('id')).text();

    //Verificando status das tarefas e adicionando cores de fundo
    if (status == 'Foi bom'){ //Foi bom
      //Incrementando variável com quantidade de tarefas
      foiBom += 1;
    } else if (status == 'Pode melhorar'){ //Pode melhorar
      //Incrementando variável com quantidade de tarefas
      podeMelhorar += 1;

    } else if (status == 'Deve melhorar'){ //Deve melhorar
      //Incrementando variável com quantidade de tarefas
      deveMelhorar += 1;
    } else { //Igual a 0
      console.log("Não há retrospectiva");
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

    //Adicionando imagem de Responsável e autoridade
    let pessoaResponsavel = $("#id_responsavel" + $(valor).attr('id')).attr('title');
    $("#imgIdResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaResponsavel + "/perfil/" + pessoaResponsavel + ".png").on("error", function(){
      $("#imgIdResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
    });
    $("#id_responsavel" + $(valor).attr('id')).prop('title', 'Responsável Retrospectiva: ' + pessoaResponsavel);
    pessoaResponsavel = $("#responsavel" + $(valor).attr('id')).attr('title');
    $("#imgResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaResponsavel + "/perfil/" + pessoaResponsavel + ".png").on("error", function(){
      $("#imgResponsavel" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
    });
    $("#responsavel" + $(valor).attr('id')).prop('title', 'Responsável Tarefa: ' + pessoaResponsavel);
    let pessoaAutoridade = $("#autoridade"  + $(valor).attr('id')).attr('title');
    $("#imgAutoridade" + $(valor).attr('id')).attr("src", "../media/usuarios/" + pessoaAutoridade + "/perfil/" + pessoaAutoridade + ".png").on("error", function(){
      $("#imgAutoridade" + $(valor).attr('id')).attr("src", "../media/usuarios/Padrão/perfil/Padrão.png");
    });
    $("#autoridade" + $(valor).attr('id')).prop('title', 'Autoridade: ' + pessoaAutoridade);
  });

  //Adicionando quantidade de tarefas em cada coluna
  $(".titulos").html(`
    <span title="Foi Bom: ${foiBom}" class="titulo-child afazer">Foi bom | ${foiBom}</span>
    <span title="Pode melhorar: ${podeMelhorar}" class="titulo-child fazendo">Pode melhorar | ${podeMelhorar}</span>
    <span title="Deve melhorar: ${deveMelhorar}" class="titulo-child feito">Deve melhorar | ${deveMelhorar}</span>`);

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
    localStorage.controller1 = 3;
  });
});

function capturaId(){
  tarefa_id = $('.selecionada').attr("id");
}

function ignoraSelecao(){
  $('.tarefa').removeClass('selecionada');
  $('.tarefa').css("background-color","rgb(255, 255, 255)");
}
