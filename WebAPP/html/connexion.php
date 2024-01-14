<?php
include_once "header.php";

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
    }
    else {
        echo "<p>❌ La connexion à la base de donnée est <span class='bad'>inactive</span>.</p>";
    }
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
            ?>
        </div>
    </div>
</div>

<?php
include_once "footer.php";
?>