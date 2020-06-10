<?php 
    include('header.php');
    
    
?>		
		
		<!--  Navbar  -->
		
		<div class='navbar'>
			<a href='https://www.whocando.eu/'><img src='https://www.whocando.eu/images/logoWhoCanDo.jpg' height=40px; style='float:left; margin-right:50px;'></a>
			
			<div class='profilLogin'>
				<?php 
    				if(isset($userID)) {
    				   echo "<img src='https://www.whocando.eu/".$userPicture[$userID]."' class='menuProfilePic'>";
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
		
		
		<div class='headerProfil'>
			<div class='headerProfilDetails'>
				<?php 
                    //echo "<img src='https://www.whocando.eu/".$userPicture[$userID]."'>";
			    ?>
				<span><?php //echo $userFirstName[$userID]." ".$userName[$userID];?></span>
			</div>	
		</div>
		<div class='mainframe'>
    		<div class='sidebar'>
    			<?php
        			if (isset($_GET['page'])) {
        			    $page = $_GET['page'];
        			    $messageSystem = $_GET['messageSystem'];
        			} elseif(isset($_POST['page'])) {
        			    $page = $_POST['page'];
        			    $messageSystem = $_POST['messageSystem'];
        			}
        			
        			if ($page == 'details') {
        			    echo "<button style='background-color:#F38333;'><a style='color:white;' href='https://www.whocando.eu/profil.php?page=details'>Profil Details</a></button>";
        			} else {
        			    echo "<button><a href='https://www.whocando.eu/profil.php?page=details'>Profil Details</a></button>";
        			}
        			
        			if ($page == 'offers') {
        			    echo "<button style='background-color:#F38333;'><a style='color:white;' href='https://www.whocando.eu/profil.php?page=offers'>Angebot</a></button>";
        			} else {
        			    echo "<button><a href='https://www.whocando.eu/profil.php?page=offers'>Angebot</a></button>";
        			}
        			
        			if ($page == 'messages') {
        			    echo "<button style='background-color:#F38333;'><a style='color:white;' href='https://www.whocando.eu/profil.php?page=messages'>Nachrichten</a></button>";
        			    
        			    if ($messageSystem == 'write') {
        			        echo "<button style='background-color:#F38333;width:100px;margin-left:56px;'><a style='color:white;font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=write'>Nachricht schreiben</a></button>";
        			    } else {
        			        echo "<button style='width:100px;margin-left:56px;'><a style='font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=write'>Nachricht schreiben</a></button>";
        			    }
        			    
        			    if ($messageSystem == 'inbox') {
        			        echo "<button style='background-color:#F38333;width:100px;margin-left:56px;'><a style='color:white;font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=inbox'>Posteingang</a></button>";
        			    } else {
        			        echo "<button style='width:100px;margin-left:56px;'><a style='font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=inbox'>Posteingang</a></button>";
        			    }
        			    
        			    if ($messageSystem == 'outbox') {
        			        echo "<button style='background-color:#F38333;width:100px;margin-left:56px;'><a style='color:white;font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=outbox'>Postausgang</a></button>";
        			    } else {
        			        echo "<button style='width:100px;margin-left:56px;'><a style='font-size:12px;font-weight:normal;' href='https://www.whocando.eu/profil.php?page=messages&messageSystem=outbox'>Postausgang</a></button>";
        			    }
        			        
        			} else {
        			    echo "<button><a href='https://www.whocando.eu/profil.php?page=messages'>Nachrichten</a></button>";
        			}
        			
        			if ($page == 'preferences') {
        			    echo "<button style='background-color:#F38333;'><a style='color:white;' href='https://www.whocando.eu/profil.php?page=preferences'>Einstellungen</a></button>";
        			} else {
        			    echo "<button><a href='https://www.whocando.eu/profil.php?page=preferences'>Einstellungen</a></button>";
        			}
        	     
    			//<button><a href='https://www.whocando.eu/profil.php?page=details'>Profil Details</a></button>
    			//echo "<button><a  href='https://www.whocando.eu/profil.php?page=offers'>Angebot</a></button>";
    			//echo "<button><a href='https://www.whocando.eu/profil.php?page=messages'>Nachrichten</a></button>";
    			//echo "<button><a href='https://www.whocando.eu/profil.php?page=preferences'>Einstellungen</a></button>";
    			?>
    		</div>
    		<div class='content'>
    			<?php 
    			if (isset($_GET['page'])) {
    			    $page = $_GET['page'];
    			} elseif(isset($_POST['page'])) {
    			    $page = $_POST['page'];
    			}
        			
        			
        			
        			if ($page == 'details') {
        			    include('details.php');
        			} elseif ($page == 'offers') {
        			    include('offers.php');
        			} elseif ($page == 'messages') {
        			    include('messages.php');        
        			} elseif ($page == 'preferences') {
        			    include('preferences.php');
        			} else {
        			    include('details.php');
        			}
    			
    			?>
    		</div>
    	</div>
    	
    	<!--  Footer  -->
	
	</body>
</html>