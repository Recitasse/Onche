<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['bdd']) && !empty($_POST['bdd']))
    {
        $name = $_POST['bdd'];
        $name = strip_tags(trim($name));
    
        $api_url = 'http://localhost:5000/api/babelonche/database/import/change/'.$name;
        $response = file_get_contents($api_url);
        $data = json_decode($response, true);
        if ($data == TRUE) {
            header("location: ../connexion.php?result=1&reload=1");
            exit;
        }
        header("location: ../connexion.php?result=0&reload=1");
        exit;
    }
    elseif (isset($_POST['connect_bdd']) && !empty($_POST['connect_bdd'])) {
        if (!isset($_POST['pass']) || empty($_POST['pass'])) {
            header("location: ../connexion.php?errpass=1");
        }
        $pass = $_POST['pass'];
        $api_url = 'http://localhost:5000/api/babelonche/mysql/start/'.$pass;
        $response = file_get_contents($api_url);
        $data = json_decode($response, true);
        $_SESSION['mysql'] = TRUE;
        if ($data == TRUE) {
            header("location: ../connexion.php?start=1&reload=1");
            exit;
        }
        header("location: ../connexion.php?errsub=1");
        exit;
    }
    elseif (isset($_POST['deconnect_bdd']) && !empty($_POST['deconnect_bdd'])) {
        if (!isset($_POST['pass']) || empty($_POST['pass'])) {
            header("location: ../connexion.php?errpass=1");
        }
        $pass = $_POST['pass'];
        echo var_dump($_POST);
        $api_url = 'http://localhost:5000/api/babelonche/mysql/stop/'.$pass;
        $response = file_get_contents($api_url);
        $data = json_decode($response, true);
        $_SESSION['mysql'] = FALSE;
        if ($data == TRUE) {
            header("location: ../connexion.php?stop=1&reload=1");
            exit;
        }
        header("location: ../connexion.php?errsub=1");
        exit;
    }
}
?>