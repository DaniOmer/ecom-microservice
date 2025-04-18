<?php
header('Content-Type: application/json');

try {
    $host = getenv('DB_HOST') ?: 'postgres';
    $port = getenv('DB_PORT') ?: '5432';
    $dbname = getenv('DB_NAME') ?: 'orders_db';
    $user = getenv('DB_USER') ?: 'orders_user';
    $password = getenv('DB_PASSWORD') ?: 'orders_password';

    $db = new PDO(
        "pgsql:host=$host;port=$port;dbname=$dbname",
        $user,
        $password
    );
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    echo json_encode(['status' => 'healthy', 'database' => 'connected']);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['status' => 'unhealthy', 'error' => $e->getMessage()]);
} 