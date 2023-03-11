console.log("Página em desenvolvimento");

//Puxar dados do banco de dados na ordem p/ grafico
    var valor = $(valores).text().split(', ');
    var valor_reparo = $(valores_reparo).text().split(', ');
    var mes_axf = $(meses_axf).text().split(', ');
    var listaMes_axf = $(listaMeses_axf).text().split(', ');


    console.log(mes_axf);

    datas = [], abertas = [], finalizadas = [];
    empreendimentos_reparo = [], especialista = [], aluminio = [], madeira = [], eletrica = [], hidraulica = [], gas = [], limpeza = [], logico = [], pintura = [], civil = [];
    empreendimentos = [], sem_avaliacao = [], ruim = [], regular = [], bom = [], otimo = [];

    //Abertas x fechadas
    aux = mes_axf[0].substr(2);
    datas.push(aux);
    for (i=1;i<mes_axf.length-1; i++){
      datas.push(mes_axf[i]);
    }
    datas.push(mes_axf[mes_axf.length-1].substr(0, mes_axf[i].length-2))

    abertas.push(parseInt(listaMes_axf[1]))
    finalizadas.push(parseInt(listaMes_axf[2]))

    for(i=4;i<listaMes_axf.length; i += 2){

      abertas.push(listaMes_axf[i]);
      i += 1;
      if (i == listaMes_axf.length-1){
        finalizadas.push(listaMes_axf[i].substr(0, listaMes_axf[i].length-2));
      } else {
      finalizadas.push(listaMes_axf[i]);
      }
    }

    //Reparo
    aux = valor_reparo[0].substr(2);
    empreendimentos_reparo.push(aux);
    especialista.push(valor_reparo[1])
    aluminio.push(valor_reparo[2])
    madeira.push(valor_reparo[3])
    eletrica.push(valor_reparo[4])
    hidraulica.push(valor_reparo[5])
    gas.push(valor_reparo[6])
    limpeza.push(valor_reparo[7])
    logico.push(valor_reparo[8])
    pintura.push(valor_reparo[9])
    if(valor_reparo.length-1 == 10){
      civil.push(valor_reparo[10].substr(0, valor_reparo[10].length - 2));
    } else {
      civil.push(valor_reparo[10])
    }

    for(i=11;i<valor_reparo.length; i += 1){
      empreendimentos_reparo.push(valor_reparo[i]);
      i += 1;
      especialista.push(valor_reparo[i]);
      i += 1;
      aluminio.push(valor_reparo[i]);
      i += 1;
      madeira.push(valor_reparo[i]);
      i += 1;
      eletrica.push(valor_reparo[i]);
      i += 1;
      hidraulica.push(valor_reparo[i]);
      i += 1;
      gas.push(valor_reparo[i]);
      i += 1;
      limpeza.push(valor_reparo[i]);
      i += 1;
      logico.push(valor_reparo[i]);
      i += 1;
      pintura.push(valor_reparo[i]);
      i += 1;
      if(i == valor_reparo.length-1){
        civil.push(valor_reparo[i].substr(0, valor_reparo[i].length - 2)); 
      } else {
        civil.push(valor_reparo[i]);
      }
    };

    //Satisfação
    aux = valor[0].substr(2)
    empreendimentos.push(aux);
    sem_avaliacao.push(valor[5])
    ruim.push(valor[1])
    regular.push(valor[2])
    bom.push(valor[3])
    if(valor.length-1 == 4){
      otimo.push(valor[4].substr(0, valor[4].length - 2));
    } else {
      otimo.push(valor[4])
    }
    
    for(i=6;i<valor.length; i += 1){
      empreendimentos.push(valor[i]);
      i += 1;
      ruim.push(valor[i]);
      i += 1;
      regular.push(valor[i]);
      i += 1;
      bom.push(valor[i]);
      i += 1;
      otimo.push(valor[i]);
      i += 1;
      if(i == valor.length-1){
        sem_avaliacao.push(valor[i].substr(0, valor[i].length - 2)); 
      } else {
        sem_avaliacao.push(valor[i]);
      }
    }

//Definindo os dados p/ o gráfico de solicitações abertas x finalizadas
let graficoAxF = document.getElementById('axf').getContext('2d');
var canvas_axf = document.getElementById('axf');
 var data_axf = {
  labels: datas,
    datasets: [
      {
        label: 'Abertas',
        backgroundColor: '#C00000',
        data: abertas
      }, 
      {
        label: 'Finalizadas',
        backgroundColor: '#70AD47',
        data: finalizadas
      }
    ]
 };

 //Gráfico de Abertas x Finalizadas
