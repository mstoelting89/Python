<?php
    
    include ('header.php');
    
    if (!isset($_SESSION['userID'])) {
        die("Bitte logge dich ein!");
    }
?>

    <!--  Navbar  -->
    <div class='navbar'>
    <a href='https://www.whocando.eu/'><img src='https://www.whocando.eu/images/logoWhoCanDo.jpg' height=40px; style='float:left; margin-right:50px;'></a>

	<div class='profilLogin'>
			<?php
			if(isset($userID)) {
			    echo "<img src='https://www.whocando.eu/images/profilbildEmpty.jpg''>";
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
    <div class='headerSearch'>
			<div class='headerSearchDetails'>
				
			</div>	
		</div>

<?php 
    
    include('uniArray.php');

    if (!isset($_SESSION['userID'])) {
        die("Bitte logge dich ein!");
    }
    $searchText = $_POST['searchbox'];
    $searchUni = $_POST['universitaet'];
    $searchCategory = $_POST['category'];
    
    
    $searchAbfrage = new dbQuery("SELECT 
                                  u.id, u.name as userName, u.firstName, u.firstLogin, u.lastLogin, u.birthDate, u.email, u.university, u.city, uni.name as uniName, o.offerID,o.title,o.description,o.date,o.price 
                                  FROM db764570417.userdata u 
                                  LEFT JOIN db764570417.universitydata uni ON u.university = uni.ID 
                                  LEFT JOIN db764570417.offerdata o ON o.userid = u.id 
                                  WHERE uni.id = $universityArray[$searchUni]
                                  AND title LIKE '%$searchText%'");
    
    $userName = $searchAbfrage->fetchData('id', 'userName');
    $firstName = $searchAbfrage->fetchData('id', 'firstName');
    $lastLogin = $searchAbfrage->fetchData('id', 'lastLogin');
    $university = $searchAbfrage->fetchData('id', 'uniName');
    $city = $searchAbfrage->fetchData('id', 'city');
    $offerUser = $searchAbfrage->fetchData('offerID','id');
    $offerTitle = $searchAbfrage->fetchData('offerID', 'title');
    $offerDescription = $searchAbfrage->fetchData('offerID', 'description');
    $offerPrice = $searchAbfrage->fetchData('offerID', 'price');
    $offerDate = $searchAbfrage->fetchData('offerID', 'date');
    
    foreach($userName as $userID => $name) {
        echo "<table>";
            echo "<th>".$firstName[$userID]." ".$name."</th>";
                foreach ($offerUser as $offerID => $uID) {
                    if ($uID == $userID) {
                        echo "<tr>";
                            echo "<td></td>";
                            echo "<td>";
                                echo $title;
                            echo "</td>";
                        echo "</tr>";
                        echo "<tr>";
                            echo "<td>Beschreibung</td>";
                            echo "<td>";
                                echo $offerDescription[$offerID];
                            echo "</td>";
                        echo "</tr>";
                        echo "<tr>";
                            echo "<td>Preis</td>";
                            echo "<td>";
                                echo $offerPrice[$offerID];
                            echo "</td>";
                        echo "</tr>";
                        echo "<tr>";
                            echo "<td>Eingestellt am</td>";
                            echo "<td>";
                                echo $offerDate[$offerID];
                            echo "</td>";
                        echo "</tr>";
                        echo "<tr><td><p></td></tr>";
                    }
                }
                
                echo "<tr>";
                    echo "<td>";
                        echo "Kontaktieren";
                    echo "</td>";
                echo "</tr>";
       echo "</table>";    
    } 
    
    
?>