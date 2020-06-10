<html>
<head>
</head>

<body>
<?php
if (!isset($_SESSION)) {
    session_start();
    echo session_status();
    echo "SessionID: ".session_id();
}

echo "SessionID: ".session_id();
echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/test=1';</script>";
    exit();
?>
</body>
</html>