var graficoBarra3 = Chart.Bar(canvas_axf, {
  data: data_axf,
  options: {
    plugins: {
      // Muda as opções de TODAS as labels DESTE gráfico
      datalabels: {
        font: {
          weight: 'bold',
            size: '14'
        },
        formatter: function(value, index, values) {
          if(value >0 ){
              value = value.toString();
              value = value.split(/(?=(?:...)*$)/);
              value = value.join(',');
              return value;
          }else{
              value = "";
              return value;
          }
        }
      }
    },
    // responsive: true,
    scales: {
      xAxes: [{ stacked: false }],
      yAxes: [{ stacked: false}]
    },
    ticks: {
      beginAtZero: true
   },
  }
});

//Definindo os dados p/ o gráfico de tipo de reparo
let graficoTipo = document.getElementById('tipo').getContext('2d');
var canvas_tipo = document.getElementById('tipo');
 var data_tipo = {
    labels: empreendimentos_reparo,
    datasets: [
      {
        label: 'Especialista',
        backgroundColor: '#F7CE1C',
        data: especialista,
      }, 
      {
        label: 'Esquadrias de Alumínio',
        backgroundColor: '#BDBDBD',
        data: aluminio,
      },
      {
        label: 'Esquadrias de Madeira',
        backgroundColor: '#EB4424',
        data: madeira,
      },
      {
        label: 'Instalações Elétricas',
        backgroundColor: '#FEA21E',
        data: eletrica,    
      },
      {
        label: 'Instalações Hidráulicas',
        backgroundColor: '#66a3ff',    
        data: hidraulica, 
      },
      {
        label: 'Instalações Gás',
        backgroundColor: '#BBD631',
        data: gas,  
      },
      {
        label: 'Limpeza',
        backgroundColor: '#1CDB7B',
        data: limpeza, 
      },
      {
        label: 'Lógico e Telefonia',
        backgroundColor: '#4785B6',
        data: logico,
      },
      {
        label: 'Pintura',
        backgroundColor: '#9c9acb',
        data: pintura,
      },
      {
        label: 'Serviço Civil',
        backgroundColor: '#d0abd3',
        data: civil
      }
    ],
  };
  
//Gráfico de tipos de reparo
  var graficoBarra2 = Chart.Bar(canvas_tipo, {
    data: data_tipo,
    options: {
      plugins: {
        // Muda as opções de TODAS as labels DESTE gráfico
        datalabels: {     
          rotation: 320,
          font: {
            weight: 'bold',
            size: '11'
        },
          formatter: function(value, index, values) {
            if(value >0 ){
                value = value.toString();
                value = value.split(/(?=(?:...)*$)/);
                value = value.join(',');
                return value;
            }else{
                value = "";
                return value;
            }
          }
        }
      },
      showAllTooltips: false,
      responsive: true,
      //Escala para manter o grafico com uma barra só
      scales: {
      xAxes: [{ stacked: false,
        barThickness: 8,  // number (pixels) or 'flex'
        maxBarThickness: 12 // number (pixels)
      }],
      yAxes: [{ stacked: false,}]
      },
      ticks: {
        beginAtZero: true
     },
    } 
  });

//Definindo os dados p/ o gráfico de satisfação
let graficoSatisfacao = document.getElementById('satisfacao').getContext('2d');
var canvas_satisfacao = document.getElementById('satisfacao');
 var data_satisfacao = {
    labels: empreendimentos,
    datasets: [
      {
        label: 'Sem Avaliação',
        backgroundColor: '#BDBDBD',
        data: sem_avaliacao,
        hidden: true,
      }, 
      {
        label: 'Ruim',
        backgroundColor: '#EBCCD1',
        data: ruim,
      },
      {
        label: 'Regular',
        backgroundColor: '#FAEBCC',
        data: regular,
      },
      {
        label: 'Bom',
        backgroundColor: '#D6E9C6',
        data: bom,
        
      },
      {
        label: 'Ótimo',
        backgroundColor: '#90ddf5',    
        data: otimo, 
      }],
  };

//Gráfico de Satisfação
var graficoBarra1 = Chart.Bar(canvas_satisfacao, {
  data: data_satisfacao,
  options: {
    plugins: {
      // Muda as opções de TODAS as labels DESTE gráfico
      datalabels: {
        font: {
          weight: 'bold',
          size: '14'
        },
        formatter: function(value, index, values) {
          if(value >0 ){
              value = value.toString();
              value = value.split(/(?=(?:...)*$)/);
              value = value.join(',');
              return value;
          }else{
              value = "";
              return value;
          }
        }
      }
    },
    showAllTooltips: false,
    // responsive: true,
    scales: {
      xAxes: [{ stacked: true }],
      yAxes: [{ stacked: true}]
    },
    ticks: {
      beginAtZero: true
   },
  }
});

$(function(){
    
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
});