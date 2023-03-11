$(function(){
    function removerClasses(){
        $("#fTarefa").removeClass("ativado");
        $("#fTarefa").removeClass("desativado");
        $("#fAnexo").removeClass("ativado");
        $("#fAnexo").removeClass("desativado");
        $("#fRetrospectiva").removeClass("ativado");
        $("#fRetrospectiva").removeClass("desativado");
        $("#f5w2h").removeClass("ativado");
        $("#f5w2h").removeClass("desativado");
    }
    function verificarController(){
    if (controller == 1){
        removerClasses();
        $("#fTarefa").addClass("ativado");
        $("#fAnexo").addClass("desativado");
        $("#fRetrospectiva").addClass("desativado");
        $("#f5w2h").addClass("desativado");
    } else if (controller == 2) {
        removerClasses();
        $("#fTarefa").addClass("desativado");
        $("#fAnexo").addClass("ativado");
        $("#fRetrospectiva").addClass("desativado");
        $("#f5w2h").addClass("desativado");
    } else if (controller == 3) {
        removerClasses();
        $("#fTarefa").addClass("desativado");
        $("#fAnexo").addClass("desativado");
        $("#fRetrospectiva").addClass("ativado");
        $("#f5w2h").addClass("desativado");
    } else if (controller == 4) {
        removerClasses();
        $("#fTarefa").addClass("desativado");
        $("#fAnexo").addClass("desativado");
        $("#fRetrospectiva").addClass("desativado");
        $("#f5w2h").addClass("ativado");
    } else {
        console.log("Controller incorreto.")
    }
    }
    
    let controller;
    if(localStorage.getItem("controller1") == 4){
    controller = 4;
    } else if (localStorage.getItem("controller1") == 3){
    controller = 3;
    } else if (localStorage.getItem("controller1") == 2){
    controller = 2;
    } else if (localStorage.getItem("controller1") == 1){
    controller = 1;
    } else {
    controller = 1;
    }
    
    localStorage.removeItem("controller1");
    verificarController();

    let retrospectiva = $("#id_retrospec").val();
    
    $(".anterior").click(function(){
        if (controller == 1){
            controller = 3;
        } else {
            controller -= 1;
            // if($("#id_5w2h").val() == "--------"){
            //   controller -= 1;
            // }
        }
        if(retrospectiva == 0 && controller == 3){
            controller -= 1;
        }
        verificarController();
    });
    
    $(".proximo").click(function(){
        if (controller == 3){
            controller = 1;
        } else {
            controller += 1;
            // if($("#id_5w2h").val() == "--------"){
            //   controller += 1;
            // }
        }
        if(retrospectiva == 0 && controller == 3){
            controller = 1;
        }
        verificarController();
    });

    if ($("#rNome").html() == ""){
        $("#rAtualizacao").hide();
    }

    $("#mFinalizar").click(function(){
        localStorage.controller1 = 3;
    });
});