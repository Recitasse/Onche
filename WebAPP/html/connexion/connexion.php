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

$Cond = FALSE;
if (isset($_GET['reload']) && !empty($_GET['reload'])) {
    $reload = $_GET['reload'];
    if ($reload == 1) {
        $Cond = TRUE;
    }
}
# Si on a un chargement :
if ($Cond == TRUE) {
    ?>
    <div class="page">
        <div class="center">
            <img class="loading-image" src="../images/icon/main.ico" alt="Loading">
        </div>
        <?php
        loadbar_title(1, "Changement de la base de donnée", 20);
        ?>
    </div>
    <script>
        const bars = document.getElementsByClassName('progressBars');

        function startProgress(bars, index = 0) {
        const bar = bars[index];
        if (!bar) return;

        const id = setInterval(() => {
            if (bar.value < bar.max) bar.value++;
            else {
            clearInterval(id);
            startProgress(bars, index + 1);
            }
        }, 10);
        }

        startProgress(bars);
    </script>
    <?php
    if (isset($_GET['result']) && !empty($_GET['result'])) {
        $result=$_GET['result'];
        header("refresh: 1; url=connexion/connexion.php?result=$result");
        exit;
    }
    elseif (isset($_GET['stop']) && !empty($_GET['stop'])) {
        $result=$_GET['stop'];
        header("refresh: 1; url=connexion/connexion.php?stop=$result");
        exit;
    }
    elseif (isset($_GET['start']) && !empty($_GET['start'])) {
        $result=$_GET['start'];
        header("refresh: 1; url=connexion/connexion.php?start=$result");
        exit;
    }
}
else {
    ?>
    <div class="page">
        <?php
            if (isset($_GET['stop']) && !empty($_GET['stop'])) {
                $result=$_GET['stop'];
                if ($result == 1) {
                    echo "<p>✅ La connexion MySQL est <span class='good'>innactive</span>.</p>";
                }
            }
            elseif (isset($_GET['start']) && !empty($_GET['start'])) {
                $result=$_GET['start'];
                if ($result == 1) {
                    echo "<p>✅ La connexion MySQL est <span class='good'>active</span>.</p>";
                }
            }
        ?>
        <div class="babel">
            <div class="babel_titre">
                <p class="terminal"><img src="../images/icon/main.ico" alt="icone" style="height: 2.5em; vertical-align: middle;"> Terminal de la base de donnée</p>
            </div>
            <div class="linux">
                <?php
                foreach ($data1 as $key => $value) {
                    echo $value. "<br>";
                }
                ?>
            </div>
        </div>
        <?php
        if ($data['running']  == TRUE) {
            echo "<p>✅ La base de donnée MySQL est <span class='good'>active</span>.</p>";
            $_SESSION['mysql'] = TRUE;
            echo '<form action="../function/submit.php" method="post">';
            echo '<input type="password" placeholder="Votre mot de passe" class="password" name="pass">';
            echo '<button class="submit_deco" style="margin-bottom: 30px;" name="deconnect_bdd" value=1>Arrêter MySQL</button>';
            echo '</form>';
        }
        else {
            echo "<p>❌ La base de donnée MySQL est <span class='bad'>inactive</span>.</p>";
            echo '<form action="../function/submit.php" method="post">';
            echo '<input type="password" placeholder="Votre mot de passe" class="password" name="pass">';
            echo '<button class="submit_co" style="margin-bottom: 30px;" name="connect_bdd" value=1>Démarrer MySQL</button>';
            echo '</form>';
        }
        }
        ?>
    </div>
<?php
include_once "../footer.php";
?>