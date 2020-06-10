<html>
	<head>
		<link rel="stylesheet" type="text/css" href="stylesheet.css" media="screen" />
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	
	<body>
		<?php 
		  $name = $_POST['name'];
		  $vorName = $_POST['vorname'];
		  $email = $_POST['email'];
		  $uni = $_POST['uni'];
		  $geburtstag = $_POST['gebDatum'];
		  $password = $_POST['passwort'];
		  $confirmedPassword = $_POST['confirmPasswort'];
		  
		  $gebDatum = date("Y-m-d",strtotime($geburtstag));
		  
		  include('dbConnection.php');
		  
		  $abfrageEmail = "SELECT email FROM whocando.logindata";
		  $statement = $mysqli->prepare($abfrageEmail);
		  $statement->execute();
		  
		  $result = $statement->get_result();
		  
		  while ($row = $result->fetch_object()) {
		      $userEmails[] = $row->email;
		  }
		  
		  if (password_verify($password, $confirmedPassword)) {
		      die ("Die Passw�rter stimmen nicht �ber ein");
		  } elseif (in_array($email,$userEmails)) {
		      die ("Die Email ist bereits registriert");  
		  } else {
		      
		      $date = date("Y-m-d H:i:s",time());
    		  $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    		  $sqlCode = "INSERT INTO whocando.loginData (name,email,password)
                      VALUES (?,?,?)";
    		  
    		  $userName = $vorName."".$name;
    		  
    		  $statement = $mysqli->prepare($sqlCode);
    		  $statement->bind_Param('sss',$userName,$email,$hashedPassword);
    		  $statement->execute();
    		  $newUserId = $mysqli->insert_id;
    		  
    		  $sqlCode = "INSERT INTO whocando.userData (ID,name,firstName,firstLogin,lastLogin,birthDate,email,university)
                          VALUES (?,?,?,?,?,?,?,?)";
    		  
    		  $statement = $mysqli->prepare($sqlCode);
    		  $statement->bind_Param('isssssss',$newUserId,$name,$vorName,$date,$date,$gebDatum,$email,$uni);
    		  
    		  $statement->execute();
		  } 
		?>
	</body>

</html>
