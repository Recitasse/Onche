<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['bdd']) && !empty($_POST['bdd']))
    {
        $name = $_POST['bdd'];
        $name = strip_tags(trim($name));
    
        $api_url = 'http://localhost:5000/api/babelonche/database/import/change/'.$name;
        $response = file_get_contents($api_url);
        $data = json_decode($response, true);
        if ($data == TRUE) {
            header("location: ../base_de_donnee.php?result=1");
            exit;
        }
        else {
            header("location: ../base_de_donnee.php?result=0");
            exit;
        }
    }
}