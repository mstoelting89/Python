
<?php
    
    echo "<button><a href='profil.php?page=messages&messageSystem=inbox'>Eingang</a></button>";
    echo "<button><a href='profil.php?page=messages&messageSystem=outbox'>Ausgang</a></button>";
    echo "<button><a href='profil.php?page=messages&messageSystem=write'>Nachricht schreiben</a></button>";
    
    include('dbConnection.php');
    
    if (empty($_GET['messageSystem']) || $_GET['messageSystem'] == 'inbox') {
        
        $userID = $_SESSION['userID'];
        
        $abfrageMessages = new dbQuery("SELECT id,date,sender,receiver,subject,message
                                        FROM db764570417.messagesdata
                                        WHERE receiver = $userID
                                        ORDER BY date DESC");
        
        $messagesDate = $abfrageMessages->fetchData('id', 'date');
        $messagesSender = $abfrageMessages->fetchData('id','sender');
        $messagesSubject = $abfrageMessages->fetchData('id', 'subject');
        $messagesContent = $abfrageMessages->fetchData('id','message');
        
        echo "<table>";
            echo "<th>Datum</th>";
            echo "<th>Sender</th>";
            echo "<th>Betreff</th>";
            
            foreach ($messagesDate as $id => $date) {
                echo "<tr>";
                    echo "<td>";
                        echo $date;
                    echo "</td>";
                    echo "<td>";
                         echo $completeUserName[$messagesSender[$id]];
                    echo "</td>";
                    echo "<td>";
                        echo $messagesSubject[$id];
                    echo "</td>";
               echo "</tr>";
            }
        echo "</table>";
        
    } elseif ($_GET['messageSystem'] == 'outbox') {
        $userID = $_SESSION['userID'];
        
        $abfrageMessages = new dbQuery("SELECT id,date,sender,receiver,subject,message
                                        FROM db764570417.messagesdata
                                        WHERE sender = $userID
                                        ORDER BY date DESC");
        
        $messagesDate = $abfrageMessages->fetchData('id', 'date');
        $messagesSender = $abfrageMessages->fetchData('id','sender');
        $messagesReceiver = $abfrageMessages->fetchData('id','receiver');
        $messagesSubject = $abfrageMessages->fetchData('id', 'subject');
        $messagesContent = $abfrageMessages->fetchData('id','message');
        
        echo "<table>";
            echo "<th>Datum</th>";
            echo "<th>Empfänger</th>";
            echo "<th>Betreff</th>";
            
            foreach ($messagesDate as $id => $date) {
                echo "<tr>";
                    echo "<td>";
                        echo $date;
                    echo "</td>";
                    echo "<td>";
                        echo $completeUserName[$messagesReceiver[$id]];
                    echo "</td>";
                    echo "<td>";
                        echo $messagesSubject[$id];
                    echo "</td>";
                echo "</tr>";
            }
        echo "</table>";
        
    } elseif ($_GET['messageSystem'] == 'write') {
        
        if ($_POST['messageSent'] == 1) {
            
            $date = date("Y-m-d H:i:s",time());
            $receiver = $_POST['receiver'];
            $sender = $_SESSION['userID'];
            $subject = $_POST['subject'];
            $message = nl2br($_POST['messageContent']);
           
            
            $sqlCode = "INSERT INTO db764570417.messagesdata (date,sender,receiver,subject,message)
                      VALUES (?,?,?,?,?)";

		            $statement = $mysqli->prepare($sqlCode);
		            $statement->bind_Param('siiss',$date,$sender,$completeUserNameID[$receiver],$subject,$message);
		            if ($statement->execute()) {
		                echo "Nachricht wurde gesendet";
		            } else {
		                echo "Nachricht konnte nicht gesendet werden";
		            } 
        }
        
        echo "<form action='profil.php?page=messages&messageSystem=write' method='POST'>";
        echo "<table>";
            echo "<tr>";
                echo "<td>";
                    echo "Empfänger:";
                echo "</td>";
                echo "<td>";
                    echo "<input type='text' name='receiver' id='receiver'>";
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Betreff:";
                echo "</td>";
                echo "<td>";
                    echo "<input type='text' name='subject'>";
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo "<td>";
                    echo "Nachricht:";
                echo "</td>";
                echo "<td>";
                    echo "<textarea cols=40 rows=10 name='messageContent'></textarea>";
                echo "</td>";
            echo "</tr>";
            echo "<tr>";
                echo"<td>";
                    echo "<input type='hidden' name='messageSent' value=1>";
                    echo "<input type='submit'>";
                echo "</td>";
            echo "</tr>";
       echo "</table>";
       echo "</form>";
    }
    ?>