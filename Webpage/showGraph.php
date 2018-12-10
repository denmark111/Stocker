<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Stock news analytics</title>

    <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js'></script>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script src="js/cloud.js"></script>

    <!-- Main CSS -->
    <link rel="stylesheet" href="css/graph-style.css">
</head>

<body>

    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
        <div id="tradingview_85c60"></div>
        <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank">
                <span class="blue-text">AAPL chart</span>
            </a> by TradingView
        </div>
    </div>
    <!-- TradingView Widget END -->

    <div id="container">
        <div id="graph">
            <canvas id="canvas"></canvas>
        </div>
        <div id="chart"></div>
    </div>

    <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.0/Chart.min.js'></script>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <script src="js/graph.js"></script>

    <script>
        window.onload = function() {

            <?php
                echo $_SESSION['result'];
            ?>

            var result = "<?php echo json_encode($_SESSION['result']); ?>";
            var keyword = "<?php echo $_SESSION['keywords']; ?>";

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
              data: getChartData(result),
              options: getChartOption()
            });
            
            var wCloud = document.getElementById("chart");
            var text_string = keyword
            window.myCloud = drawWordCloud(text_string, wCloud);
        };
    </script>

</body>
</html>