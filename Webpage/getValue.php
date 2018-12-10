<?php

	$stock_name = htmlspecialchars($_POST["stock-name"]);
	# $parser_type = htmlspecialchars($_POST["type"]);

	echo "<p>" . $stock_name . "</p>";

	
	$parser_type = 1;

	if ($parser_type === 1)
	{
		$parser = "nasdaq.py";
	}
	else if ($parser_type === 2)
	{
		$parser = "fidelity.py";
	}
	else if ($parser_type === 3)
	{
		$parser = "seeking.py";
	}
	else
	{
		// Print crawler not available error log
		echo "<p>" . $parser_type . "</p>";
		sleep(3);
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}
	$command = escapeshellcmd("python3 ../parsers/" . $parser . " " . $stock_name);
	$output = shell_exec($command);

	if (strcmp($output, "Success") !== 0)
	{
		// Print crawling fail error log
		echo "<p>" . $output . "</p>";
		sleep(3);
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}
	
	$parser = substr($parser, 0, -3);

	$stock_name = "amzn";
	$parser = "fidelity";

	$db_host = "210.117.181.240";
	$db_user = "home_user";
	$db_passwd = "qaz1234";
	$db_name = "STOCKER";

	$mysqli = new mysqli($db_host, $db_user, $db_passwd, $db_name);

	$positive = array();
	$negative = array();
	$mixed = array();
	$neutral = array();
	$row_cnt = array();
	for ($i = 0; $i < 12; $i++)
	{
		$positive[$i] = 0;
		$negative[$i] = 0;
		$mixed[$i] = 0;
		$neutral[$i] = 0;
		$row_cnt[$i] = 0;
	}

	$keywords = "";

	if ($mysqli)
	{
		$sql = "SELECT * FROM " . $parser . " WHERE stockName = '$stock_name';";

		if ($res = $mysqli->query($sql))
		{
			while ($row = $res->fetch_assoc())
			{
				$dateIndex = (int)substr($row[articleTime], 4, -6) - 1;

				$positive[$dateIndex] += $row["positiveRate"];
				$negative[$dateIndex] += $row["negativeRate"];
				$mixed[$dateIndex] += $row["mixedRate"];
				$neutral[$dateIndex] += $row["neutralRate"];
				
				$row_cnt[$dateIndex]++;

				$keywords .= (str_replace("'", " ", $row["keyWords"]) . " ");
			}
		}
		else
		{
			echo "No result to show";
		}

		for ($i = 0; $i < 12; $i++)
		{
			if ($row_cnt[$i] !== 0)
			{
				$positive[$i] /= $row_cnt[$i];
				$negative[$i] /= $row_cnt[$i];
				$mixed[$i] /= $row_cnt[$i];
				$neutral[$i] /= $row_cnt[$i];
			}
		}

		$res->free();
	}
	else
	{
		echo "<p>MySQL Fail</p>";
	}

	$mysqli->close();
?>

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

            var pos = <?php echo json_encode($positive);?>;
			var neg = <?php echo json_encode($negative);?>;
			var mix = <?php echo json_encode($mixed);?>;
			var neu = <?php echo json_encode($neutral);?>;

           	var keyword = "<?php echo $keywords;?>";

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
            
            var ctx = document.getElementById("canvas").getContext("2d");
            window.myBar = new Chart(ctx, {
              type: "bar",
              data: getChartData(pos, neg, mix, neu),
              options: getChartOption()
            });
            
            var wCloud = document.getElementById("chart");
            window.myCloud = drawWordCloud(keyword, wCloud);
        };
    </script>

</body>
</html>