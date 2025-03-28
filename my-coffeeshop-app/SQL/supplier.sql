CREATE DATABASE IF NOT EXISTS `supplier` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `supplier`;

DROP TABLE IF EXISTS supplier;
CREATE TABLE IF NOT EXISTS supplier (
  supplier_id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  contact_person varchar(255) DEFAULT NULL,
  phone varchar(8) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  address text,
  created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (supplier_id),
  UNIQUE KEY email (email)
);

DROP TABLE IF EXISTS supplier_ingredient;
CREATE TABLE IF NOT EXISTS supplier_ingredient (
    ingredient varchar(255) NOT NULL,
    supplier_id int NOT NULL,
    price_per_unit decimal(10,2) NOT NULL,
    lead_time int NOT NULL,
    last_updated timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (ingredient, supplier_id),
    KEY supplier_id (supplier_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE CASCADE
);

-- Insert sample data into the supplier table
INSERT INTO supplier (name, contact_person, phone, email, address) VALUES
('Sweet Additions Co.', 'Jane Lim', '65087328', 'jane@sweetadditions.com', '45 Orchard Street, Orchard City'),
('Cafe Supply Network', 'Robert Chua', '65432943', 'robert@cafesupply.com', '78 Shenton Road, East Town'),
('Brew & Beverage Wholesale', 'John Tan', '67543254', 'john@brewbev.com', '123 Bishan Street, West Town');

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