-- cart_items_customisation

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cart_items_customisation`
--
CREATE DATABASE IF NOT EXISTS `cart_items_customisation` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `cart_items_customisation`;

-- --------------------------------------------------------

--
-- Table structure for table `cart_items_customisation`
--

DROP TABLE IF EXISTS `cart_items_customisation`;
CREATE TABLE IF NOT EXISTS `cart_items_customisation` (
  `cic_id` int NOT NULL AUTO_INCREMENT,
  `cart_item_id_fk` int NOT NULL,
  `customisationId_fk` int NOT NULL,
  PRIMARY KEY (`cic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart_items_customisation`
--

INSERT INTO `cart_items_customisation` (`cic_id`, `cart_item_id_fk`, `customisationId_fk`) VALUES
(1, 1, 4),
(2, 2, 2);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- cart_items

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cart_items`
--
CREATE DATABASE IF NOT EXISTS `cart_items` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `cart_items`;

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
CREATE TABLE IF NOT EXISTS `cart_items` (
  `cart_items_id` int NOT NULL AUTO_INCREMENT,
  `cart_id_fk` int NOT NULL,
  `drink_id` int NOT NULL,
  `Quantity` int NOT NULL,
  PRIMARY KEY (`cart_items_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`cart_items_id`, `cart_id_fk`, `drink_id`, `Quantity`) VALUES
(1, 10000, 1, 2),
(2, 10000, 2, 5),
(5, 10006, 1, 2),
(6, 10003, 1, 2),
(8, 10003, 2, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- cart
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cart`
CREATE DATABASE IF NOT EXISTS `cart` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `cart`;


-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
CREATE TABLE IF NOT EXISTS `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(45) NOT NULL,
  `outlet_id` int NOT NULL,
  `totalPrice` float NOT NULL,
  PRIMARY KEY (`cart_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10078 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `user_id`, `outlet_id`, `totalPrice`) VALUES
(10000, 'vPWKyHuXm9N', 1, 11.3),
(10001, 'vPWKyHuXm9N', 2, 12.9),
(10003, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 18.6),
(10004, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 7.6);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- drink_customisation
DROP SCHEMA IF EXISTS customisation;

create schema customisation;

use customisation;

create table if not exists `customisation`
(customisation_id int not null,
customisation_type varchar(10) not null,
name varchar(32) not null, 
price_diff decimal(4, 2) not null,
constraint customisation_id_pk primary key (customisation_id));

    
insert into customisation (customisation_id, customisation_type, name, price_diff)
values 
	(1, "S", "Small", 0.00),
	(2, "S", "Medium", 0.50),
	(3, "S", "Large", 0.80),
	(4, "M", "Regular", 0.00),
	(5, "M", "Skim", 0.00),
	(6, "M", "Almond", 0.75),
	(7, "M", "Oat", 0.75),
	(8, "M", "Soy", 0.75),
	(9, "A", "Vanilla Syrup", 0.50),
	(10, "A", "Caramel Syrup", 0.50),
	(11, "A", "Hazelnut Syrup", 0.50),
	(12, "A", "Whipped Cream", 0.50),
	(13, "A", "Chocolate Sprinkles", 0.25);


select * from customisation;
-- drink_ingredients
DROP SCHEMA IF EXISTS drink_ingredients;

create schema drink_ingredients;

use drink_ingredients;

create table drink_ingredients
(drink_ingredient_id int not null auto_increment,
drink_id int,
ingredient varchar(255) not null,
quantity int not null,
unit varchar(15) not null,
constraint drink_ingredient_id_pk primary key (drink_ingredient_id));

insert into drink_ingredients (drink_id, ingredient, quantity, unit)
values 

	-- Espresso (Drink ID 1)
    (1, 'Coffee Beans', 10, 'g'),

    -- Latte (Drink ID 2)
    (2, 'Coffee Beans', 10, 'g'),

    -- Cappuccino (Drink ID 3)
    (3, 'Coffee Beans', 10, 'g'),

    -- Americano (Drink ID 4)
	(4, 'Coffee Beans', 15, 'g'),

    -- Iced Matcha Latte (Drink ID 5)
    (5, 'Matcha Powder', 5, 'g'),
	(5, 'Sugar Syrup', 1, 'tbsp'),

    -- Iced Chocolate (Drink ID 6)
    (6, 'Chocolate Syrup', 2, 'tbsp'),

	
	(104, 'Regular Milk', 200, 'ml'),
	(105, 'Skim Milk', 200, 'ml'),
	(106, 'Almond Milk', 200, 'ml'),
	(107, 'Oat Milk', 200, 'ml'),
	(108, 'Soy Milk', 200, 'ml'),
	(109, 'Vanilla Syrup', 2, 'tbsp'),
	(110, 'Caramel Syrup', 2, 'tbsp'),
	(111, 'Hazelnut Syrup', 2, 'tbsp'),
	(112, 'Whipped Cream', 20, 'g'),
	(113, 'Chocolate Sprinkles', 4, 'g');
    

select * from drink_ingredients;

-- drink_menu
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 28, 2025 at 10:21 AM
-- Server version: 8.3.0
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `drink_menu`
CREATE DATABASE IF NOT EXISTS `drink_menu` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `drink_menu`;


-- --------------------------------------------------------

--
-- Table structure for table `drink_menu`
--

DROP TABLE IF EXISTS `drink_menu`;
CREATE TABLE IF NOT EXISTS `drink_menu` (
  `drink_id` int NOT NULL AUTO_INCREMENT,
  `drink_name` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `prep_time_min` decimal(5,2) NOT NULL,
  `available` varchar(10) NOT NULL,
  PRIMARY KEY (`drink_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drink_menu`
--

INSERT INTO `drink_menu` (`drink_id`, `drink_name`, `description`, `price`, `image`, `prep_time_min`, `available`) VALUES
(1, 'Espresso', 'A bold and concentrated shot of rich, aromatic coffee, perfect for those who love a strong caffeine kick.', 3.00, 'espresso.png', 2.00, 'Yes'),
(2, 'Latte', 'Smooth and creamy, this espresso-based drink is blended with steamed milk and topped with a light layer of foam for a balanced, velvety taste.', 4.50, 'latte.webp', 4.00, 'Yes'),
(3, 'Cappuccino', 'A classic favorite with equal parts espresso, steamed milk, and frothy foam, delivering a rich, robust flavor with a light, airy texture.', 4.00, 'cappuccino.png', 6.00, 'Yes'),
(4, 'Americano', 'A simple yet satisfying mix of espresso and hot water, creating a smooth, mellow coffee with a slightly lighter body than a traditional espresso.', 5.50, 'americano.png', 1.00, 'Yes'),
(5, 'Iced Matcha Latte', 'A refreshing blend of premium matcha green tea, creamy milk, and a touch of sweetness, served chilled over ice. Perfect for matcha lovers seeking a cool, invigorating treat.', 6.00, 'iced_matcha_latte.jpg', 4.00, 'Yes'),
(6, 'Iced Chocolate', 'Rich, velvety chocolate mixed with chilled milk and ice, delivering a decadent, indulgent experience. A satisfying choice for chocolate enthusiasts looking to cool down.', 2.50, 'iced_chocolate.jpg', 2.00, 'Yes');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- inventory
CREATE DATABASE IF NOT EXISTS `inventory` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `inventory`;

DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    ingredient VARCHAR(64) NOT NULL,
    available_quantity FLOAT(10,2) NOT NULL,
    unit VARCHAR(32) NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    change_in_quantity FLOAT(10,2) DEFAULT 0.00
);

INSERT INTO inventory (ingredient, available_quantity, unit, date_time, change_in_quantity) VALUES

    # Coffee Beans
    ('Coffee Beans', 1500.0, 'g', '2025-03-27 10:00:00', -60.0),
    ('Coffee Beans', 1440.0, 'g', '2025-03-28 12:00:00', -50.0),
    ('Coffee Beans', 1390.0, 'g', '2025-03-29 09:00:00', -40.0),
    ('Coffee Beans', 1350.0, 'g', '2025-03-29 17:00:00', -30.0),
    ('Coffee Beans', 1320.0, 'g', '2025-03-30 11:00:00', -55.0),
    ('Coffee Beans', 1265.0, 'g', '2025-03-31 15:00:00', -45.0),
    ('Coffee Beans', 1220.0, 'g', '2025-04-01 08:00:00', -35.0),
    ('Coffee Beans', 1185.0, 'g', '2025-04-02 13:00:00', -65.0),
    ('Coffee Beans', 1120.0, 'g', '2025-04-03 09:00:00', -40.0),

    # Almond Milk
    ('Almond Milk', 1250.0, 'ml', '2025-03-27 08:00:00', -25.0),
    ('Almond Milk', 1225.0, 'ml', '2025-03-28 09:00:00', -30.0),
    ('Almond Milk', 1195.0, 'ml', '2025-03-29 11:00:00', -20.0),
    ('Almond Milk', 1175.0, 'ml', '2025-03-30 07:00:00', -15.0),
    ('Almond Milk', 1160.0, 'ml', '2025-03-30 18:00:00', -10.0),
    ('Almond Milk', 1150.0, 'ml', '2025-03-31 10:00:00', -25.0),
    ('Almond Milk', 1125.0, 'ml', '2025-04-01 14:00:00', -10.0),
    ('Almond Milk', 1115.0, 'ml', '2025-04-02 08:00:00', -10.0),
    ('Almond Milk', 1105.0, 'ml', '2025-04-03 10:00:00', -20.0); 

-- outlet
-- phpMyAdmin SQL Dump
-- Database: `outlet`

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS `outlet` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `outlet`;

-- Drop and recreate the outlets table
DROP TABLE IF EXISTS `outlets`;
CREATE TABLE IF NOT EXISTS `outlets` (
  `outlet_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `address` TEXT NOT NULL,
  `latitude` FLOAT NOT NULL,
  `longitude` FLOAT NOT NULL,
  `contact_info` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`outlet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert sample data
INSERT INTO `outlets` (`name`, `address`, `latitude`, `longitude`, `contact_info`) VALUES
('Orchard Rd', '2 Orchard Turn, #B2 - 09, Singapore 238801', 1.30453350, 103.83167718, '62389283'),
('SMU', '70 Stamford Rd, #B1-25 Li Ka Shing Library, SMU 178901', 1.29643403, 103.84995523, '67239283'),
('Changi Airport', '80 Airport Blvd, Singapore Changi Airport, Singapore 819642', 1.364420, 103.991531, '65412345'),
('Tiong Bahru', '56 Eng Hoon St, Tiong Bahru Estate, Singapore 160056', 1.285364, 103.828412, '62224455'),
('Jurong East', '3 Gateway Drive, #01-18, Westgate, Singapore 608532', 1.333180, 103.742125, '68901234'),
('Tampines Hub', '1 Tampines Walk, Singapore 528523', 1.352083, 103.940415, '67894567'),
('Paya Lebar Quarter', '10 Paya Lebar Rd, #01-28, Singapore 409057', 1.317300, 103.892400, '63887766');

COMMIT;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `payment_log`
--
CREATE DATABASE IF NOT EXISTS `payment_log` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `payment_log`;

-- --------------------------------------------------------

--
-- Table structure for table `payment_log`
--

DROP TABLE IF EXISTS `payment_log`;
CREATE TABLE IF NOT EXISTS `payment_log` (
  `payment_log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(50) NOT NULL,
  `order_id` int NOT NULL,
  `amount` float NOT NULL,
  `payment_id` varchar(15) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `outlet_id` int NOT NULL,
  PRIMARY KEY (`payment_log_id`),
  UNIQUE KEY `transaction_id` (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

use payment_log;

--
-- Dumping data for table `payment_log`
--

INSERT INTO `payment_log` (`payment_log_id`, `user_id`, `order_id`, `amount`, `payment_id`, `payment_status`, `created_at`, `outlet_id`) VALUES
(1, '1', 1001, 10, 'TXN123456', 'Completed', '2025-03-30 14:00:04', 0),
(2, '2', 1002, 15, 'TXN123457', 'Pending', '2025-03-30 14:00:04', 0),
(3, '3', 1003, 20, 'TXN123458', 'Failed', '2025-03-30 14:00:04', 0),
(4, '4', 1004, 30, 'TXN123459', 'Completed', '2025-03-30 14:00:04', 0),
(5, '5', 1005, 25, 'TXN123460', 'Refunded', '2025-03-30 14:00:04', 0),
(6, '0', 0, 23, 'pi_3R8kh4QRYfaB', 'pending', '2025-03-31 07:56:11', 2),
(7, '0', 0, 23, 'pi_3R8kkgQRYfaB', 'pending', '2025-03-31 07:59:55', 2),
(8, '0', 0, 23, 'pi_3R8ks9QRYfaB', 'pending', '2025-03-31 08:07:38', 2),
(9, '0', 0, 23, 'pi_3R8kvDQRYfaB', 'pending', '2025-03-31 08:10:48', 2),
(10, '0', 0, 23, 'pi_3R8kvIQRYfaB', 'pending', '2025-03-31 08:10:53', 2),
(11, '12332', 10042, 10.8, 'pi_3R8yHEQRYfaB', 'success', '2025-03-31 22:33:43', 7),
(12, '0', 10080, 23, 'pi_3R93ScQRYfaB', 'succeeded', '2025-04-01 03:58:44', 2),
(13, 'test24', 10080, 23, 'pi_3R97F4QRYfaB', 'succeeded', '2025-04-01 08:00:59', 2),
(14, 'test24', 10080, 23, 'pi_3R97JuQRYfaB', 'succeeded', '2025-04-01 08:06:02', 2),
(15, 'test24', 10082, 13.5, 'pi_3R97NoQRYfaB', 'succeeded', '2025-04-01 08:10:04', 6),
(16, 'test24', 10083, 4, 'pi_3R97VKQRYfaB', 'succeeded', '2025-04-01 08:17:50', 1),
(17, 'test24', 10084, 4, 'pi_3R97Z7QRYfaB', 'succeeded', '2025-04-01 08:21:44', 7),
(18, 'test24', 10084, 4, 'pi_3R97arQRYfaB', 'succeeded', '2025-04-01 08:23:27', 7),
(19, 'test24', 10085, 3, 'pi_3R97bTQRYfaB', 'succeeded', '2025-04-01 08:24:12', 3),
(20, 'test24', 10086, 22, 'pi_3R97hHQRYfaB', 'requires_payment_met', '2025-04-01 08:30:17', 3),
(22, 'test24', 10087, 10.25, 'pi_3R97qgQRYfaB', 'succeeded', '2025-04-01 08:39:48', 5),
(23, 'test24', 10083, 12.25, 'pi_3R97ysQRYfaB', 'succeeded', '2025-04-01 08:48:17', 1),
(24, 'test24', 10088, 13.8, 'pi_3R9859QRYfaB', 'succeeded', '2025-04-01 08:54:46', 3),
(25, 'test24', 10089, 4.5, 'pi_3R9868QRYfaB', 'requires_payment_met', '2025-04-01 08:55:51', 3),
(26, 'test24', 10089, 4.5, 'pi_3R988qQRYfaB', 'succeeded', '2025-04-01 08:58:37', 3),
(27, 'test24', 10083, 16.25, 'pi_3R98jVQRYfaB', 'succeeded', '2025-04-01 09:36:43', 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- profile

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `profile`
CREATE DATABASE IF NOT EXISTS `profile` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `profile`;

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
CREATE TABLE IF NOT EXISTS `profile` (
  `userId` varchar(45) NOT NULL,
  `userName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phoneNum` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `userId_UNIQUE` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`userId`, `userName`, `email`, `phoneNum`) VALUES
('iTeYSJ3xoBQuDdI0uXravnQgbqo2', 'gogo', 'gogo@gmail.com', '95434237'),
('randoootext', 'JuJuss', 'juju@gmail.com.sg', '93434597'),
('vPWKyHuXm9Np4YHoZE7grVeEZay2', 'yoyo', 'yoyo@gmail.com', '91234567');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- supplier_ingredient
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
-- supplier 
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
-- threshold 
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