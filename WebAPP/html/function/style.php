<?php
function getRandomImage() {
    $folder = "images/background/";
    $imageFiles = glob($folder . "*.svg"); // You can change the file extension as needed
    $randomIndex = array_rand($imageFiles);
    return $imageFiles[$randomIndex];
}
?>
