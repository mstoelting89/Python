<?php

    if (isset($_SESSION['userID'])) {
        
        include('dbConnection.php');
        
        
        if (isset($_POST['eintragung'])) {
            
            $date = date("Y-m-d H:i:s",time());
            
            $userID = $_SESSION['userID'];
            $title = $_POST['title'];
            $description = $_POST['description'];
            $price = $_POST['price'];
            
            $sqlCode = "INSERT INTO db764570417.offerdata (userID,title,description,price,date)
                        VALUES (?,?,?,?,?)";
            
            $statement = $mysqli->prepare($sqlCode);
            $statement->bind_Param('issss',$userID,$title,$description,$price,$date);
            
            if($statement->execute()) {
                echo "Eintragung erfolgreich!";
            } else {
                echo "Query fehlgeschlagen: ".$statement->error;
            }
        }
        
        $offerID = $_POST['offerID'];
        
        if (isset($_POST['loeschen'])) {
            
            $sqlCode = "DELETE FROM db764570417.offerdata WHERE offerID = $offerID";
            
            $statement = $mysqli->prepare($sqlCode);
            
            if($statement->execute()) {
                echo "Eintrag wurde erfolgreich gelöscht!";
            } else {
                echo "Query fehlgeschlagen: ".$statement->error;
            }
        }
        
        $userID = $_SESSION['userID'];
        
        $abfrageEigenesAngebot = new dbQuery("SELECT 
                                              offerID, title, description, price, date 
                                              FROM db764570417.offerdata 
                                              WHERE userID = $userID");
        
        $offerTitle = $abfrageEigenesAngebot->fetchData('offerID', 'title');
        $offerDescription = $abfrageEigenesAngebot->fetchData('offerID','description');
        $offerPrice = $abfrageEigenesAngebot->fetchData('offerID','price');
        $offerDate = $abfrageEigenesAngebot->fetchData('offerID','date');
        
        
    } else {
        die ("Bitte log dich ein: <a href='https://www.whocando.eu'> Login </a>");
    }
  
    
    echo "<form action='profil.php' method='POST'>";
    echo "<table>";
        echo "<tr>";
            echo "<td>";
                echo "Titel";
            echo "</td>";
            echo "<td>";
                echo "<input type='text' name='title'>";
            echo "</td>";
        echo "</tr>";
        echo "<tr>";
            echo "<td>";
                echo "Description";
            echo "</td>";
            echo "<td>";
                echo "<textarea name='description' cols='30' rows='10'></textarea>";
             echo "</td>";   
        echo "</tr>";
        echo "<tr>";
            echo "<td>";
                echo "Preis";
            echo "</td>";
            echo "<td>";
                echo "<input type='text' name='price'>";
            echo "</td>";
        echo "</tr>";
        echo "<tr>";
            echo "<td>";
                echo "<input type='hidden' name='eintragung' value=1>";
                echo "<input type='hidden' name='page' value='offers'>";
                echo "<input type='submit' value='Eintragen'>";
            echo "</td>";
        echo "</tr>";
    echo "</table>";
    echo "</form>";
    
    
    foreach($offerTitle as $offerID => $title) {
        echo "<form action='profil.php' method='POST'>";
        echo "<table>";
             echo "<th>".$title."</th>";
            echo "<tr>";
                echo "<td>";
                    echo $offerDescription[$offerID];
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                     echo $offerPrice[$offerID];
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo $offerDate[$offerID];
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<input type=hidden name=page value='offers'>";
                echo "<input type=hidden name=offerID value=".$offerID.">";
                echo "<td>";
                    echo "<input type=submit name='loeschen' value='Eintrag löschen'>";
                echo "</td>";
            echo "</tr>";
        echo "</table>";
        echo "</form>";
    }
?>