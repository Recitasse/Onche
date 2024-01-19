<?php

function getRandomImage() {
    $folder = "images/background/";
    $imageFiles = glob($folder . "*.svg"); // You can change the file extension as needed
    $randomIndex = array_rand($imageFiles);
    return $imageFiles[$randomIndex];
}

function loadbar_title($time, $label, $height) {
    $time = 100 * $time;
    $func = 'simulateLoading'.$label;
    echo '<div class="load_container"><p class="loading_info">'.$label.'</p>
    <progress class="progressBars" value="0" max="'.$time.'" style="background-color: #fff; progress::-moz-progress-bar { background: #fff; }
    progress::-webkit-progress-value { background: #fff; }; height: '.$height.'px;"></progress></div>
    <br/>';
}

function loadbar_sub($time, $label, $height) {
    $time = 100 * $time;
    $func = 'simulateLoading'.$label;
    echo '<li class="load"><div class="load_container_sub"><p class="loading_info_sub">'.$label.'</p>
    <progress class="progressBars" value="0" max="'.$time.'" style="background-color: #fff; progress::-moz-progress-bar { background: #fff; }
    progress::-webkit-progress-value { background: #fff; }; height: '.$height.'px; width: 80%;"></progress></div></li>';
}

# Déplacer le 2 fonctions qui suivent dans le fichier fonction
function getfile($folder, $type) {
    $api_url = 'http://localhost:5000/api/babelonche/general/import/'.$folder.'/'.$type;
    $response = file_get_contents($api_url);
    $data = json_decode($response, true);

    return $data;
}

function getAPI($url) {
    $response = file_get_contents($url);
    $data = json_decode($url, true);

    return $data;
}
?>
