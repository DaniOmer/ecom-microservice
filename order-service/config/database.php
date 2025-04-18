<?php

class Database {
    private static $instance = null;
    private $conn;

    private function __construct() {
        $host = getenv('DB_HOST') ?: 'postgres';
        $port = getenv('DB_PORT') ?: '5432';
        $dbname = getenv('DB_NAME') ?: 'orders_db';
        $user = getenv('DB_USER') ?: 'orders_user';
        $password = getenv('DB_PASSWORD') ?: 'orders_password';

        try {
            $this->conn = new PDO(
                "pgsql:host=$host;port=$port;dbname=$dbname",
                $user,
                $password
            );
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch(PDOException $e) {
            die("Connection failed: " . $e->getMessage());
        }
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->conn;
    }
} 