<?php
function getRandomImage() {
    $folder = "images/background/";
    $imageFiles = glob($folder . "*.svg"); // You can change the file extension as needed
    $randomIndex = array_rand($imageFiles);
    return $imageFiles[$randomIndex];
}

function getfile($folder, $type) {
    $api_url = 'http://localhost:5000/api/babelonche/database/import/'.$folder.'/'.$type;
    $response = file_get_contents($api_url);
    $data = json_decode($response, true);

    if ($data === null) {
        die('Erreur, la requête API a échoué');
    }
    return $data;
}
?>
