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

-- Insert sample data
INSERT INTO supplier (name, contact_person, phone, email, address) VALUES
('Sweet Additions Co.', 'Jane Lim', '65087328', 'jane@sweetadditions.com', '45 Orchard Street, Orchard City'),
('Cafe Supply Network', 'Robert Chua', '65432943', 'robert@cafesupply.com', '78 Shenton Road, East Town'),
('Brew & Beverage Wholesale', 'John Tan', '67543254', 'john@brewbev.com', '123 Bishan Street, West Town');