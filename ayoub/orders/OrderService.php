<?php

class OrderService {
    private $db;

    public function __construct() {
        $host = getenv('DB_HOST') ?: 'postgres';
        $port = getenv('DB_PORT') ?: '5432';
        $dbname = getenv('DB_NAME') ?: 'orders_db';
        $user = getenv('DB_USER') ?: 'orders_user';
        $password = getenv('DB_PASSWORD') ?: 'orders_password';

        try {
            $this->db = new PDO(
                "pgsql:host=$host;port=$port;dbname=$dbname",
                $user,
                $password
            );
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            http_response_code(500);
            echo json_encode(['error' => 'Database connection failed: ' . $e->getMessage()]);
            exit;
        }
    }

    public function createOrder($data) {
        try {
            $this->db->beginTransaction();

            // Create order
            $stmt = $this->db->prepare("INSERT INTO orders (total) VALUES (0) RETURNING id");
            $stmt->execute();
            $orderId = $stmt->fetchColumn();

            $total = 0;
            foreach ($data['items'] as $item) {
                // Get product price from catalog service
                $productResponse = file_get_contents("http://catalog-service:3000/products/" . $item['product_id']);
                $product = json_decode($productResponse, true);

                if (!$product) {
                    throw new Exception("Product not found: " . $item['product_id']);
                }

                // Create order item
                $stmt = $this->db->prepare(
                    "INSERT INTO order_items (order_id, product_id, product_name, price) 
                     VALUES (?, ?, ?, ?)"
                );
                $stmt->execute([
                    $orderId,
                    $item['product_id'],
                    $product['name'],
                    $product['price']
                ]);

                $total += $product['price'] * $item['quantity'];
            }

            // Update order total
            $stmt = $this->db->prepare("UPDATE orders SET total = ? WHERE id = ?");
            $stmt->execute([$total, $orderId]);

            $this->db->commit();
            return ['id' => $orderId, 'total' => $total];
        } catch (Exception $e) {
            $this->db->rollBack();
            throw $e;
        }
    }

    public function getOrder($id) {
        $stmt = $this->db->prepare("
            SELECT o.*, json_agg(json_build_object(
                'id', oi.id,
                'product_id', oi.product_id,
                'product_name', oi.product_name,
                'price', oi.price
            )) as items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.id = ?
            GROUP BY o.id
        ");
        $stmt->execute([$id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    public function getAllOrders() {
        $stmt = $this->db->query("
            SELECT o.*, json_agg(json_build_object(
                'id', oi.id,
                'product_id', oi.product_id,
                'product_name', oi.product_name,
                'price', oi.price
            )) as items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            GROUP BY o.id
        ");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
} 