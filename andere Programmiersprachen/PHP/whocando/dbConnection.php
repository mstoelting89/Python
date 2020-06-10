<?php  
    $servernameDB = 'db764570417.hosting-data.io';
    $usernameDB = 'dbo764570417';
    $passwordDB = 'Rainbow1989!';
    
    $mysqli = new mysqli($servernameDB,$usernameDB,$passwordDB);
    
    if ($mysqli->connect_errno) {
        die("Verbindung fehlgeschlagen: " . $mysqli->connect_error);
    }
    

   ?>