function graficoProdutividade(previsto, periodo, realizado) {
    var barOptions_stacked1 = {
        title: {
            display: true,
            text: 'Produtividade (horas)Produtividade (horas)'
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            enabled: true
        },
        hover: {
            animationDuration: 0
        },
        legend: {
            display: true
        },
        scales: {
            yAxes: [{
                ticks: {
                    max: 300,
                    min: 0,
                    stepSize: 100
                }
            }]
        },
        pointLabelFontFamily: "Quadon Extra Bold",
        scaleFontFamily: "Quadon Extra Bold"
    };
    var ctx1 = document.getElementById("barrasV");
    var myChart1 = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: [""],
            datasets: [{
                    data: [previsto],
                    backgroundColor: ["#7795d4"],
                    hoverBackgroundColor: ["#7795d4"],
                    borderColor: "#426cc3",
                    borderWidth: 2,
                    label: ["Previsto"]
                },
                {
                    data: [periodo],
                    backgroundColor: ["#ee9f64"],
                    hoverBackgroundColor: ["#ee9f64"],
                    borderColor: "#e97b22",
                    borderWidth: 2,
                    label: ["Periodo"]
                },
                {
                    data: [realizado],
                    backgroundColor: ["#cccccc"],
                    hoverBackgroundColor: ["#cccccc"],
                    borderColor: "#a1a1a1",
                    borderWidth: 2,
                    label: ["Realizado"]
                }
            ]
        },
        options: barOptions_stacked1
    });
}

function graficoProcedimento(processos, realizado, atrasado, impedimento) {
    var barOptions_stacked1 = {
        title: {
            display: true,
            text: 'Previsto x Realizado e Impedimentos por Procedimento (pontos)'
        },
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
            enabled: true
        },
        hover: {
            animationDuration: 0
        },
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true,
                    fontFamily: "'Open Sans Bold', sans-serif",
                    fontSize: 15
                },
                scaleLabel: {
                    display: false
                },
                gridLines: {},
                stacked: true
            }],
            yAxes: [{
                barThickness: 20,
                gridLines: {
                    display: false,
                    color: "#fff",
                    zeroLineColor: "#fff",
                    zeroLineWidth: 0
                },
                ticks: {
                    fontFamily: "'Open Sans Bold', sans-serif",
                    fontSize: 15
                },
                stacked: true
            }]
        },
        legend: {
            display: true
        },
    };
    var ctx1 = document.getElementById("barrasH");
    var myChart1 = new Chart(ctx1, {
        type: 'horizontalBar',
        data: {
            labels: processos,
            datasets: [{
                data: realizado,
                backgroundColor: "#7795d4",
                hoverBackgroundColor: "#7795d4",
                label: "Relizado"
            }, {
                data: atrasado,
                backgroundColor: "#ee9f64",
                hoverBackgroundColor: "#ee9f64",
                label: "Atraso"
            }, {
                data: impedimento,
                backgroundColor: "#ffc200",
                hoverBackgroundColor: "#ffc200",
                label: "Impedimento"
            }]
        },
        options: barOptions_stacked1
    });

}


function graficoDemanda(processos, realizado, cores){
    var a = processos
    var b = realizado
    var options = {
        title: {
            display: true,
            text: 'Demanda por Procedimentos (pontos)'
        },
        legend: {
            display: false
        },
        responsive: true,
        maintainAspectRatio: false,

    };
    var container = document.getElementById("quadros");
    var chart = new Chart(container, {
        type: 'pie',
        data: {
          datasets: [{
              data: realizado,
              backgroundColor:cores
          }],

          // These labels appear in the legend and in the tooltips when hovering different arcs
          labels: processos
      },
        options: options
    });
}


function graficoVelocimetro(pontos){
    var opts = {

        // color configs
        colorStart: "#6fadcf",
        colorStop: void 0,
        gradientType: 0,
        strokeColor: "#e0e0e0",
        generateGradient: true,
        percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],

        // customize pointer
        pointer: {
          length: 0.8,
          strokeWidth: 0.035,
          iconScale: 1.0
        },

        // static labels
        staticLabels: {
          font: "15px Poppins",
          labels: [0, 4, 8, 12, 15],
          fractionDigits: 0
        },

        // static zones
        staticZones: [
          {strokeStyle: "rgb(207,73,73,1)", min: 0, max: 6},
          {strokeStyle: "rgb(238,160,107,1)", min: 6, max: 8},
          {strokeStyle: "rgb(151,193,122,1)", min: 8, max: 10},
          {strokeStyle: "rgb(238,160,107,1) ", min: 10, max: 12},
          {strokeStyle: "rgb(207,73,73,1)", min: 12, max: 15}
        ],

        // render ticks
        renderTicks: {
          divisions: 4,
          divWidth: 1.1,
          divLength: 0.5,
          divColor: "#000000",
          subDivisions: 3,
          subLength: 0.3,
          subWidth: 0.6,
          subColor: "#666666"
        },

        // the span of the gauge arc
        angle: 0.00,

        // line thickness
        lineWidth: 0.40,

        // radius scale
        radiusScale: 1.0,

        // font size
        fontSize: 35,

        // if false, max value increases automatically if value > maxValue
        limitMax: false,

        // if true, the min value of the gauge will be fixed
        limitMin: false,

        // High resolution support
        highDpiSupport: true

    };
    var target = document.getElementById('velocimetro');
    var gauge = new Gauge(target).setOptions(opts);

    document.getElementById("preview-textfield").className = "preview-textfield";
    gauge.setTextField(document.getElementById("preview-textfield"))

    gauge.maxValue = 15;
    gauge.setMinValue(0);
    gauge.set(pontos);

    gauge.animationSpeed = 32
}
