var barChartData = {
  labels: [
    "Absence of OB",
    "Closeness",
    "Credibility",
    "Heritage",
    "M Disclosure",
    "Provenance",
    "Reliability",
    "Transparency"
  ],
  datasets: [
    {
      label: "American Express",
      backgroundColor: "pink",
      borderColor: "red",
      borderWidth: 1,
      data: [3, 5, 6, 7,3, 5, 6, 7]
    },
    {
      label: "Mastercard",
      backgroundColor: "lightblue",
      borderColor: "blue",
      borderWidth: 1,
      data: [4, 7, 3, 6, 10,7,4,6]
    },
    {
      label: "Paypal",
      backgroundColor: "lightgreen",
      borderColor: "green",
      borderWidth: 1,
      data: [10,7,4,6,9,7,3,10]
    },
    {
      label: "Visa",
      backgroundColor: "yellow",
      borderColor: "orange",
      borderWidth: 1,
      data: [6,9,7,3,10,7,4,6]
    }
  ]
};

var chartOptions = {
  responsive: true,
  legend: {
    position: "top"
  },
  title: {
    display: true,
    text: "Chart.js Bar Chart"
  },
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true
      }
    }]
  }
}

window.onload = function() {
  var ctx = document.getElementById("canvas").getContext("2d");
  window.myBar = new Chart(ctx, {
    type: "bar",
    data: barChartData,
    options: chartOptions
  });
};