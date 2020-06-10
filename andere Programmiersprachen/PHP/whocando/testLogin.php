<?php
   session_start();
    include('dbConnection.php');
    $userName = $_POST['userName'];
    $password = $_POST['password'];
    $_SESSION['userName'] = $userName;
    
    $sqlCode = "SELECT id,email,password
                FROM whocando.loginData
                WHERE email = '$userName'";
    
    $statement = $mysqli->prepare($sqlCode);
    $statement->execute();
    
    $result = $statement->get_result();
    
    while($row = $result->fetch_object()) {
        $userArray[$row->email] = $row->password;
        $userID[$row->email] = $row->id;
    }
    
    $_SESSION['userID'] = $userID[$userName];
    
    //$hashedPassword = password_hash($password, PASSWORD_DEFAULT);
   
    if (password_verify($password, $userArray[$userName])) {
        echo "Die Passwörter stimmen überein!";
        $_SESSION['logIn'] = 1;
        echo "<a href='testFile.php'>Link</a>";
    } else {
        echo "Die Passwörter stimmen nicht überein!";
        
        header("Location:login.php?falsePassword=1");
    }
    
 ?>