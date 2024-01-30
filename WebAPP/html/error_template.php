<?php
include_once "header.php";
include "function/style.php";
$api_url = 'http://localhost:5000/api/babelonche/database/import';
$response = file_get_contents($api_url);
$data = json_decode($response, true);
?>

<div class="page">
    <div class="erreur-cont">
        <img src="/images/icon/erreur.png" alt="Erreur" class="erreur-icone">
    </div>
</div>


<?php
include_once "footer.php";
?>