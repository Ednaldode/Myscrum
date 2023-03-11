$(function(){
    
    //Buscando cards do kanban
    var linha = $('.linha');
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

    // Percorre cada linha da tabela
    $.each(linha, function(indice, valor){
    
        //Buscando dados no código
        let dataAberto = $('#dataAberto' + $(valor).attr('id'));
        dataAberto = dataAberto.text()

        //Formatando data para jQuery
        let formatarAberto = dataAberto.split('/');
        let aberto = new Date(formatarAberto[2] + '-' + formatarAberto[1] + '-' + formatarAberto[0]);

        let diaUtil = 0
        for (i = aberto.getTime(); i <= dataAtual.getTime() ; i += 86400000){
            i += 86400000;
            diaSemana = new Date(i);
            if ( (diaSemana.getDay() >= 0) && (diaSemana.getDay() <= 7) ) {
                diaUtil += 1;
            }
            i -= 86400000;
        }
        $("#diasAberto" + $(valor).attr('id')).text(diaUtil - 1);
    });

    
});