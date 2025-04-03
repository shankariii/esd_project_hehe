CREATE DATABASE IF NOT EXISTS `threshold` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `threshold`;

DROP TABLE IF EXISTS threshold;
CREATE TABLE IF NOT EXISTS threshold (
  threshold_id int NOT NULL AUTO_INCREMENT,
  ingredient varchar(255) NOT NULL UNIQUE,
  threshold decimal(10,2) NOT NULL,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (threshold_id)
);

INSERT INTO threshold (ingredient, threshold) VALUES
("Coffee Beans", 1200.00),
("Skim Milk", 120.50),
("Almond Milk", 1000.00),
("Chocolate Sprinkles", 30.00);