<?php

$db_host = "localhost";
$db_user = "root";
$db_passwd = "confidential";
$db_name = "test";

$mysqli = new mysqli($db_host, $db_user, $db_passwd, $db_name);

if ($mysqli)
{
    echo "<p>MySQL Alive!!</p>"

    $sql = 'SELECT * FROM test';
    $res = $mysqli->query($sql);

    if ($res->num_rows > 0)
    {
        while ($row = $res->fetch_assoc())
        {
            echo "$row["timeStamp"] . $row["positive"]";
        }
    }
    else
    {
        echo "0 Results";
    }
}
else
{
    echo "Failed to access database";
}

$mysqli->close();
?>