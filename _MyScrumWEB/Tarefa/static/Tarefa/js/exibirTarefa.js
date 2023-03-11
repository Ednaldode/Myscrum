$(function(){
    function removerClasses(){
        $("#fTarefa").removeClass("ativado");
        $("#fTarefa").removeClass("desativado");
        $("#trocarTarefa").css("text-decoration", "underline");
        $("#trocarTarefa").css("text-decoration", "none");
        $("#fAnexo").removeClass("ativado");
        $("#fAnexo").removeClass("desativado");
        $("#trocarAnexo").css("text-decoration", "underline");
        $("#trocarAnexo").css("text-decoration", "none");
        $("#fFilho").removeClass("ativado");
        $("#fFilho").removeClass("desativado");
        $("#trocarFilho").css("text-decoration", "underline");
        $("#trocarFilho").css("text-decoration", "none");
        $("#fRetrospectiva").removeClass("ativado");
        $("#fRetrospectiva").removeClass("desativado");
        $("#trocarRetrospectiva").css("text-decoration", "underline");
        $("#trocarRetrospectiva").css("text-decoration", "none");
        $("#f5w2h").removeClass("ativado");
        $("#f5w2h").removeClass("desativado");
        $("#trocar5w2h").css("text-decoration", "underline");
        $("#trocar5w2h").css("text-decoration", "none");
        $("#sat").removeClass("ativado");
        $("#sat").removeClass("desativado");
        $("#trocarSat").css("text-decoration", "underline");
        $("#trocarSat").css("text-decoration", "none");
        $("#locacao").removeClass("ativado");
        $("#locacao").removeClass("desativado");
        $("#trocarLocacao").css("text-decoration", "underline");
        $("#trocarLocacao").css("text-decoration", "none");
        $("#fMedicaoTerceiros").removeClass("ativado");
        $("#fMedicaoTerceiros").removeClass("desativado");
        $("#trocarMedicaoTerceiros").css("text-decoration", "underline");
        $("#trocarMedicaoTerceiros").css("text-decoration", "none");
        $("#juridico").removeClass("ativado");
        $("#juridico").removeClass("desativado");
        $("#trocarJuridico").css("text-decoration", "underline");
        $("#trocarJuridico").css("text-decoration", "none");
        $("#historicoJuridico").removeClass("ativado");
        $("#historicoJuridico").removeClass("desativado");
        $("#trocarHistorico").css("text-decoration", "underline");
        $("#trocarHistorico").css("text-decoration", "none");
    }
    function verificarController(){
        if (controller == 1){
            removerClasses();
            $("#fTarefa").addClass("ativado");
            $("#trocarTarefa").css("text-decoration", "underline");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 2) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("ativado");
            $("#fFilho").addClass("desativado");
            $("#trocarAnexo").css("text-decoration", "underline");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 3) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("ativado");
            $("#trocarRetrospectiva").css("text-decoration", "underline");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 4) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("ativado");
            $("#trocar5w2h").css("text-decortion", "underline");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 5) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("ativado");
            $("#trocarSat").css("text-decoration", "underline");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 6) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("ativado");
            $("#trocarLocacao").css("text-decoration", "underline");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 7) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("ativado");
            $("#trocarMedicaoTerceiros").css("text-decoration", "underline");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 8) {
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("ativado");
            $("#trocarJuridico").css("text-decoration", "underline");
            $("#historicoJuridico").addClass("desativado");
        } else if (controller == 9){
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fFilho").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("ativado");
            $("#trocarHistorico").css("text-decoration", "underline");
        } else if (controller == 10){
            removerClasses();
            $("#fTarefa").addClass("desativado");
            $("#fAnexo").addClass("desativado");
            $("#fRetrospectiva").addClass("desativado");
            $("#f5w2h").addClass("desativado");
            $("#sat").addClass("desativado");
            $("#locacao").addClass("desativado");
            $("#fMedicaoTerceiros").addClass("desativado");
            $("#juridico").addClass("desativado");
            $("#historicoJuridico").addClass("ativado");
            $("#fFilho").addClass("ativado");
            $("#trocarFilho").css("text-decoration", "underline");
        } else {
            console.log("Controller incorreto.");
        }
        ControlFinalizar();
    }
    
    let controller;
    
    if (localStorage.getItem("controller1") == 10){
        controller = 10;
    } else if (localStorage.getItem("controller1") == 9){
        controller = 9;
    } else if (localStorage.getItem("controller1") == 8){
        controller = 8;
    } else if (localStorage.getItem("controller1") == 7){
        controller = 7;
    } else if (localStorage.getItem("controller1") == 6){
        controller = 6;
    } else if (localStorage.getItem("controller1") == 5){
        controller = 5;
    } else if (localStorage.getItem("controller1") == 4){
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
    
    $("#trocarTarefa").click(function(){
        controller = 1;
        verificarController();
    });

    $("#trocarAnexo").click(function(){
        controller = 2;
        verificarController();
    });
    
    $("#trocarFilho").click(function(){
        controller = 10;
        verificarController();
    });

    $("#trocarRetrospectiva").click(function(){
        controller = 3;
        verificarController();
    });

    $("#trocar5w2h").click(function(){
        controller = 4;
        verificarController();
    });

    $("#trocarSat").click(function(){
        controller = 5;
        verificarController();
    });

    $("#trocarLocacao").click(function(){
        controller = 6;
        verificarController();
    });

    $("#trocarMedicaoTerceiros").click(function(){
        controller = 7;
        verificarController();
    });
    
    $("#trocarJuridico").click(function(){
        controller = 8;
        verificarController();
    });

    $("#trocarHistorico").click(function(){
        controller = 9;
        verificarController();
    });

    if ($("#id_retrospec").val() == 0){
        $("#trocarRetrospectiva").hide();
        $("#barraRetrospectiva").hide();
    } else {
        $("#trocarRetrospectiva").show();
        $("#barraRetrospectiva").show();
    }

    if($("#id_id_status").val() == 0 && $("#id_id_filho").val() == $("#id_tarefa").val()){
        $("#trocarFilho").show();
        $("#barraFilho").show();
    } else{
        $("#trocarFilho").hide();
        $("#barraFilho").hide();
    };

    if($("#id_id_status").val() == 1 && $("#id_id_filho").val() > 0){
        $("#trocarMae").show();
        $("#barraMae").show();
    } else{
        $("#trocarMae").hide();
        $("#barraMae").hide();
    };

    $("#id_retrospec")

    if ($("#id_r5w2hT").val() == 0){
        $("#trocar5w2h").hide();
        $("#barra5w2h").hide();
    } else {
        $("#trocar5w2h").show();
        $("#barra5w2h").show();
    }

    $("#id_r5w2hT").change(function(){
        if ($("#id_r5w2hT").val() == 0){
            $("#trocar5w2h").hide();
            $("#barra5w2h").hide();
        } else {
            $("#trocar5w2h").show();
            $("#barra5w2h").show();
        }
    });

    optionDuracaoPadrao = `
    <option value="0">0</option>
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="5">5</option>
    <option value="8">8</option>
    <option value="13">13</option>
    <option value="21">21</option>
    <option value="34">34</option>
    <option value="55">55</option>
    <option value="89">89</option>
    <option value="144">144</option>
    <option value="233">233</option>
    <option value="377">377</option>
    <option value="610">610</option>
    <option value="987">987</option>
    `
    optionDuracaoSAT = `
    <option value="0">0</option>
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="5">5</option>
    <option value="8">8</option>
    <option value="13">13</option>
    <option value="21">21</option>
    <option value="30">30</option>
    <option value="34">34</option>
    <option value="55">55</option>
    <option value="89">89</option>
    <option value="144">144</option>
    <option value="233">233</option>
    <option value="377">377</option>
    <option value="610">610</option>
    <option value="987">987</option>
    `
    // Processo:  75 - Solicitação Assistência Técnica
    // Processo:  51 - Conservação / Limpeza
    // Processo:  63 - Atendimento Locação
    // Processo:  23 - Medição terceiros
    // Processo: 146 - Retorno de Locação
    // Processo:  29 - Processo Cível
    if ($("#id_processo_relacionado").val() != 75 && $("#id_processo_relacionado").val() != 51){
        $("#trocarSat").hide();
        $("#barraSat").hide();
        $("#impressao").hide();
        $("#id_prazo").html(optionDuracaoPadrao).val($("#prazoTarefa").text());

        executores();
    } else if($("#id_processo_relacionado").val() == 75){
        $("#trocarSat").show();
        $("#barraSat").show();
        $("#impressao").show();
        $("#id_prazo").html(optionDuracaoSAT).val(30);
        $("#executoresSat").html($("#executoresTarefa").html());
        $("#executoresTarefa").html("");
        $('#id_status_processo').val($("#statusprocessoTarefa").text())
        requeridosSAT();
        executores();
    } else {
        $("#trocarSat").show();
        $("#barraSat").show();
        $("#impressao").show();
        $("#id_prazo").html(optionDuracaoSAT).val($("#prazoTarefa").text());
        $("#executoresSat").html($("#executoresTarefa").html());
        $("#executoresTarefa").html("");
        $('#id_status_processo').val($("#statusprocessoTarefa").text())
        executores();
        $("#id_status_processo").val() == "Manutenção" ? requeridosSAT() : requeridosConservacao();
    }

    $("#id_processo_relacionado").change(function(){
        if ($("#id_processo_relacionado").val() != 75 && $("#id_processo_relacionado").val() != 51){
            $("#trocarSat").hide();
            $("#barraSat").hide();
            $("#impressao").hide();
            if($("#id_prazo").val() != 30){
                $("#prazoTarefa").text($("#id_prazo").val());
            }
            $("#id_prazo").html(optionDuracaoPadrao).val($("#prazoTarefa").text());
            if($("#executoresTarefa").html() == ""){
                $("#executoresTarefa").html($("#executoresSat").html());
            }
            $("#executoresSat").html("");
            nrequeridosSAT()
            executores();
        } else if($("#id_processo_relacionado").val() == 75){
            $("#trocarSat").show();
            $("#barraSat").show();
            $("#impressao").show();
            $("#id_prazo").html(optionDuracaoSAT).val(30);
            $("#executoresSat").html($("#executoresTarefa").html());
            $("#executoresTarefa").html("");
            requeridosSAT();
            executores();
        } else {
            $("#trocarSat").show();
            $("#barraSat").show();
            $("#impressao").show();
            $("#id_prazo").html(optionDuracaoSAT).val($("#prazoTarefa").text());
            $("#executoresSat").html($("#executoresTarefa").html());
            $("#executoresTarefa").html("");
            executores();
            $("#id_status_processo").val() == "Manutenção" ? requeridosSAT() : requeridosConservacao();
        }
    });

    if ($("#id_processo_relacionado").val() != 63){
        $("#trocarLocacao").hide();
        $("#barraLocacao").hide();
        $("#statusLocacao").html("");
    } else {
        $("#trocarLocacao").show();
        $("#barraLocacao").show();
    }

    $("#id_processo_relacionado").change(function(){
        if ($("#id_processo_relacionado").val() != 63){
            $("#trocarLocacao").hide();
            $("#barraLocacao").hide();;
        } else {
            $("#trocarLocacao").show();
            $("#barraLocacao").show();
        }
    });

    if ($("#id_processo_relacionado").val() == 23){
        $("#medicao-terceiros").show();
        $("#trocarMedicaoTerceiros").show();
        $("#barraMedicaoTerceiros").show();
    } else{
        $("#medicao-terceiros").hide();
        $("#trocarMedicaoTerceiros").hide();
        $("#barraMedicaoTerceiros").hide();
    }

    if ($("#id_processo_relacionado").val() != 63 && $("#id_processo_relacionado").val() != 146){
        $("#trocarLocacao").hide();
        $("#barraLocacao").hide();
    } else {
        $("#trocarLocacao").show();
        $("#barraLocacao").show();
    }

    $("#id_processo_relacionado").change(function(){
        if ($("#id_processo_relacionado").val() != 63 && $("#id_processo_relacionado").val() != 146){
            $("#trocarLocacao").hide();
            $("#barraLocacao").hide();;
        } else {
            $("#trocarLocacao").show();
            $("#barraLocacao").show();
        }
    });
    
    if ($("#id_processo_relacionado").val() != 29){
        $("#trocarJuridico").hide();
        $("#barraJuridico").hide();
        $("#trocarHistorico").hide();
        $("#barraHistorico").hide();
        $("#statusJuridico").html("");
        nrequeridosJuridico();
    } else {
        $("#trocarJuridico").show();
        $("#barraJuridico").show();
        $("#trocarHistorico").show();
        $("#barraHistorico").show();
        if($("#id_status_juridico").text() == 1){
            $("#statusJuridico").css('display', 'none');
        } else{
            $("#redireciona-mae").css('display', 'block');
        }
        requeridosJuridico();
    }

    $("#id_processo_relacionado").change(function(){
        if ($("#id_processo_relacionado").val() != 29){
            $("#trocarJuridico").hide();
            $("#barraJuridico").hide();
            $("#trocarHistorico").hide();
            $("#barraHistorico").hide();
            nrequeridosJuridico();
        } else {
            $("#trocarJuridico").show();
            $("#barraJuridico").show();
            $("#trocarHistorico").show();
            $("#barraHistorico").show();
            if($("#id_status_juridico").text() == 1){
                $("#statusJuridico").css('display', 'none');
            } else{
                $("#redireciona-mae").css('display', 'block');
            }
            requeridosJuridico();
        }
    });

    $("#id_processo_relacionado").change(function(){
        if ($("#id_processo_relacionado").val() == 23){
            $("#medicao-terceiros").show();
            $("#trocarMedicaoTerceiros").show();
            $("#barraMedicaoTerceiros").show();
        } else{
            $("#medicao-terceiros").hide();
            $("#trocarMedicaoTerceiros").hide();
            $("#barraMedicaoTerceiros").hide();
        }
    });

    if ($("#id_id_medicao").val() == 0){
        $("#trocarMedicaoTerceiros").hide();
        $("#barraMedicaoTerceiros").hide();
    } else {
        $("#trocarMedicaoTerceiros").show();
        $("#barraMedicaoTerceiros").show();
    }
    
    $("#id_id_medicao").change(function(){
        if ($("#id_id_medicao").val() == 0){
            $("#trocarMedicaoTerceiros").hide();
            $("#barraMedicaoTerceiros").hide();
        } else {
            $("#trocarMedicaoTerceiros").show();
            $("#barraMedicaoTerceiros").show();
        }
    });
    
    function requeridosSAT(){
        $("#id_empreendimento").attr("required", "req");
        $("#id_bloco").attr("required", "req");        
        $("#id_unidade").attr("required", "req");
        $("#id_proprietario").attr("required", "req");
        $("#id_status_processo").attr("required", "req");
        $("#id_status_processo").val() == "" ? $("#id_status_processo").val("Análise") : $("#id_status_processo").val($("#id_status_processo").val());
        $("#id_porcentagem_sat").val() == "" ? $("#id_porcentagem_sat").val($("#id_porcentagem").val()) : $("#id_status_processo").val($("#id_status_processo").val());
        $("#id_data_abertura").val() == "" ? $("#id_data_abertura").val($("#id_data_ini").val()) : $("#id_data_abertura").val($("#id_data_abertura").val());
        $("#id_data_atendimento").val() == "" ? $("#id_data_atendimento").val($("#id_data_real").val()) : $("#id_data_atendimento").val($("#id_data_atendimento").val());
        $("#id_data_finalizacao_sat").val() == "" ? $("#id_data_finalizacao_sat").val($("#id_data_fim").val()) : $("#id_data_finalizacao_sat").val($("#id_data_finalizacao_sat").val());
        $("#id_tipo_solicitacao").attr("required", "req");
        $("#id_ambiente1").attr("required", "req");
        $("#id_descricao1").attr("required", "req");
        $("#id_reparo1").attr("required", "req");
        $("#id_procedencia1").attr("required", "req");
        $("#id_historico1").attr("required", "req");
        $("#id_estimativa_custo1").attr("required", "req");
        $("#id_duracao1").attr("required", "req");
        $("#id_material1").attr("required", "req");
    }

    function requeridosConservacao(){
        $("#id_empreendimento").attr("required", "req");
        $("#id_unidade").attr("required", "req");
        $("#id_status_processo").attr("required", "req");
        $("#id_status_processo").val() == "" ? $("#id_status_processo").val("Agendamento") : $("#id_status_processo").val($("#id_status_processo").val());
        $("#id_porcentagem_sat").val() == "" ? $("#id_porcentagem_sat").val($("#id_porcentagem").val()) : $("#id_status_processo").val($("#id_status_processo").val());
        $("#id_data_abertura").val() == "" ? $("#id_data_abertura").val($("#id_data_ini").val()) : $("#id_data_abertura").val($("#id_data_abertura").val());
        $("#id_data_atendimento").val() == "" ? $("#id_data_atendimento").val($("#id_data_real").val()) : $("#id_data_atendimento").val($("#id_data_atendimento").val());
        $("#id_data_finalizacao_sat").val() == "" ? $("#id_data_finalizacao_sat").val($("#id_data_fim").val()) : $("#id_data_finalizacao_sat").val($("#id_data_finalizacao_sat").val());
    }

    function nrequeridosSAT(){
        $("#id_empreendimento").removeAttr("required");
        $("#id_bloco").removeAttr("required");
        $("#id_unidade").removeAttr("required");
        $("#id_proprietario").removeAttr("required");
        $("#id_status_processo").removeAttr("required");
        $("#id_tipo_solicitacao").removeAttr("required");
        $("#id_ambiente1").removeAttr("required");
        $("#id_descricao1").removeAttr("required");
        $("#id_reparo1").removeAttr("required");
        $("#id_procedencia1").removeAttr("required");
        $("#id_historico1").removeAttr("required");
        $("#id_estimativa_custo1").removeAttr("required");
        $("#id_duracao1").removeAttr("required");
        $("#id_material1").removeAttr("required");
    }

    function requeridosJuridico(){
        $("#id_resumo_processo").attr("required", "req");
        $("#id_escritorio").attr("required", "req");        
        $("#id_escritorio_advogado").attr("required", "req");      
        $("#id_numero_processo").attr("required", "req");
        $("#id_valor_causa").attr("required", "req");
        $("#id_autor1").attr("required", "req");
        $("#id_reu1").attr("required", "req");
    }

    function nrequeridosJuridico(){
        $("#id_resumo_processo").removeAttr("required");
        $("#id_escritorio").removeAttr("required");
        $("#id_escritorio_advogado").removeAttr("required");
        $("#id_numero_processo").removeAttr("required");
        $("#id_valor_causa").removeAttr("required");
        $("#id_autor1").removeAttr("required");
        $("#id_reu1").removeAttr("required");
    }

    function executores (){
    /* Função que adiciona executores */
    $("#add-executor").click(function(){
        if(contar() >= 2){
            comboALiberar = (10 - contar()) + 2;
            executor = "#executor" + comboALiberar
            $(executor).removeAttr("hidden");
        } else {
            alert("Limite de executores atingido")}
    });

    $("#remove-executor2").click(function(){
        var executor = document.getElementById("id_executor2");
        executor.selectedIndex = 0;
        
        var porcento = document.getElementById("id_porcento2");
        porcento.value = '';

        $("#executor2").attr("hidden", true);

    })

    $("#remove-executor3").click(function(){
        var executor = document.getElementById("id_executor3");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento3");
        porcento.value = '';
        
        $("#executor3").attr("hidden", true);
    });

    $("#remove-executor4").click(function(){
        var executor = document.getElementById("id_executor4");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento4");
        porcento.value = '';
        
        $("#executor4").attr("hidden", true);
    });

    $("#remove-executor5").click(function(){
        var executor = document.getElementById("id_executor5");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento5");
        porcento.value = '';
        
        $("#executor5").attr("hidden", true);
    });

    $("#remove-executor6").click(function(){
        var executor = document.getElementById("id_executor6");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento6");
        porcento.value = '';
        
        $("#executor6").attr("hidden", true);
    });

    $("#remove-executor7").click(function(){
        var executor = document.getElementById("id_executor7");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento7");
        porcento.value = '';
        
        $("#executor7").attr("hidden", true);
    });

    $("#remove-executor8").click(function(){
        var executor = document.getElementById("id_executor8");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento8");
        porcento.value = '';
        
        $("#executor8").attr("hidden", true);
    });

    $("#remove-executor9").click(function(){
        var executor = document.getElementById("id_executor9");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento9");
        porcento.value = '';
        
        $("#executor9").attr("hidden", true);
    });

    $("#remove-executor10").click(function(){
        var executor = document.getElementById("id_executor10");
        executor.selectedIndex = 0;

        var porcento = document.getElementById("id_porcento10");
        porcento.value = '';
        
        $("#executor10").attr("hidden", true);
    });

    }
 
    $("#id_retrospectiva").val($("#id_retrospec").val());

    $("#id_retrospec").change(function(){
        $("#id_retrospectiva").val($("#id_retrospec").val());
        verificarRetrospectiva($("#id_retrospec").val());
    });

    $("#id_retrospectiva").change(function(){
        $("#id_retrospec").val($("#id_retrospectiva").val());
        verificarRetrospectiva($("#id_retrospec").val());
    });

    function verificarRetrospectiva(valor){
        switch (valor){
            case 0:
                $("#aprimorar").html("");
                break;
            case "Foi bom":
                $("#aprimorar").html("O que foi bom?");
                break;
            case "Pode melhorar":
                $("#aprimorar").html("O que pode melhorar?");
                break;
            case "Deve melhorar":
                $("#aprimorar").html("O que deve melhorar?");
                break;
            default:
                $("#aprimorar").html("");
                break;

        }
    }
    verificarRetrospectiva($("#id_retrospec").val());

    $("#cadastrar").click(function(){
        $("#id_data_finalizacao").val($("#id_data_fim").val());
        if(($("#id_processo_relacionado").val() == 75 || $("#id_processo_relacionado").val() == 51) && (($("#id_empreendimento").val() == "") || ($("#id_bloco").val() == "") || ($("#id_unidade").val() == "") || ($("#id_proprietario").val() == "") || ($("#id_status_processo").val() == ""))){
            controller = 5;
            console.log("teste")
            verificarController();
        } else if(($("#id_processo_relacionado").val() == 29) && (($("#id_resumo_processo").val() == "") || ($("#id_escritorio").val() == "") || ($("#id_escritorio_advogado").val() == "") || ($("#id_numero_processo").val() == "") || ($("#id_valor_causa").val() == "") || ($("#id_autor1").val() == "") || ($("#id_reu1").val() == ""))){
            controller = 8;
            console.log(controller)
            verificarController();
        }
    })

    $("#salvar").click(function(){
        if(($("#id_r5w2hT").val() != 0) && (($("#id_rWhat").val() == "") || ($("#id_rWhy").val() == "") || ($("#id_rWhere").val() == "") || ($("#id_rWhen").val() == "") || ($("#id_rWho").val() == "") || ($("#id_rHow").val() == "") || ($("#id_rHowMuch").val() == ""))){
            controller = 4;
            verificarController();
        } else if(($("#id_retrospec").val() != 0) && (($("#id_classificacao").val() == "") || ($("#id_id_responsavel").val() == ""))){
            controller = 3;
            verificarController();
        } else if(($("#id_processo_relacionado").val() == 75 || $("#id_processo_relacionado").val() == 51) && (($("#id_empreendimento").val() == "") || ($("#id_bloco").val() == "") || ($("#id_unidade").val() == "") || ($("#id_proprietario").val() == "") || ($("#id_status_processo").val() == ""))){
            controller = 5;
            verificarController();
        } else if(($("#id_processo_relacionado").val() == 29) && (($("#id_resumo_processo").val() == "") || ($("#id_escritorio").val() == "") || ($("#id_escritorio_advogado").val() == "") || ($("#id_numero_processo").val() == "") || ($("#id_valor_causa").val() == "") || ($("#id_autor1").val() == "") || ($("#id_reu1").val() == ""))){
            controller = 8;
            console.log(controller)
            verificarController();
        }
    });

    function ControlFinalizar(){
        if ((controller != 3) || ($("#id_finalizado").val() == true)){
            $("#finalizar").hide();
        } else {
            $("#finalizar").show();
        }
    }

    $("#mFinalizar").click(function(){
        $("#id_finalizado").val(1);
        console.log($("#id_finalizado").val());
        $("#finalizar").hide();
        $('#id_classificacao').attr('readonly', 'readonly');
        $('#id_rStat').prop("readonly", "readonly");
        $('#id_id_responsavel').prop("readonly", "readonly");
        $("#id_retrospectiva").prop("readonly", "readonly");
        $("#id_retrospec").prop("readonly", "readonly");
        $('#id_rHistorico').attr('readonly', 'readonly');
        $("#modalConfirmacao").hide();
        $('.modal-backdrop').css('display', 'none');
    });

    let data = new Date();
    let dia = data.getDate();
    let mes = data.getMonth() + 1;
    let ano = data.getFullYear();
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
    
    $('#id_status_pendencia').focus(function(){
        if ($('#id_status_pendencia').val() == "") {
            $('#id_status_pendencia').val(`${formatarData(dia) + "/" + formatarData(mes) + "/" + formatarData(ano)} - ${$("#funcionario").html()}: `);
        }
      });

    $('#id_sDescri').focus(function(){
        if ($('#id_sDescri').val() == "") {
            $('#id_sDescri').val(`${formatarData(dia) + "/" + formatarData(mes) + "/" + formatarData(ano)} - ${$("#funcionario").html()}: `);
        }
    });

    $("#id_classificacao").focus(function(){
        if ($("#id_classificacao").val() == "") {
            $("#id_classificacao").val(`${formatarData(dia) + "/" + formatarData(mes) + "/" + formatarData(ano)} - ${$("#funcionario").html()}: `);
        }
    });

    $("#copiar").click(function(){
        if ($("#id_status_pendencia").val() != ""){
            $("#id_historico").val($("#id_status_pendencia").val() + "\n" + $("#id_historico").val());
            $("#id_sDescri").val("");
            $("#id_status_pendencia").val("");
        } else {
            $("#id_sDescri").val("");
            $("#id_status_pendencia").val("");
        }
    });

    $("#rCopiar").click(function(){
        if ($("#id_classificacao").val() != ""){
            $("#id_rHistorico").val($("#id_classificacao").val() + "\n" + $("#id_rHistorico").val());
            $("#id_classificacao").val("");
        } else {
            $("#id_classificacao").val("");
        }
    });

    $("#id_porcento1").attr("required", "req");

    // Altera tamanho do problema
    $("#sidebarCollapse").click(function(){
        $(".ba1_min").toggleClass("ba1_max");
        $(".bb1_min").toggleClass("bb1_max");
        $(".bc1_min").toggleClass("bc1_max");
    });

    // Altera status da tarefa conforme status do processo.
    $("#id_status_processo").change(function(){
        if($("#id_processo_relacionado").val() == 75){
            if($("#id_status_processo").val() ==  "Análise" || $("#id_status_processo").val() ==  "Agendamento" || $("#id_status_processo").val() ==  "Atendimento" || $("#id_status_processo").val() ==  "Termo de Quitação" || $("#id_status_processo").val() == "Jurídico"){
                $("#id_stat").val("Fazendo");
            } else if($("#id_status_processo").val() == "Concluído" || $("#id_status_processo").val() == "Fora de Garantia"){
                $("#id_stat").val("Feito");
                $("#id_porcentagem_sat").val("100");
            } else{
                $("#id_stat").val("Cancelado");
            }
        } else {
            if($("#id_status_processo").val() == "Limpeza" || $("#id_status_processo").val() == "Manutenção" || $("#id_status_processo").val() == "Pagar"){
                $("#id_stat").val("Fazendo");
            } else if ($("#id_status_processo").val() == "Concluído"){
                $("#id_stat").val("Feito");
                $("#id_porcentagem_sat").val("100");
            } else if ($("#id_status_processo").val() == "Cancelado"){
                $("#id_stat").val("Cancelado");
            } else{
                $("#id_stat").val("A fazer");
            }
        }
    });

    $("#id_stat").change(function(){
        if($("#id_stat").val() == 'Feito' && ($("#id_processo_relacionado").val() == 75 || $("#id_processo_relacionado").val() == 51)){
            $("#id_status_processo").val("Concluído")
            $("#id_porcentagem_sat").val("100");
        } 

        if ($("#id_stat") == 'Cancelado' && ($("#id_processo_relacionado").val() == 75 || $("#id_processo_relacionado").val() == 51)){
            $("#id_status_processo").val("Cancelado")
        }
    });

    // Conservação / Limpeza
    if($("#id_processo_relacionado").val() == 51){
        $("#id_stat").change(function(){
            if($("#id_stat").val() == "Feito"){
                $(".salvar").html(`<button type="button" class="btn btn-primary" id="l_editar" data-toggle="modal" data-target="#modalDuplicar">Salvar edição</button>`);
                $(".salvarDuplicar").html(`<input class="btn btn-primary" type="submit" value="Confirmar" id="salvar"/>`);
            } else{
                $(".salvar").html(`<input class="btn btn-primary" type="submit" value="Salvar edição" id="salvar"/>`);
                $(".salvarDuplicar").html(`<button type="button" class="btn btn-primary" data-dismiss="modal">Salvar</button>`);
            }
        });
    }
});
