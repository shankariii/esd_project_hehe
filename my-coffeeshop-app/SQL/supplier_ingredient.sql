CREATE DATABASE IF NOT EXISTS `supplier_ingredient` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `supplier_ingredient`;

DROP TABLE IF EXISTS supplier_ingredient;
CREATE TABLE IF NOT EXISTS supplier_ingredient (
    ingredient varchar(100) NOT NULL,
    supplier_id int NOT NULL,
    price_per_unit decimal(10,2) NOT NULL,
    lead_time int NOT NULL,
    last_updated timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ingredient)
);

-- Insert sample data into the supplier_ingredient table
-- INSERT INTO supplier_ingredient (ingredient, supplier_id, price_per_unit, lead_time) VALUES
-- ("Coffee Beans", 2, 12.90, 3),
-- ("Regular Milk", 3, 2.75, 2),
-- ("Skim Milk", 2, 2.60, 2),
-- ("Soy Milk", 2, 2.75, 2),
-- ("Almond Milk", 3, 3.50, 2),
-- ("Oat Milk", 3, 4.00, 2),
-- ("Vanilla Syrup", 1, 5.95, 4),
-- ("Caramel Syrup", 1, 6.25, 3),
-- ("Hazelnut Syrup", 1, 7.50, 4),
-- ("Chocolate Sprinkles", 1, 6.75, 3),
-- ("Whipped Cream", 3, 4.50, 2);

INSERT INTO supplier_ingredient (ingredient, supplier_id, price_per_unit, lead_time) VALUES
-- Coffee (price per g)
("Coffee Beans", 2, 0.012, 3),

-- Dairy & Alternatives (price per ML)
("Regular Milk", 3, 0.0025, 2),          
("Skim Milk", 2, 0.0023, 2),             
("Soy Milk", 2, 0.0026, 2),              
("Almond Milk", 3, 0.0032, 2),            
("Oat Milk", 3, 0.0035, 2),               

-- Syrups (price per ML)
("Vanilla Syrup", 1, 0.0066, 4),        
("Caramel Syrup", 1, 0.0070, 3),          
("Hazelnut Syrup", 1, 0.0080, 4),         
("Sugar Syrup", 1, 0.0047, 2),           
("Chocolate Syrup", 1, 0.0067, 3),   

-- Toppings & Extras (price per g)
("Chocolate Sprinkles", 1, 0.028, 3),     
("Whipped Cream", 3, 0.0038, 2),         
("Matcha Powder", 2, 0.12, 4);             