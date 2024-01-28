<?php
include_once "header.php";
include "../function/style.php";
$api_url = 'http://localhost:5000/api/babelonche/database/import';
$response = file_get_contents($api_url);
$data = json_decode($response, true);
?>

<div class="page">
    <div class="babel">
        <div class="babel_titre">
            <p class="terminal"><img src="../images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée <b>SERVER</b></p>
        </div>
        <div class="files">
            <form action="../function/submit.php" method="post">
            <?php
                if ($data[0] != "none") {
                    $files = getfile("BDD_import_server","sql");
                    foreach ($files as $key => $value) {
                        echo "<input type='radio' value=$value name='bdd'><img src='../images/icon/database.png' alt='icon database' style='vertical-align: middle;width: 25px; height: 25spx;'>$value<br>";
                    }
                }
            ?>
        </div>
    </div>
    <p><i>Expérimental (version >= 0.9.1) base de donnée locale avec sqlite</i></p>
    <div class="babel">
        <div class="babel_titre">
            <p class="terminal"><img src="../images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée <b>LOCALE</b></p>
        </div>
        <div class="files">
            <form action="../function/submit.php" method="post">
            <?php
                if ($data[0] != "none") {
                    $files = getfile("BDD_import_local","db");
                    foreach ($files as $key => $value) {
                        echo "<input type='radio' value=$value name='bdd'><img src='../images/icon/database.png' alt='icon database' style='vertical-align: middle;width: 25px; height: 25spx;'>$value<br>";
                    }
                }
            ?>
        </div>
    </div>
    <?php
    if ($data[0] == "none") {
        echo "<p>⚠️ Aucune base de donnée ne se trouve dans le répertoire.</p>";
    }
    else {
        ?>
        <button class="submit">Changer de base de donnée</button>
        <?php
    }
    ?>
    </form>
</div>
<?php
include_once "../footer.php";
?>