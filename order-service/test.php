<?php
// Simple health check file
header('Content-Type: application/json');
echo json_encode(['status' => 'ok', 'timestamp' => date('Y-m-d H:i:s')]);
?>
