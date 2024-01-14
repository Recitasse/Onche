<?php
include_once "header.php";

$forum_array = array(0 => "babla général", 1 => "suggestions et réclamations", 2 => "plus de 18 ans", 3 => "goulag", 4 => "forum des anciens", 5 => "modération", 6 => "finance & crypto", 7 => "jeux vidéo", 8 => "autonomie & lifehack");

$api_url = 'http://localhost:5000/api/babelonche/mysql';
$response = file_get_contents($api_url);
$data = json_decode($response, true);

if ($data === null) {
    die('Erreur, la requête API a échoué');
}

$api_url = 'http://localhost:5000/api/babelonche/connexion';
$response = file_get_contents($api_url);
$data2 = json_decode($response, true);

if ($data2 === null) {
    die('Erreur, la requête API a échoué');
}

$api_url = 'http://localhost:5000/api/babelonche/database/info';
$response = file_get_contents($api_url);
$data3 = json_decode($response, true);

if ($data3 === null) {
    die('Erreur, la requête API a échoué');
}

?>

<div class="page">
    <div class="babel">
        <div class="babel_titre">
            <p class="terminal"><img src="images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée</p>
        </div>
        <div class="linux">
            <?php
            foreach ($data['state'] as $key => $value) {
                echo $value. "<br>";
            }
            ?>
        </div>
    </div>
    <?php
    if ($data['running']  == TRUE) {
        echo "<p>✅ La connexion à la base de donnée est <span class='good'>active</span>.</p>";
        ?>
        <div class="babel">
        <div class="babel_titre">
            <p class="terminal"><img src="images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée</p>
        </div>
        <div class="linux">
            <?php
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
            echo "<br><span class='comment'># Database info topics #</span><br>";
            echo $data3['Onchois'];
            ?>
        </div>
    </div>
    <?php
    }
    else {
        echo "<p>❌ La connexion à la base de donnée est <span class='bad'>inactive</span>.</p>";
    }
    ?>
</div>

<?php
#include_once "footer.php";
?>