<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include_once "../function/global.php";

RestartAPI();

function plugged($val) {
    if ($val == FALSE) {
        echo '<a href="connexion/connexion.php" style="color: black; text-decoration: none;" title="Se connecter à MySQL"><img class="plug" src="../images/icon/unplugged.png" alt="déco" style="height: 3em; vertical-align: middle; position: absolute; left: 0;"></a>';
    }
    else {
        echo '<a href="connexion/connexion.php" style="color: black; text-decoration: none;" title="Se déconnecter de MySQL"><img class="plug" src="../images/icon/plugged.png" alt="déco" style="height: 3em; vertical-align: middle; position: absolute; left: 0;"></a>';
    }
}

session_start();
if (!isset($_SESSION['mysql']) && empty($_SESSION['mysql'])) {
    $_SESSION['mysql'] = FALSE;
}

?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Babel Onche</title>
    <link rel="stylesheet" href="../style.css">
    <link rel="shortcut icon" href="../images/icon/main.ico" type="image/x-icon">
</head>
<body>
    <div class="top_enca">
            <div class="main_titre">
                <h1><?php plugged($_SESSION["mysql"]);?><a href="../index.php" style="color: black; text-decoration: none;" title="Menu principal">BABEL <img src="../images/icon/main.ico" alt="logo">NCHE</h1></a>
            </div>
        <div class="menu">
            <nav>
                <ul class="horizontal-menu">
                    <li>
                        <a href="#">Queries</a>
                        <ul class="submenu">
                            <li><a href="#">Prédéfinie</a></li>
                            <li><a href="#">Manuelle</a></li>
                        </ul>
                    </li>
                    <li>
                        <a href="#">Topics</a>
                        <ul class="submenu">
                            <li><a href="#">Recherche 🔍</a></li>
                            <li><a href="#">Boucle 🔂</a></li>
                        </ul>
                    </li>
                    <li>
                    <a href="#">Onchois <img src="../images/icon/onche.png" alt="" style="vertical-align: middle;width: 20px; height: 20px;"></a>
                    <ul class="submenu">
                        <li><a href="../onchois/recherche.php">Recherche 🔍</a></li>
                        <li><a href="#">Constellation 🕸️</a></li>
                        <li><a href="#">Communautés 🌐</a></li>
                        <li><a href="#">Réplicant 🤖</a></li>
                    </ul>
                    </li>
                    <li>
                        <a href="#">Paramètres ⚙️</a>
                        <ul class="submenu">
                            <li><a href="connexion.php">Connexion 📶</a></li>
                            <li><a href="base_de_donnee.php">Base de donnée 💾</a></li>
                            <li><a href="informations.php">Informations ℹ️</a></li>
                            <li><a href="aide.php">Aide ♿</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
        </div>
    </div>