<?php
require_once 'OrderService.php';

$uri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

header('Content-Type: application/json');

if ($uri === '/orders' && $method === 'POST') {
    // Create a new order
    $data = json_decode(file_get_contents('php://input'), true);
    $productIds = $data['productIds'] ?? [];
    echo json_encode(createOrder($productIds));
} elseif ($uri === '/orders' && $method === 'GET') {
    // Get all orders
    echo json_encode(getAllOrders());
} elseif (preg_match('#^/orders/([a-f0-9\-]+)$#i', $uri, $matches) && $method === 'GET') {
    // Get a specific order by UUID
    $id = $matches[1];
    echo json_encode(getOrder($id));
} else {
    http_response_code(404);
    echo json_encode(["error" => "Route not found"]);
}
