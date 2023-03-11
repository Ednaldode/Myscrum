$(document).ready(function() {
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
                    data: [240],
                    backgroundColor: ["#7795d4"],
                    hoverBackgroundColor: ["#7795d4"],
                    borderColor: "#426cc3",
                    borderWidth: 2,
                    label: ["Previsto"]
                },
                {
                    data: [144],
                    backgroundColor: ["#ee9f64"],
                    hoverBackgroundColor: ["#ee9f64"],
                    borderColor: "#e97b22",
                    borderWidth: 2,
                    label: ["Periodo"]
                },
                {
                    data: [197],
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
});

$(document).ready(function() {
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
												 gridLines: {
												 },
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
								 labels: ["Atendimento", "Manutençao", "Compras", "Inplantaçao sistema"],
								 datasets: [{
												 data: [727, 589, 537, 543, 574],
												 backgroundColor: "#7795d4",
												 hoverBackgroundColor: "#7795d4",
												 label: "Relizado"
										 }, {
												 data: [238, 553, 746, 884, 903],
												 backgroundColor: "#ee9f64",
												 hoverBackgroundColor: "#ee9f64",
												 label: "Atraso"
										 }, {
												 data: [1238, 553, 746, 884, 903],
												 backgroundColor: "#ffc200",
												 hoverBackgroundColor: "#ffc200",
												 label: "Inpedimento"
										 }]
						 },
						 options: barOptions_stacked1
				 });
});

$(document).ready(function(){
    var options = {
        title: {
            display: true,
            text: 'Demanda por Procedimentos (pontos)'
        },
        responsive: true,
        maintainAspectRatio: false,

    };
    var container = document.getElementById("quadros");
    var chart = new Chart(container, {
        type: 'pie',
        data: {
          datasets: [{
              data: [10, 20, 30],
              backgroundColor:["#007bff", "#fd7e14", "#ffc107"]
          }],

          // These labels appear in the legend and in the tooltips when hovering different arcs
          labels: [
              'Melhoria cotinua',
              'Conservaçao e limpeza',
              'Implantacao sistema'
          ]
      },
        options: options
    });
});

$(document).ready(function() {
    var ctx = document.getElementById("velocimetro").getContext("2d");
    new Chart(ctx, {
      type: "doughnut",
      responsive: true,
      maintainAspectRatio: false,
      data: {
          datasets: [
              {
                  data: [
                      30,
                      30,
                      20,
                      1,
                      20
                  ],
                  backgroundColor: [
                      "rgb(255, 69, 96)",
                      "rgb(206, 148, 73)",
                      "rgb(153, 223, 89)",
                      "rgba(0, 0, 0, 0.6)",
                      "rgb(153, 223, 89)"
                  ],
                  borderWidth: 0,
                  hoverBackgroundColor: [
                      "rgb(255, 69, 96)",
                      "rgb(206, 148, 73)",
                      "rgb(153, 223, 89)",
                      "rgba(0, 0, 0, 0.6)",
                      "rgb(153, 223, 89)"
                  ],
                  hoverBorderWidth: 0
              },
              {
                  data: [
                      30,
                      30,
                      20,
                      1,
                      20
                  ],
                  backgroundColor: [
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0.6)",
                      "rgba(0, 0, 0, 0)"
                  ],
                  borderWidth: 0,
                  hoverBackgroundColor: [
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0)",
                      "rgba(0, 0, 0, 0.6)",
                      "rgba(0, 0, 0, 0)"
                  ],
                  hoverBorderWidth: 0
              }
          ]
      },
      options: {
          cutoutPercentage: 0,
          rotation: -3.1415926535898,
          circumference: 3.1415926535898,
          legend: {
              display: false
          },
          tooltips: {
              enabled: false
          },
          title: {
              display: true,
              text: 4,
              position: "bottom"
          }
    }
  })
});
