<html>
	<?php 
	
	include('header.php');
	
		if (!isset($_SESSION)) {
		    session_start();
		}
		
		error_reporting(E_ALL & ~E_NOTICE); 
	   
		
	?>
	<head>
		<link rel="stylesheet" type="text/css" href="stylesheet.css" media="screen" />
		<meta http-equiv="content-type" content="text/html; charset=utf-8">
	</head>
	
	<body>
		
		<!--  Navbar  -->
		<div class='navbar'>
			<a href='https://www.whocando.eu/'><img src='https://www.whocando.eu/images/logoWhoCanDo.jpg' height=35px; style='float:left; margin-right:50px;'></a>
			<button><a href='#searchBox'>Search</a></button>
			<button><a href='#features'>Features</a></button>
			<button><a href='#register'>Registrierung</a></button>
			<button><a href='#function'>Wie es funktioniert's?</a></button>
			<button><a href='#aboutUs'>Über uns</a></button>
		</div>
		<div class='headerProfil'>
		</div>
		<div class='mainFrameRegister'>
			<div class='registerForm'>
        		<h1>Werde ein Teil der WhoCanDo Community<br> und registriere dich jetzt kostenlos:</h1>
        		<?php 
        		$fault = $_GET['fault'];
        		$name = $_GET['name'];
        		$vorName = $_GET['vorname'];
        		$email = $_GET['email'];
        		$uni = $_GET['uni'];
        		$gebDatum = $_GET['gebDatum'];
        		
        		if (isset($fault)) {
        		    if ($fault == 'passwordNotMatched') {
        		        $faultMessage = "Die Passwörter stimmen nicht überein";
        		    } elseif ($fault == 'emailAlreadyUses') {
        		        $faultMessage = "Die Email-Adresse ist bereits registriert";
        		    } elseif ($fault == 'nameMissing') {
        		        $faultMessage = "Bitte gib deinen Nachnamen ein";
        		    } elseif ($fault == 'vorNameMissing') {
        		        $faultMessage = "Bitte gib deinen Vornamen ein";
        		    } elseif ($fault == 'emailMissing') {
        		        $faultMessage = "Bitte gib deine Enail-Adresse ein";
        		    } elseif ($fault == 'uniMissing') {
        		        $faultMessage = "Bitte gib deine Universität an";
        		    } elseif ($fault == 'cityMissing') {
        		        $faultMessage = "Bitte gebe deinen Wohnort ein";
        		    } elseif ($fault == 'gebMissing') {
        		        $faultMessage = "Bitte gebe dein Geburtsdatum an";
        		    } elseif ($fault == 'passwordMissing') {
        		        $faultMessage = "Bitte trage ein Passwort ein";
        		    } elseif ($fault == 'confirmedPasswordMissing') {
        		        $faultMessage = "Bitte bestätige dein Passwort";
        		    }
        		} else {
        		    $faultMessage = "";
        		    
        		}
        		
        		
        		$abfrageUnis = new dbQuery("SELECT ID, name, bundesland FROM db764570417.universitydata");
        		$unis = $abfrageUnis->fetchData('ID', 'name');
        		$uniBundesland = $abfrageUnis->fetchData('ID', 'bundesland');
        		
        		
        		?>
        		<h3 style='color:red;'><?php echo $faultMessage; ?></h3>
        		<form action='https://www.whocando.eu/' method='POST'>
					<label>Name</label>
					<input type='text' name='name' value='<?php echo $name;?>'>
					<label>Vorname</label>
					<input type='text' name='vorname' value='<?php echo $vorName;?>'>
					<label>Email</label>
					<input type='text' name='email' value='<?php echo $email;?>'>
					<label>Universität</label>
					<input type='text' name='uni' id='unis'>
					<!-- 
					<select name='uni'>
					
        				<?php /*
        				    asort($unis);
            				foreach ($unis as $index => $uniName) {
            				    echo "<option value='".$index."'>".$uniName."</option>";
            				} */
        				?>
        			</select> 
        			
					<!--<label>Universität</label>
					<input type='text' name='uni' value='<?php echo $uni;?>'> -->
					
					<label>Stadt</label>
					<input type='text' name='city' value='<?php echo $city;?>'>
					<label>Geburtsdatum</label>
					<input type='date' name='gebDatum' value='<?php echo $gebDatum;?>'>
					<label>Passwort</label>
					<input type='password' name='passwort'>
					<label>Passwort bestätigen</label>
					<input type='password' name='confirmPasswort'>
					<input type='hidden' name='registration' value=1>
					<input type='submit' value='Registrieren'>
					<input type='reset' value='Abbrechen'>
            	</form>
            </div>
        </div>
        
        <!--  Footer  -->
		<div class='footer'>
    		Diese Seite befindet sich noch in den Anfängen und da auch du ein Teil dieser Community bist würden wir uns über ein Feedback von dir freuen!<br>
    		Schreib uns einfach eine Mail an feedback@who-can-do.de<br>
    		Impressum | Datenschutz<br>
    		v1.1.0 &code; 2018 all rights reserved. Powered by WhoCanDo. <br>
		</div>
		
	</body>
</html>
