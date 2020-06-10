<?php
if (!isset($_SESSION)) {
    session_start();
}
?>

<html>
	
	<?php 
	   
    	function autoload ($className) {
    	    if (file_exists('classes/'.$className.'.php')) {
    	        require 'classes/'.$className.'.php';
    	    }
    	}
    	
    	spl_autoload_register("autoload");
    	
    	$userAbfrage = new dbQuery("SELECT id, name, firstName FROM db764570417.userdata");
    	$userName = $userAbfrage->fetchData('id', 'name');
    	$userIDName = $userAbfrage->fetchData('name','id');
    	$userFirstName = $userAbfrage->fetchData('id', 'firstName');
    	
    	foreach ($userName as $id => $name) {
    	    $userString .= "'".$userFirstName[$id]." ".$name."',";
    	    $completeUserNameID[$userFirstName[$id]." ".$userName[$id]] = $id;
    	    $completeUserName[$id] = $userFirstName[$id]." ".$userName[$id];
    	}
    	
    	$userString = substr($userString,0,-1);
    	
    	$uniAbfrage = new dbQuery("SELECT id, name FROM db764570417.universitydata");
    	$unis = $uniAbfrage->fetchData('id', 'name');
    	$university = $uniAbfrage->fetchData('name','id');
    	
    	foreach ($unis as $id => $name) {
    	    $uniString .= "'".$name."',";
    	}
    	
    	$uniString = substr($uniString,0,-1);
    	
    	?>
    	
	<head>
		<link rel="stylesheet" type="text/css" href="stylesheet.css" media="screen" />
		<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  		<link rel="stylesheet" href="/resources/demos/style.css">
		<meta charset="UTF-8" />
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
		<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  		<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
		<script>
            $(document).ready(function(){
              // Add smooth scrolling to all links
              $("a").on('click', function(event) {
            
                // Make sure this.hash has a value before overriding default behavior
                if (this.hash !== "") {
                  // Prevent default anchor click behavior
                  event.preventDefault();
            
                  // Store hash
                  var hash = this.hash;
            
                  // Using jQuery's animate() method to add smooth page scroll
                  // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
                  $('html, body').animate({
                    scrollTop: $(hash).offset().top
                  }, 800, function(){
               
                    // Add hash (#) to URL when done scrolling (default click behavior)
                    window.location.hash = hash;
                  });
                } // End if
              });

              //Toggle Function

              $(".loginField").click(function() {
                  $(".loginDetails").toggle("slow");
              });

              $(".profilName").click(function() {
                  $(".profilMenu").toggle("slow");
              });

              $("#middleLoginButton").click(function() {
                  $(".middleLoginForm").toggle("slow");
              });


              //Lightbox
              
              var heightUser = $(window).height();
              
              $('#registration').click(function() {
					$("body").append($.parseHTML("<div class='overlay'></div>"));
					$(".overlay").css("height",heightUser);
					alert(heightUser);
              });


              //Profilbild adjustment
              
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
 			 
              console.log(newHeightProfilePic);
              $('.pPicture').height(newHeightProfilePic);

			 
            
              //Slider

              //rotation speed and timer
                    var speed = 5000;
                    
                    var run = setInterval(rotate, speed);
                    var slides = $('.slide');
                    var container = $('#slides ul');
                    var elm = container.find(':first-child').prop("tagName");
                    var item_width = container.width();
                    var previous = 'prev'; //id of previous button
                    var next = 'next'; //id of next button
                    slides.width(item_width); //set the slides to the correct pixel width
                    container.parent().width(item_width);
                    container.width(slides.length * item_width); //set the slides container to the correct total width
                    container.find(elm + ':first').before(container.find(elm + ':last'));
                    resetSlides();
                    
                    
                    //if user clicked on prev button
                    
                    $('#buttons a').click(function (e) {
                        //slide the item
                        
                        if (container.is(':animated')) {
                            return false;
                        }
                        if (e.target.id == previous) {
                            container.stop().animate({
                                'left': 0
                            }, 1500, function () {
                                container.find(elm + ':first').before(container.find(elm + ':last'));
                                resetSlides();
                            });
                        }
                        
                        if (e.target.id == next) {
                            container.stop().animate({
                                'left': item_width * -2
                            }, 1500, function () {
                                container.find(elm + ':last').after(container.find(elm + ':first'));
                                resetSlides();
                            });
                        }
                        
                        //cancel the link behavior            
                        return false;
                        
                    }); 
                    
                    //if mouse hover, pause the auto rotation, otherwise rotate it    
                    container.parent().mouseenter(function () {
                        clearInterval(run);
                    }).mouseleave(function () {
                        run = setInterval(rotate, speed);
                    });
                    
                    
                    function resetSlides() {
                        //and adjust the container so current is in the frame
                        container.css({
                            'left': -1 * item_width
                        });
                    }

                    
            });

            function rotate() {
                $('#next').click();
            }

            //AutoComplete
			
            $( function() {
                
				var allUserArray = [<?php echo $userString; ?>];
				var allUniArray = [<?php echo $uniString ?>];
                
                $("#receiver").autocomplete({
                	source: allUserArray
                }); 

                $("#unis").autocomplete({
                	source: allUniArray
                });
                
            }); 


            
    	</script>
	</head>

	<body>
		<!-- getting UserData, if available -->
		<?php
		
		    //delete Session Data, if logout
    		if (isset($_GET['logout']) && $_GET['logout'] == 1) {
    		   session_destroy();
    		   $_SESSION = [];
    		   //header("Location:https://www.whocando.eu");
    		}
    		/*
    		function autoload ($className) {
    		    if (file_exists('classes/'.$className.'.php')) {
    		        require 'classes/'.$className.'.php';
    		    }
    		} */
    		
    		spl_autoload_register("autoload");
		    
		    if ($_GET['falsePassword'] == 1) {
		        $falsePassword = 1;
		    }
		    
		    if ((empty($_POST['userName']) || empty($_POST['password'])) && empty($_POST['registration']) && empty($_SESSION['userID'])) {
		        
		    // after Login Check! 
		    } elseif (isset($_POST['userName']) && isset($_POST['password']) && !isset($_POST['registration'])) {
                $loginCheck = new loginParser();
                $userID = $loginCheck->loginChecker($_POST['userName'],$_POST['password']);
                $_SESSION['userID'] = $userID;
                
                $abfrage = new dbQuery("SELECT ID,name, firstName, profilePicture FROM db764570417.userdata WHERE ID = '$userID'");
                $userName = $abfrage->fetchData('ID','name');
                $userFirstName = $abfrage->fetchData('ID','firstName');
                $userPicture = $abfrage->fetchData('ID','profilePicture');
                
            // already logged in Check!
		    } elseif (isset($_SESSION['userID'])) {
		        $userID = $_SESSION['userID'];
		        
		        $abfrage = new dbQuery("SELECT ID,name, firstName, profilePicture FROM db764570417.userdata WHERE ID = '$userID'");
		        $userName = $abfrage->fetchData('ID','name');
		        $userFirstName = $abfrage->fetchData('ID','firstName');
		        $userPicture = $abfrage->fetchData('ID','profilePicture');
		        
		    // after Registration Check!
		    } elseif (isset($_POST['registration'])) {
		        $name = utf8_decode($_POST['name']);
		        $vorName = utf8_decode($_POST['vorname']);
		        $email = utf8_decode($_POST['email']);
		        $uni = utf8_decode($_POST['uni']);
		        $city = utf8_decode($_POST['city']);
		        $geburtstag = utf8_decode($_POST['gebDatum']);
		        $password = utf8_decode($_POST['passwort']);
		        $confirmedPassword = utf8_decode($_POST['confirmPasswort']);
		        $gebDatum = date("Y-m-d",strtotime($geburtstag));
		        $abfrageEmail = new dbQuery("SELECT ID,email FROM db764570417.logindata");
		        $userEmails = $abfrageEmail->fetchData('ID','email');
		        
		        if ($password != $confirmedPassword) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=passwordNotMatched&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		             exit();
		        } elseif (in_array($email,$userEmails)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=emailAlreadyUses&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($name)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=nameMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        }elseif (empty($vorName)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=vorNameMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($email)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=emailMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($uni)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=uniMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($city)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=cityMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($geburtstag)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=gebMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($password)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=passwordMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } elseif (empty($confirmedPassword)) {
		            echo "<script type='text/javascript'>window.location.href = 'https://www.whocando.eu/registration.php?fault=confirmedPasswordMissing&name=".$name."&vorname=".$vorName."&email=".$email."&uni=".$uni."&gebDatum=".$geburtstag."&city=".$city."';</script>";
		            exit();
		        } else {
		            include ('dbConnection.php');
		            
		            $date = date("Y-m-d H:i:s",time());
		            $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
		            $sqlCode = "INSERT INTO db764570417.logindata (name,email,password)
                      VALUES (?,?,?)";
		            
		            $userNameDB = $vorName."".$name;

		            $statement = $mysqli->prepare($sqlCode);
		            $statement->bind_Param('sss',$userNameDB,$email,$hashedPassword);
		            $statement->execute();
		            $newUserId = $mysqli->insert_id;
		            
		            $_SESSION['userID'] = $newUserId;
		            
		            
		            $sqlCode = "INSERT INTO db764570417.userdata (ID,name,firstName,firstLogin,lastLogin,birthDate,email,university,city)
                          VALUES (?,?,?,?,?,?,?,?,?)";
		            
		            $statement = $mysqli->prepare($sqlCode);
		            $statement->bind_Param('issssssss',$newUserId,$name,$vorName,$date,$date,$gebDatum,$email,$university[$uni],$city);
		            
		            $statement->execute();
		            //header("Location:index.php");
		            
		            $userID = $newUserId;
		            $userFirstName[$userID] = $vorName;
		            $userName[$userID] = $name;
	
		        }
		    }
		    
		?>
		
		