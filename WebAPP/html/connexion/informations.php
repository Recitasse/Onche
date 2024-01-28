<?php
include_once "header.php";
include "../function/style.php";

$forum_array = array(0 => "babla général", 1 => "suggestions et réclamations", 2 => "plus de 18 ans", 3 => "goulag", 4 => "forum des anciens", 5 => "modération", 6 => "finance & crypto", 7 => "jeux vidéo", 8 => "autonomie & lifehack");

$api_url = 'http://localhost:5000/api/babelonche/mysql/state';
$response = file_get_contents($api_url);
$data = json_decode($response, true);

$data1 = $data['state'];

$api_url = 'http://localhost:5000/api/babelonche/mysql/info';
$response = file_get_contents($api_url);
$data2 = json_decode($response, true);

$api_url = 'http://localhost:5000/api/babelonche/database/info';
$response = file_get_contents($api_url);
$data3 = json_decode($response, true);
?>

<div class="page">
    <?php
    if (isset($_GET['result']) && !empty($_GET['result'])) {
        $result = $_GET['result'];
        if ($result == 1) {
            echo "<p>✅ La base de donnée a été modifié.</p>";
        }
        else {
            echo "<p>❌ <span class='bad'>ERREUR</span>, impossible de changer de base donnée";
        }
    }
    ?>
    <div class="babel">
    <div class="babel_titre">
        <p class="terminal"><img src="../images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée</p>
    </div>
    <div class="linux">
        <?php
        if ($_SESSION['mysql'] == TRUE) {
            foreach ($data2 as $key => $value) {
                echo $value. "<br>";
            }
            echo "<br><span class='comment'># Database info messages #</span><br>";
            $it = 0;
            foreach ($data3['Messages'] as $key => $value) {
                echo $forum_array[$it]. " : ".$value. "<br>";
                $it += 1;
            }
            echo "<br><span class='comment'># Database info topics #</span><br>";
            $it = 0;
            foreach ($data3['Topics'] as $key => $value) {
                echo $forum_array[$it]. " : ".$value. "<br>";
                $it += 1;
            }
            echo "<br><span class='comment'># Database info Onchois #</span><br>";
            echo $data3['Onchois'];
        }
        else {
            echo "<p>Vous n'êtes connecté à aucune base de donnée</p>";
        }
        ?>
    </div>
</div>
    </div>
    <?php
include_once "../footer.php";
?>