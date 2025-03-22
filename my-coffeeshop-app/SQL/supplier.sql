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
  ingredient_id int NOT NULL,
  supplier_id int NOT NULL,
  price_per_unit decimal(10,2) NOT NULL,
  lead_time int NOT NULL,
  last_updated timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (ingredient_id, supplier_id),
  KEY supplier_id (supplier_id)
);

-- Insert sample data into the supplier table
INSERT INTO supplier (name, contact_person, phone, email, address) VALUES
('Fresh Produce Co.', 'John Tan', '67543254', 'john@freshproduce.com', '123 Bishan Street, West Town'),
('Organic Supplies Ltd.', 'Jane Lim', '65087328', 'jane@organicsupplies.com', '45 Orchard Street, Orchard City'),
('Global Spices', 'Robert Chua', '65432943', 'robert@globalspices.com', '78 Shenton Road, East Town');

-- Insert sample data into the supplier_ingredient table
INSERT INTO supplier_ingredient (ingredient_id, supplier_id, price_per_unit, lead_time) VALUES
(1, 2, 6.55, 3),
(2, 1, 1.75, 3),
(3, 2, 5.00, 7),
(4, 3, 3.25, 4),
(5, 3, 5.45, 2),
(6, 2, 9.95, 9);