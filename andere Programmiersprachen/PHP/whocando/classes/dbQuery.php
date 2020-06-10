<?php
class dbQuery {
    
    public $sqlCode;
    
    public function __construct($sqlCode) {
       $this->sqlCode = $sqlCode;
    }
    
    public function fetchData($index,$value) {
        
        include ('dbConnection.php');
        
        $statement = $mysqli->prepare($this->sqlCode);
        //$mysqli->set_charset("utf8");
        $statement->execute();
        
        $result = $statement->get_result();
        
        while ($row = $result->fetch_object()) {
            $wert = utf8_encode($row->$value);
            $array[$row->$index] = $wert;
        }     
        return $array; 
    }
}
