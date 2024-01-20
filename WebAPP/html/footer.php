<?php

$api_url = 'http://localhost:5000/api/babelonche/general/info';
$response = file_get_contents($api_url);
$data = json_decode($response, true);

?>

</body>
<footer>
    <div class="bot_enca">
        <p>Développé par <b><?php echo $data["Créateur"][0];?></b> v.<i><?php echo $data['version'];?></i> BDD <b><?php echo $data['BDD'];?></b> du <?php echo $data['DATE'];?>.</p>
    </div>
</footer>
</html>