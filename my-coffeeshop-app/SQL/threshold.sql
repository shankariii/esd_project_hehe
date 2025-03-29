CREATE DATABASE IF NOT EXISTS `threshold` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `threshold`;

DROP TABLE IF EXISTS threshold;
CREATE TABLE IF NOT EXISTS threshold (
  threshold_id int NOT NULL AUTO_INCREMENT,
  supplier_id int NOT NULL,
  ingredient varchar(255) NOT NULL,
  threshold decimal(10,2) NOT NULL,
  safety_stock decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (threshold_id),
  UNIQUE KEY unique_supplier_ingredient (supplier_id, ingredient)
);

INSERT INTO threshold (supplier_id, ingredient, threshold, safety_stock) VALUES
(2, "Coffee Beans", 80.00, 10.00),
(2, "Skim Milk", 75.50, 15.00),
(3, "Almond Milk", 30.00, 5.00),
(1, "Chocolate Sprinkles", 20.00, 3.00);