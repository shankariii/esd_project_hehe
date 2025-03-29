CREATE DATABASE IF NOT EXISTS `supplier_ingredient` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `supplier_ingredient`;

DROP TABLE IF EXISTS supplier_ingredient;
CREATE TABLE IF NOT EXISTS supplier_ingredient (
    ingredient varchar(100) NOT NULL,
    supplier_id int NOT NULL,
    price_per_unit decimal(10,2) NOT NULL,
    lead_time int NOT NULL,
    last_updated timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ingredient, supplier_id),
    KEY supplier_id (supplier_id)
);

-- Insert sample data into the supplier_ingredient table
INSERT INTO supplier_ingredient (ingredient, supplier_id, price_per_unit, lead_time) VALUES
("Coffee Beans", 2, 12.50, 5),
("Regular Milk", 3, 2.75, 2),
("Skim Milk", 2, 2.60, 2),
("Soy Milk", 2, 2.75, 2),
("Almond Milk", 3, 3.50, 2),
("Oat Milk", 3, 4.00, 2),
("Vanilla Syrup", 1, 5.95, 4),
("Caramel Syrup", 1, 6.25, 3),
("Hazelnut Syrup", 1, 7.50, 6),
("Chocolate Sprinkles", 1, 6.75, 3);