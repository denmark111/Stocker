function getChartData(result) {
  var barChartData = {
    labels: [
      "May",
      "June",
      "July",
      "Augest",
      "September",
      "October",
      "November",
      "December"
    ],
    datasets: [
      {
        label: "Neutral",
        backgroundColor: "lightgreen",
        borderColor: "green",
        borderWidth: 1,
        data: result["neutral"]
        //data: [3, 5, 6, 7, 3, 5, 6, 7]
      },
      {
        label: "Positive",
        backgroundColor: "lightblue",
        borderColor: "blue",
        borderWidth: 1,
        data: result["positive"]
        //data: [4, 7, 3, 6, 10, 7, 4, 6]
      },
      {
        label: "Negative",
        backgroundColor: "pink",
        borderColor: "red",
        borderWidth: 1,
        data: result["negative"]
        //data: [10, 7, 4, 6, 9, 7, 3, 10]
      },
      {
        label: "Mixed",
        backgroundColor: "yellow",
        borderColor: "orange",
        borderWidth: 1,
        data: result["mixed"]
        //data: [6, 9, 7, 3, 10, 7, 4, 6]
      }
    ]
  };

  return barChartData;
}

function getChartOption() {
  var chartOptions = {
    responsive: true,
    legend: {
      position: "top"
    },
    title: {
      display: true,
      text: "Stock news analysis"
    },
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }

  return chartOptions;
}

function drawWordCloud(text_string, attr) {
  var common = "poop,i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,say,says,said,shall";

  var word_count = {};

  var words = text_string.split(/[ '\-\(\)\*":;\[\]|{},.!?]+/);
  if (words.length == 1) {
    word_count[words[0]] = 1;
  } else {
    words.forEach(function (word) {
      var word = word.toLowerCase();
      if (word != "" && common.indexOf(word) == -1 && word.length > 1) {
        if (word_count[word]) {
          word_count[word]++;
        } else {
          word_count[word] = 1;
        }
      }
    })
  }

  var svg_location = attr;
  var width = $(document).width() / 2;
  var height = $(document).height() / 2;

  var fill = d3.scale.category20();

  var word_entries = d3.entries(word_count);

  var xScale = d3.scale.linear()
    .domain([0, d3.max(word_entries, function (d) {
      return d.value;
    })
    ])
    .range([10, 100]);

  d3.layout.cloud().size([width, height])
    .timeInterval(20)
    .words(word_entries)
    .fontSize(function (d) { return xScale(+d.value); })
    .text(function (d) { return d.key; })
    .rotate(function () { return ~~(Math.random() * 2) * 90; })
    .font("Impact")
    .on("end", draw)
    .start();

  function draw(words) {
    d3.select(svg_location).append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
      .selectAll("text")
      .data(words)
      .enter().append("text")
      .style("font-size", function (d) { return xScale(d.value) + "px"; })
      .style("font-family", "Impact")
      .style("fill", function (d, i) { return fill(i); })
      .attr("text-anchor", "middle")
      .attr("transform", function (d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function (d) { return d.key; });
  }

  d3.layout.cloud().stop();
}

/*
window.onload = function() {

  new TradingView.widget(
    {
      "width": 1900,
      "height": 400,
      "symbol": "NASDAQ:AAPL",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "Light",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_85c60"
    }
  );

  console.log(result);
  console.log(keyword);

  var ctx = document.getElementById("canvas").getContext("2d");
  window.myBar = new Chart(ctx, {
    type: "bar",
    data: getChartData(window.result),
    options: getChartOption()
  });

  var wCloud = document.getElementById("chart");
  var text_string = window.keyword
  window.myCloud = drawWordCloud(text_string, wCloud);
};
*/