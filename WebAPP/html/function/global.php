<?php

function APIRunning() {
    $apiUrl = 'http://127.0.0.1:5000';
    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if (curl_errno($ch)) {
        return TRUE;
    }
    return FALSE;
}

function RestartAPI() {
    $is_running = APIRunning();
    if ($is_running != TRUE) {
        $pythonScript = "../API/main.py";
        $result = shell_exec("python3 $pythonScript 2>&1");
    }
}