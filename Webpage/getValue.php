<?php

/*
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
*/

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
				$dateIndex = (int)(substr($row[articleTime], 4, -6)) - 1;

				$positive[$dateIndex] += $row["positiveRate"];
				$negative[$dateIndex] += $row["negativeRate"];
				$mixed[$dateIndex] += $row["mixedRate"];
				$neutral[$dateIndex] += $row["neutralRate"];
				
				// $result["positive"][$dateIndex] += $row["positiveRate"];
				// $result["negative"][$dateIndex] += $row["negativeRate"];
				// $result["mixed"][$dateIndex] += $row["mixedRate"];
				// $result["neutral"][$dateIndex] += $row["neutralRate"];
				
				$row_cnt[$dateIndex]++;

				$keywords .= ($row["keyWords"] . " ");
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
	}

		$res->free();
	}
	else
	{
		echo "<p>MySQL Fail</p>";
	}

	$mysqli->close();

	echo print_r($positive);
	echo print_r($negative);
	echo print_r($mixed);
	echo print_r($neutral);

	//header("Location: showGraph.php");
?>

<script>
	var res = <?php echo json_encode($positive);?>;
	console.log(res);
</script>