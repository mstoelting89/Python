<script>
	var profilePicHeight = $('.pPicture').height();
    var profilePicWidth = $('.pPicture').width();
	var profilePicHeightFactor = profilePicHeight/150;
	var profilePicWidthFactor = profilePicWidth/150;

    var newPictureFactor;
	  
	  if (profilePicHeightFactor > profilePicWidthFactor) {
		  newPictureFactor = profilePicWidthFactor;
	  } else {
		  newPictureFactor = profilePicHeightFactor;
	  }
	  
    var newHeightProfilePic = profilePicHeight/newPictureFactor
	 
    $('.pPicture').height(newHeightProfilePic);

	/*
    $( function() {
        $( ".draggable" ).draggable();
      } ); */
      
</script>

<?php
    
    if (isset($_SESSION['userID'])) {
        
        include('dbConnection.php');
        
        $userID = $_SESSION['userID'];
        
        $abfrageUnis = new dbQuery("SELECT ID, name, bundesland FROM db764570417.universitydata");
        $uniNameID = $abfrageUnis->fetchData('name','ID');
        $unis = $abfrageUnis->fetchData('ID', 'name');
        $uniBundesland = $abfrageUnis->fetchData('ID', 'bundesland'); 
        
        if ($_GET['newData'] == 1) {
            $vorName = utf8_decode($_GET['vorName']);
            $name = utf8_decode($_GET['name']);
            $email = utf8_decode($_GET['email']);
            $city = utf8_decode($_GET['city']);
            $birthDate = utf8_decode($_GET['birthDate']);
            $uni = utf8_decode($_GET['universitaet']);
            $uni = $uniNameID[$uni];
            $topTest = $_GET['top'];
            
            $sqlCode = "UPDATE db764570417.userdata 
                       SET name = '$name', firstName= '$vorName', email = '$email', birthDate = '$birthDate', university = '$uni', city = '$city'
                       WHERE ID = $userID";
            
            $statement = $mysqli->prepare($sqlCode);
            $statement->execute();
            echo "<b>Die Daten wurde geupdatet<br></b>";
        }
        
       
        
        $abfrage = new dbQuery("SELECT u.ID as userID,u.name as userName, u.firstName,u.lastLogin,u.birthDate,u.email,u.university,u.city,uni.name as uniName, u.profilePicture FROM db764570417.userdata u LEFT JOIN db764570417.universitydata uni ON u.university = uni.id WHERE u.ID = '$userID'");
        $userName = $abfrage->fetchData('userID','userName');
        $userFirstName = $abfrage->fetchData('userID','firstName');
        $userLastLogin = $abfrage->fetchData('userID','lastLogin');
        $userBirthDate = $abfrage->fetchData('userID','birthDate');
        $userPicture = $abfrage->fetchData('userID','profilePicture');
        $uniName = $abfrage->fetchData('userID','uniName');
        $userCity = $abfrage->fetchData('userID','city');
        $userEmail = $abfrage->fetchData('userID','email');
        $userUniversity = $abfrage->fetchData('userID','uniName');
 
        
        if ($_POST['newPicture'] == 1) {
            //$uploadFolder = 'Images/profilePictures/';
            $filename = pathinfo($_FILES['profilePicture']['name'], PATHINFO_FILENAME);
            $extension = strtolower(pathinfo($_FILES['profilePicture']['name'], PATHINFO_EXTENSION));
            
            //erlaubte Endungen 
            
            $extensionArray = array('jpg','jpeg','gif','png');
            if(!empty($extension) && !in_array($extension,$extensionArray)) {
               die("Falsches Format"); 
            } 
            
            if(!empty($_FILES['profilePicture']['size']) && $_FILES['profilePicture']['size'] > 10000000) {
                die("Die Datei ist zu groß");
            }
            
            //Überprüfung dass das Bild keine Fehler enthält
            if(function_exists('exif_imagetype')) { //Die exif_imagetype-Funktion erfordert die exif-Erweiterung auf dem Server
                $allowed_types = array(IMAGETYPE_PNG, IMAGETYPE_JPEG, IMAGETYPE_GIF);
                $detected_type = exif_imagetype($_FILES['profilePicture']['tmp_name']);
                if(!empty($extension) && !in_array($detected_type, $allowed_types)) {
                    die("Nur der Upload von Bilddateien ist gestattet");
                } 
            }
            //Pfad zum Upload
            $userID = $_SESSION['userID'];
            $new_path = "Images/profilePictures/".$userID.'.'.$extension;
            move_uploaded_file($_FILES['profilePicture']['tmp_name'], $new_path);
            
            $sqlCode = "UPDATE db764570417.userdata SET profilePicture = '".$new_path."' WHERE ID = $userID";
            $statement = $mysqli->prepare($sqlCode);
            $statement->execute();
            
        }
        
        $change = $_GET['change'];
       
        
    } else {
        die ("Bitte log dich ein: <a href='https://www.whocando.eu'> Login </a>");
    }
    
    echo "<div class='profileInfo'>";
        echo "<form action='profil.php' method='GET' enctype='multipart/form-data'>";
        echo "<table>";
            echo "<tr>";
                echo "<td>";
                    echo "Name:";
                echo "</td>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='text' value='".$userName[$userID]."' name='name'>";
                    } else {
                        echo $userName[$userID];
                    }
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Vorname:";
                echo "</td>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='text' value='".$userFirstName[$userID]."' name='vorName'>";
                    } else {
                        echo $userFirstName[$userID];
                    }
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Email:";
                echo "</td>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='text' value='".$userEmail[$userID]."' name='email'>";
                    } else {
                        echo $userEmail[$userID];
                    }
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Geburtstag:";
                echo "</td>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='date' value='".$userBirthDate[$userID]."' name='birthDate'>";
                    } else {
                        echo $userBirthDate[$userID];
                    }
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Stadt:";
                echo "</td>";
                echo "<td>";
                   if ($change == 1) {
                       echo "<input type='text' value='".$userCity[$userID]."' name='city'>";
                    } else {
                        echo $userCity[$userID];
                    } 
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Universität:";
                echo "</td>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='text' name='universitaet' id='unis' value='".$userUniversity[$userID]."'>";
                    } else {
                        echo $userUniversity[$userID];
                    }
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    if ($change == 1) {
                        echo "<input type='hidden' name='page' value='details'>";
                        echo "<input type='hidden' name='newData' value=1>";
                        echo "<input type='submit' value='Profil updaten'>";
                    } else {
                        echo "<input type='hidden' name='page' value='details'>";
                        echo "<input type='hidden' name='change' value=1>";
                        echo "<input type='submit' value='Profil bearbeiten'>";
                    }
                echo "</td>";
            echo "</tr>";
        echo "</table>";
        echo "</form>";
    echo "</div>";
    
    echo "<div class='profilePictureDetails'>";
        if ($change == 1) {
            
            echo "<form action='profil.php?page=details' method=POST enctype='multipart/form-data'>";
                echo "<table class='profilePicTable'>";
                    echo "<tr>";
                        echo "<td>";
                            echo "<div class='overlayPicture'>";
                                echo "<img src='https://www.whocando.eu/".$userPicture[$userID]."' class='pPicture'><br>";
                            echo "</div>";
                        echo "</td>";
                    echo "</tr>";
                    echo "<tr>";
                        echo "<td>";
                            
                            echo "<input type='hidden' name='newPicture' value=1>";
                            echo "<input type='file' name='profilePicture'>";
                        echo "</td>";
                    echo "</tr>";
                    echo "<tr>";
                        echo "<td>";
                            echo "<input type='submit' value='Hochladen' name='hochladen'>";
                        echo "</td>";
                    echo "</tr>";
                echo "</table>";
            echo "</form>";
        } else {
            echo "<table class='profilePicTable'>";
                echo "<tr>";
                    echo "<td>";
                        echo "<div class='overlayPicture'>";
                            echo "<img src='https://www.whocando.eu/".$userPicture[$userID]."' class='pPicture'>";
                        echo "</div>";
                    echo "</td>";
                 echo "</tr>";
            echo "</table>";
        }
    echo "</div>";
    
       
?>