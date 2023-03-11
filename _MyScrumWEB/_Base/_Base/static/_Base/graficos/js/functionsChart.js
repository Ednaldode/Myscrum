function graficoProdutividade(previsto, periodo, realizado) {

    var barOptions_stacked1 = {
        title: {
            display: true,
            text: 'Produtividade (horas)'
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
            animationDuration: 10
        },
        scales: {
            xAxes: [{
                ticks: {
                    beginAtZero: true,
                },
                scaleLabel: {
                    display: true
                },
                gridLines: {},
                stacked: true
            }],
            yAxes: [{
                barThickness: 15,
                gridLines: {
                    display: true,
                    color: "#fff",
                    zeroLineColor: "#fff",
                    zeroLineWidth: 1
                },
                ticks: {
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
            display: false,
            defaultFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
            defaultFontStyle: 'normal',
            defaultFontSize: 10,
            defaultFontColor: '#215487'

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
        maintainAspectRatio: false,

        // color configs
        colorStart: "#6fadcf",
        colorStop: void 0,
        gradientType: 0,
        strokeColor: "#e0e0e0",
        generateGradient: true,
        percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],

        // customize pointer
        pointer: {
          length: 0.6,
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
          divWidth: 1,
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
        fontSize: 25,

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

function graficoCC(cc1, cc2, cc3, cc4, cc5) {
    var barOptions_stacked1 = {
        title: {
            display: true,
            text: 'Produtividade (horas) por Centro de Custo'
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
    var ctx1 = document.getElementById("barrasVCC");
    var myChart1 = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: [""],
            datasets: [{
                    data: [cc1.pontos],
                    backgroundColor: ["#7795d4"],
                    hoverBackgroundColor: ["#7795d4"],
                    borderColor: "#426cc3",
                    borderWidth: 2,
                    label: [cc1.nome]
                },
                {
                    data: [cc2.pontos],
                    backgroundColor: ["#ee9f64"],
                    hoverBackgroundColor: ["#ee9f64"],
                    borderColor: "#e97b22",
                    borderWidth: 2,
                    label: [cc2.nome]
                },
                {
                    data: [cc3.pontos],
                    backgroundColor: ["#cccccc"],
                    hoverBackgroundColor: ["#cccccc"],
                    borderColor: "#a1a1a1",
                    borderWidth: 2,
                    label: [cc3.nome]
                },
                {
                    data: [cc4.pontos],
                    backgroundColor: ["#203566"],
                    hoverBackgroundColor: ["#203566"],
                    borderColor: "#203590",
                    borderWidth: 2,
                    label: [cc4.nome]
                },
                {
                    data: [cc5.pontos],
                    backgroundColor: ["#cf4949"],
                    hoverBackgroundColor: ["#cf4949"],
                    borderColor: "#cf4954",
                    borderWidth: 2,
                    label: [cc5.nome]
                }
            ]
        },
        options: barOptions_stacked1
    });
}


    /**
 * Sum elements of an array up to the index provided.
 */
function sumArrayUpTo(arrData, index) {
    var total = 0;
    for (var i = 0; i <= index; i++) {
        if (arrData.length > i) {
        total += arrData[i];
            }
    }
    return total;
    }
  
function showBurnDown(elementId, burndownData, scopeChange = []) {

var speedCanvas = document.getElementById(elementId);

Chart.defaults.global.defaultFontFamily = "Arial";
Chart.defaults.global.defaultFontSize = 14;

const totalHoursInSprint = burndownData[0];
const idealHoursPerDay = totalHoursInSprint / 9;
i = 0;

var speedData = {
    labels: [ "Day 1",	"Day 2",	"Day 3",	"Day 4",	"Day 5",	"Day 6",	"Day 7",	"Day 8",	"Day 9", "Day 10"],
    datasets: [
    {
        label: "Burndown",
        data: burndownData,
        fill: false,
        borderColor: "#cf4949",
        backgroundColor: "#cf4949",
        lineTension: 0,
    },
    {
        label: "Ideal",
        borderColor: "#7795d4",
        backgroundColor: "#7795d4",
        lineTension: 0,
        borderDash: [5, 5],
        fill: false,
        data: [
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 0)), // 1
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 1)), // 2
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 2)), // 3
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 3)), // 4
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 4)), // 5
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 5)), // 6
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 6)), // 7
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 7)), // 8
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 8)), // 9
        Math.round(totalHoursInSprint - (idealHoursPerDay * i++) + sumArrayUpTo(scopeChange, 9))  // 10
        ]
    },
    ]
};

var chartOptions = {
maintainAspectRatio: false,
    legend: {
    display: true,
    position: 'top',
    labels: {
        boxWidth: 80,
        fontColor: 'black'
    }
    },
    scales: {
        yAxes: [{
            ticks: {
                min: 0,
                max: Math.round(burndownData[0] * 1.1)
            }
        }]
    }
};

var lineChart = new Chart(speedCanvas, {
    type: 'line',
    data: speedData,
    options: chartOptions
});

}

