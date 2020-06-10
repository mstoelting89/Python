<html>
	<head>
		<link rel="stylesheet" type="text/css" href="stylesheet.css" media="screen" />
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	<body>
		<h2>Login</h2>
		<form action='index.php' method='POST'>
    		Benutzername / Email: <input type='text' name='userName'><br>
    		Passwort: <input type='password' name='password'><br>
    		<?php if(isset($_GET['falsePassword']) && $_GET['falsePassword'] == 1) {
    		  echo "Bitte geben Sie das richtige Passwort ein!<br>";
    		}?>
    		<input type='submit'>
    	</form>
	</body>
</html>
