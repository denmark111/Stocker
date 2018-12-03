<?php

$db_host = "localhost";
$db_user = "root";
$db_passwd = "confidential";
$db_name = "temp";

$mysqli = new mysqli($db_host, $db_user, $db_passwd, $db_name);

if ($mysqli)
{
    // DO DATABASE STUFF!!
}
else
{
    echo "Failed to access database";
}

?>