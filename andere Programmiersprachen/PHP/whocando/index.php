<?php 
include('header.php');

?>

		<!--  Navbar  -->
		<div class='navbar'>
			<a href='https://www.whocando.eu/'><img src='https://www.whocando.eu/images/logoWhoCanDo.jpg' height=40px; style='float:left; margin-right:50px;'></a>
			<button><a href='/#search'>Search</a></button>
			<button><a href='https://www.whocando.eu/#features'>Features</a></button>
			<button><a href='https://www.whocando.eu/#register'>Registrierung</a></button>
			<button><a href='https://www.whocando.eu/#function'>Wie es funktioniert's?</a></button>
			<button><a href='https://www.whocando.eu/#aboutUs'>Über uns</a></button>
			<div class='profilLogin'>
				<?php 
					//****************************************************************
					//
					// Abfrage ob die SessionID gesetzt ist. 
					//
					//****************************************************************
					
					//****************************************************************
					// Wenn ja, werden die Userdaten aus der Datenbank geladen
					//****************************************************************
    				if(isset($userID)) {
    				        echo "<img src='https://www.whocando.eu/".$userPicture[$userID]."'>";
    				   echo "<div class='profilName'>";
    				        echo $userFirstName[$userID]." ".$userName[$userID];
    				   echo "</div>";
    				   echo "<div class='profilMenu'>";
    				        echo "<table>";
    				            echo "<tr><td>";
    				                 echo "<button><a href='https://www.whocando.eu/profil.php?page=details'>Profildetails</a></button>";
    				            echo "</td></tr>";
    				            echo "<tr><td>";
    				                 echo "<button><a href='https://www.whocando.eu/profil.php?page=offers'>Deine Angebote</a></button>";
    				            echo "</td></tr>";
    				            echo "<tr><td>";
    				                 echo "<button><a href='https://www.whocando.eu/profil.php?page=messages'>Nachrichten</a></button>";
    				            echo "</td></tr>";
    				            echo "<tr><td>";
    				                  echo "<button><a href='https://www.whocando.eu/profil.php?page=preferences'>Einstellungen</a></button>";
    				            echo "</td></tr>";
    				            echo "<tr><td>";
    				                  echo "<button><a href='https://www.whocando.eu/index.php?logout=1'>Logout</a></button>";
    				            echo "</td></tr>";
    				       echo "</table>";
    				   echo "</div>";
					   
					//****************************************************************
					// Wenn nicht, werden Einlogmöglichkeiten zur Verfügung gestellt
					//****************************************************************
    				} else {
    				    echo "<div class='loginField'>";
    				        echo "Login";
    				    echo "</div>";
    				    echo "<div class='loginDetails'>";
    			            echo "<form action='https://www.whocando.eu/' method='POST' class='loginForm'>";
    			                echo "<table>";
    			                    echo "<tr>";
    			                        echo "<td>";
    			                            echo "<label>Benutzername</label>";
    			                            echo "<input type='text' name='userName'>";
    			                         echo "</td>";
    			                     echo "</tr>";
    			                     echo "<tr>";
    			                        echo "<td>";
    			                            echo "<label>Passwort</label>";
    			                            echo "<input type='password' name='password'>";
    			                        echo "</td>";
    			                     echo "</tr>";
    			                     if ($falsePassword == 1) {
    			                         ?>
    			                         <script>
    			                         	$(".loginDetails").toggle("slow");
    			                         </script>
    			                         <?php 
    			                         echo "<tr><td>";
    			                             echo "Email oder Passwort sind falsch!";
    			                         echo "</td></tr>";
    			                     }
    			                     echo "<tr>";
    			                        echo "<td>";
    			                            echo "<input type='submit' value='Einloggen'>";
    			                            echo "<button><a href='https://www.whocando.eu/registration.php'>Registrieren</a></button>";
    			                        echo "</td>";
    			                     echo "</tr>";
    			                 echo "</table>"; 
    			             echo "</form>";
    			         echo "</div>";
    				}
				?>	
			</div>
		</div>
		
		<!--  Header -->
		
		<?php 
			//****************************************************************
			// Datenbankabfrage alles Unis für das Autofill-Dropdown Menü
			//****************************************************************
			$abfrageUnis = new dbQuery("SELECT ID, name, bundesland FROM db764570417.universitydata");
			$unis = $abfrageUnis->fetchData('ID', 'name');
			$uniBundesland = $abfrageUnis->fetchData('ID', 'bundesland');
		?>
		
		<div class='header'> <!--  
			<div class='headerText' id='headerOne'>Studenten suchen</div>
			<div class='headerText' id='headerTwo'>Studenten finden</div>
			<div class='headerText' id='headerThree'>Studenten verbinden</div> -->
			
			<div id="carousel"> 
                  <div class="btn-bar">
                    <div id="buttons"><a id="prev" href="#"></a><a id="next" href="#"></a> </div>
                  </div>
                <div id="slides">
                    <ul>
                        <li class="slide">
                            <div class="quoteContainer">
                            	Du brauchst Nachhilfe in Mathe?<br>
                           	</div>
                            <div class="quoteContainer">
                            	Du möchtest neue Fotos von dir?<br>
                            </div>
                            <div class="quoteContainer">
                            	Du wolltest schon immer Luftgitarre spielen lernen?     	
                            </div>
                        </li>
                        <li class="slide">
                            <div class="quoteContainer">
                                Du kannst gut Physik Nachhilfe geben?<br>
                            </div>
                            <div class="quoteContainer">
                                Gitarre spielen ist ein klacks für dich?<br>
                            </div>
                            <div class="quoteContainer">
                                Oder du bist ein begnadeter Steptänzer?<br>
                            </div>
                        </li>
                        <li class="slide">
                            <div class="quoteContainer">
                                Dann melde dich jetzt kostenlos an! 
                            </div>
                            <div class="quoteContainer">
                                Lerne etwas neues - Bringe anderen etwas bei
                            </div>
                            <div class="quoteContainer">
                                Studenten suchen ... finden ... verbinden
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
		</div>
		
		<!--  Searchbox  -->
		<div class='search' id='searchBox'>
			<h2 style='text-align:center;'>Suche hier nach dem umfangreichen Angebot an deiner Universität</h2>
			<form class='searchForm' action='search.php' method='POST'>
				<label>Was?</label>
    			<input type='search' name='searchbox'>
    			<label>Wo?</label>
    			<input type='text' name='universitaet' id='unis'>
    			<label>Kategoie</label>
    			<select name='category'>
    				<option>Nachhilfe</option>
    				<option>andere Dienstleistungen</option>
    				<option>Kommilitonen</option>
    			</select>
    			<input type='submit'>
    		</form>	
		</div>
				
		<!--  Infoboxen  -->
		<div class='infoSection' id='features'>
    		<div class='infoBox'>
    			<div class='infoHeader'>
    				<img src='https://www.whocando.eu/images/icons8-omnichannel-100.png' width='80px'>
    			</div>
    			<div class='infoText'>
    				<h3>Vernetze dich mit anderen Studenten</h3>
    				Egal was du brauchst und egal was du suchst,
    				an deiner Uni gibt es jemanden der dir das beibringen kann.
    			</div>
    		</div>
    		
    		<div class='infoBox'>
    			<div class='infoHeader'>
    				<img src='https://www.whocando.eu/images/icons8-us-dollar-64.png' width='80px'>
    			</div>
    			<div class='infoText'>
    				<h3>Was kostet dich das?</h3>
					Du und der Tutor können die Gegenleistung selbst bestimmen.
					Ob ein Kasten Bier, ein kleines Entgeld oder
					was anderes ist euch überlassen.
    			</div>
    		</div>
    		
    		<div class='infoBox'>
    			<div class='infoHeader'>
    				<img src='https://www.whocando.eu/images/icons8-händeschütteln-64.png' width='80px'>
    			</div>
    			<div class='infoText'>
    				<h3>Zeige was du kannst und biete es an</h3>
    				Du bist gut in Mathe oder kannst außerordentlich Ballet tanzen? 
    				Dann werde Tutor und bringe es anderen bei und verdiene dir etwas dazu.
    			</div>
    		</div>
    		
    		<div class='infoBox' style='margin-bottom:5%;'>
    			<div class='infoHeader'>
    				<img src='https://www.whocando.eu/images/icons8-suche-80.png' width='80px'>
    			</div>
    			<div class='infoText'>
    				<h3>Was kann man hier alles finden?</h3>
    				Es gibt keine Grenzen. Suche, finde und biete an was du willst!
    			</div>
    		</div>
    	</div>
		
		<!--  Registrierung  -->
		<div class='loginSection' id='register' style='clear:left;'>
			<div class='login'>
				<button id='middleLoginButton'>Login</button>
				<button>
					<a href='https://www.whocando.eu/registration.php'>
						Registrieren
					</a>
				</button>
				<div class='loginFieds'>
					<form action='https://www.whocando.eu/' method='POST' class='middleLoginForm'>
						<label>Benutzername</label>
    			        <input type='text' name='userName'>
    			        <label>Passwort</label>
    			        <input type='password' name='password'>
    			        <input type='submit' value='Einloggen'>
    			     </form>
				</div>
			</div>
		</div>
		
		<!--  Steps to use WhoCanDo  -->
		
		
		<div class='explanationSection' id='function'>
			<h2 style='text-align:center;'>So funktioniert's</h2>
			<div class='explanationLeft'>
				<h3>Erstelle dir ein Profil</h3>
				<div class='explanationText'>
        			Richte dir dein Profil ein und du kannst sofort mit anderen 
        			Studenten in Kontakt treten. 
        			Es dauert zwei Minuten und ist komplett kostenlos.
        		</div>
			</div>
			<div class='explanationRight'>
				<div class='explanationImage'>
					<img src='https://www.whocando.eu/images/170422_Who_Can_Do_016.jpg'>
				</div>
			</div>
			<div class='explanationLeft'>
				<div class='explanationImage'>
					<img src='https://www.whocando.eu/images/170422_Who_Can_Do_016.jpg'>
				</div>
			</div>
			<div class='explanationRight'>
				<h3>WhoCanDo ist ganz einfach</h3>
				<div class='explanationText'>
    				Suche nach Nachhilfe, Fotografie, ganz egal was du brauchst! 
    				Finde Kommilitonen an deiner Uni, die dir weiterhelfen können oder schau direkt 
    				in die verschiedenen Kategorien rein und entdecke was alles angeboten wird.
    			</div>
			</div>
			<div class='explanationLeft'>
				<h3>Biete deine Fähigkeiten an</h3>
				<div class='explanationText'>
					Du möchtest auch gerne etwas anbieten und deinen Kommilitonen mir deinen Fähigkeiten helfen? 
					Dann füge es einfach in deinem Profil hinzu.
				</div>
			</div>
			<div class='explanationRight'>
				<div class='explanationImage'>
					<img src='https://www.whocando.eu/images/170422_Who_Can_Do_016.jpg'>
				</div>
			</div>
		</div>
		
		<!--  Ueber Uns  -->
		<div class='aboutSection' id='aboutUs'>
			<div class='schraegAufheben'>
    			<h2 style='text-align:center;'>Wer wir sind</h2>
    			<div class='aboutSectionText'>
    				Wir sind Studenten aus Hamburg und uns 
    				ist eine ganz einfache Sache aufgefallen - die meisten 
    				Studenten sind in irgendetwas außerordentlich gut. 
    				Sei es in Mathe Nachhilfe oder im Fotografieren. 
    				Egal ob Tanzen oder eine Fremdsprache, die Talente sind 
    				bei jeder Universität sehr vielseitig. Warum schaffen 
    				wir nicht die Möglichkeit, Studenten untereinander zu 
    				verbinden, um diese Talente zu teilen und sie sich beizubringen? 
    				Also haben wir WhoCanDo gestartet, um Studenten die Chance
    				zu geben sich gegenseitig zu helfen. Seid ein Teil von uns und
    				helft uns dabei besonders vielseitig zu werden!
    			</div>
    			<div>
    				<img src='https://www.whocando.eu/images/170422_Who_Can_Do_029.jpg' width='45%'>
    			</div>
    		</div>
		</div>
		
		<!--  Footer  -->
		<?php 
		  include('footer.php');
		?>
	</body>
</html>

