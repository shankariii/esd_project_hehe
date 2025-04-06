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
-- Coffee Beans (in GRAMS)
("Coffee Beans", 2500), 

-- Milks (in ML)
("Regular Milk", 5000),      
("Skim Milk", 4000),         
("Soy Milk", 3000),         
("Almond Milk", 2000),       
("Oat Milk", 2500),          

-- Syrups (in ML)
("Vanilla Syrup", 750),
("Caramel Syrup", 500),    
("Hazelnut Syrup", 500),    
("Sugar Syrup", 1000),       
("Chocolate Syrup", 600),    

-- Toppings (in GRAMS)
("Chocolate Sprinkles", 100),
("Whipped Cream", 500),  

("Matcha Powder", 50);       