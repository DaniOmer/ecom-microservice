<?php
header('Content-Type: application/json');

require_once 'OrderService.php';

$orderService = new OrderService();

$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$pathParts = explode('/', trim($path, '/'));

try {
    switch ($method) {
        case 'GET':
            if (count($pathParts) === 1 && $pathParts[0] === 'orders') {
                // Get all orders
                echo json_encode($orderService->getAllOrders());
            } elseif (count($pathParts) === 2 && $pathParts[0] === 'orders') {
                // Get order by ID
                $order = $orderService->getOrder($pathParts[1]);
                if ($order) {
                    echo json_encode($order);
                } else {
                    http_response_code(404);
                    echo json_encode(['error' => 'Order not found']);
                }
            } else {
                http_response_code(404);
                echo json_encode(['error' => 'Route not found']);
            }
            break;

        case 'POST':
            if (count($pathParts) === 1 && $pathParts[0] === 'orders') {
                // Create new order
                $data = json_decode(file_get_contents('php://input'), true);
                if (!$data || !isset($data['items'])) {
                    http_response_code(400);
                    echo json_encode(['error' => 'Invalid request data']);
                    break;
                }
                $result = $orderService->createOrder($data);
                http_response_code(201);
                echo json_encode($result);
            } else {
                http_response_code(404);
                echo json_encode(['error' => 'Route not found']);
            }
            break;

        default:
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            break;
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => $e->getMessage()]);
} 