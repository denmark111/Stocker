<?php
	echo "<p>Hello World</p>";

	$stock_name = htmlspecialchars($_POST["stock-name"]);
	$parser_type = htmlspecialchars($_POST["type"]);

	echo "<p>" . $stock_name . "</p>";

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
        // Print $parser_type not set error
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}
	$command = escapeshellcmd("python3 ../parsers/" . $parser . " " . $stock_name);
    $output = shell_exec($command);
    sleep(1)

	if ($output === "Failed")
	{
        // Print failed message before return
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}

	$db_host = "localhost";
	$db_user = "root";
	$db_passwd = "12341234";
	$db_name = "test";

	$mysqli = new mysqli($db_host, $db_user, $db_passwd, $db_name);

	if ($mysqli)
	{
		echo "<p>MySQL Success</p>";

		$sql = "SELECT * FROM result WHERE stock_name = " . $stock_name;

		if ($res = $mysqli->query($sql))
		{
			while ($row = $res->fetch_assoc())
			{
				echo $row["timeStamp"] . " " . $row["positive"];
			}
		}
		else
		{
			echo "No result to show";
		}

		$res->free();
	}
	else
	{
		echo "<p>MySQL Fail</p>";
	}

	$mysqli->close();
?>


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

</body>
</html>