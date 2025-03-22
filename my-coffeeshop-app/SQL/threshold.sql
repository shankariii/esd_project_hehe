DROP TABLE IF EXISTS threshold;
CREATE TABLE IF NOT EXISTS threshold (
  threshold_id int NOT NULL AUTO_INCREMENT,
  supplier_id int NOT NULL,
  ingredient_id int NOT NULL,
  threshold decimal(10,2) NOT NULL,
  safety_stock decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (threshold_id),
  UNIQUE KEY unique_supplier_ingredient (supplier_id, ingredient_id)
);

INSERT INTO threshold (supplier_id, ingredient_id, threshold, safety_stock) VALUES
(2, 1, 80.00, 10.00),
(2, 1, 2, 75.50, 15.00),
(3, 2, 3, 30.00, 5.00),
(4, 3, 4, 100.00, 20.00);