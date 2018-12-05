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
		header("Location: " . $_SERVER["HTTP_REFERER"]);
	}
	$command = escapeshellcmd("python3 ./parsers/" . $parser . " " . $stock_name);
	$output = shell_exec($command);

	if ($output === "Failed")
	{
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
