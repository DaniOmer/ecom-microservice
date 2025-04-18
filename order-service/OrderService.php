<?php
require_once 'config/database.php';

function getProduct($id) {
    $url = "http://catalog-service:3000/products/$id";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    
    if ($response === false) {
        error_log("Error fetching product from catalog service: " . curl_error($ch));
        curl_close($ch);
        return null;
    }
    
    curl_close($ch);
    $product = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log("Error decoding JSON response from catalog service: " . json_last_error_msg());
        return null;
    }
    
    return $product;
}

function createOrder(array $productIds) {
    $db = Database::getInstance()->getConnection();
    
    try {
        $db->beginTransaction();
        
        // Create order with UUID
        $stmt = $db->prepare("INSERT INTO orders (total) VALUES (0) RETURNING id");
        $stmt->execute();
        $orderId = $stmt->fetchColumn();
        
        $total = 0;
        $orderItems = [];
        
        // Add products to order
        foreach ($productIds as $pid) {
            $product = getProduct($pid);
            if ($product && isset($product["price"])) {
                $stmt = $db->prepare("
                    INSERT INTO order_items (order_id, product_id, product_name, price)
                    VALUES (?, ?, ?, ?)
                ");
                $stmt->execute([
                    $orderId,
                    $pid,
                    $product["name"] ?? "Unknown Product",
                    $product["price"]
                ]);
                
                $total += $product["price"];
            }
        }
        
        // Update order total
        $stmt = $db->prepare("UPDATE orders SET total = ? WHERE id = ?");
        $stmt->execute([$total, $orderId]);
        
        $db->commit();
        
        return getOrder($orderId);
    } catch (Exception $e) {
        $db->rollBack();
        throw $e;
    }
}

function getOrder($id) {
    $db = Database::getInstance()->getConnection();
    
    // Get order
    $stmt = $db->prepare("
        SELECT id, created_at, total
        FROM orders
        WHERE id = ?
    ");
    $stmt->execute([$id]);
    $order = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$order) {
        return ["error" => "Order not found"];
    }
    
    // Get order items
    $stmt = $db->prepare("
        SELECT product_id, product_name, price
        FROM order_items
        WHERE order_id = ?
    ");
    $stmt->execute([$id]);
    $items = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    $order["products"] = $items;
    return $order;
}

/**
 * Get all orders
 */
function getAllOrders() {
    $db = Database::getInstance()->getConnection();
    
    // Get all orders
    $stmt = $db->prepare("
        SELECT id, created_at, total
        FROM orders
        ORDER BY created_at DESC
    ");
    $stmt->execute();
    $orders = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get items for each order
    foreach ($orders as &$order) {
        $stmt = $db->prepare("
            SELECT product_id, product_name, price
            FROM order_items
            WHERE order_id = ?
        ");
        $stmt->execute([$order['id']]);
        $order['products'] = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    
    return $orders;
}
