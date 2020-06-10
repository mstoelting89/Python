<?php

class loginParser {
    
    public function loginChecker($u,$p) {
    
            $userName = $u;
            $password = $p;
            include('dbConnection.php');
            
            $sqlCode = "SELECT id,email,password
                FROM db764570417.logindata
                WHERE email = '$userName'";
            
            $statement = $mysqli->prepare($sqlCode);
            $statement->execute();
            
            $result = $statement->get_result();
            
            while($row = $result->fetch_object()) {
                $userPassword[$row->email] = $row->password;
                $userID[$row->email] = $row->id;
            }
            
            if (password_verify($password, $userPassword[$userName])) {
                $_SESSION['userID'] = $userID[$userName];
                return $userID[$userName];
            } else {
                echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/index.php?falsePassword=1';</script>";
                exit();
            }
            //checken, ob Passwort korrekt
            //wenn ja r�ckgabe von UserID
            //SESSION Daten �bergeben 
       
    }
} 

