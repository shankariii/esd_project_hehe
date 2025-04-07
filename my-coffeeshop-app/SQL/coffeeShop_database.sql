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

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `customisation`
--

-- --------------------------------------------------------

--
-- Table structure for table `customisation`
--

DROP TABLE IF EXISTS `drink_customisations`;
CREATE TABLE IF NOT EXISTS `drink_customisations` (
  `customisation_id` int NOT NULL,
  `customisation_type` varchar(10) NOT NULL,
  `name` varchar(32) NOT NULL,
  `price_diff` decimal(4,2) NOT NULL,
  `CIID` int NOT NULL,
  PRIMARY KEY (`customisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Table structure for table `drink_customisations`
--

INSERT INTO `drink_customisations` (`customisation_id`, `customisation_type`, `name`, `price_diff`, `CIID`) VALUES
(1, 'S', 'Small', 0.00, 101),
(2, 'S', 'Medium', 0.50, 102),
(3, 'S', 'Large', 0.80, 103),
(4, 'M', 'Regular', 0.00, 104),
(5, 'M', 'Skim', 0.00, 105),
(6, 'M', 'Almond', 0.75, 106),
(7, 'M', 'Oat', 0.75, 107),
(8, 'M', 'Soy', 0.75, 108),
(9, 'A', 'Vanilla Syrup', 0.50, 109),
(10, 'A', 'Caramel Syrup', 0.50, 110),
(11, 'A', 'Hazelnut Syrup', 0.50, 111),
(12, 'A', 'Whipped Cream', 0.50, 112),
(13, 'A', 'Chocolate Sprinkles', 0.25, 113);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


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
	  (4, 'Coffee Beans', 10, 'g'),

    -- Iced Matcha Latte (Drink ID 5)
    (5, 'Matcha Powder', 5, 'g'),
	  (5, 'Sugar Syrup', 15, 'ml'),

    -- Iced Chocolate (Drink ID 6)
    (6, 'Chocolate Syrup', 30, 'ml'),

	
    (104, 'Regular Milk', 200, 'ml'),
    (105, 'Skim Milk', 200, 'ml'),
    (106, 'Almond Milk', 200, 'ml'),
    (107, 'Oat Milk', 200, 'ml'),
    (108, 'Soy Milk', 200, 'ml'),
    (109, 'Vanilla Syrup', 30, 'ml'),
    (110, 'Caramel Syrup', 30, 'ml'),
    (111, 'Hazelnut Syrup', 30, 'ml'),
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
(5, 'Iced Matcha Latte', 'A refreshing blend of premium matcha green tea, creamy milk, and a touch of sweetness, served chilled over ice. Perfect for matcha lovers seeking a cool, invigorating treat.', 6.00, 'Iced_match_latte.png', 4.00, 'Yes'),
(6, 'Iced Chocolate', 'Rich, velvety chocolate mixed with chilled milk and ice, delivering a decadent, indulgent experience. A satisfying choice for chocolate enthusiasts looking to cool down.', 2.50, 'iced_chocolate.png', 4.00, 'Yes'),
(7, 'Spiced Chai Latte', 'A warming blend of black tea, cinnamon, cardamom, and spices with steamed milk for a cozy, aromatic flavor.', 4.00, 'spiced_chai_latte.png', 4.50, 'Yes'),
(8, 'Cold Brew', 'Smooth, slow-steeped coffee brewed cold for a bold yet refreshing taste, perfect for a caffeine kick.', 5.50, 'cold_brew.png', 4.20, 'Yes'),
(9, 'Iced Vanilla Latte', 'Chilled espresso blended with milk and sweet vanilla syrup, served over ice for a smooth, creamy delight.', 5.00, 'Iced_vanilla_latte.png', 4.50, 'Yes');
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
-- Coffee Beans 
('Coffee Beans', 3500.00, 'g', '2025-03-30 07:15:00', -40.00),
('Coffee Beans', 3460.00, 'g', '2025-03-30 12:30:00', -30.00),
('Coffee Beans', 3400.00, 'g', '2025-03-31 08:00:00', -60.00),
('Coffee Beans', 3340.00, 'g', '2025-03-31 14:20:00', -40.00),
('Coffee Beans', 3270.00, 'g', '2025-04-01 09:45:00', -70.00),
('Coffee Beans', 3200.00, 'g', '2025-04-02 07:30:00', -50.00),
('Coffee Beans', 3150.00, 'g', '2025-04-02 16:00:00', -30.00),
('Coffee Beans', 3080.00, 'g', '2025-04-03 08:15:00', -70.00),
('Coffee Beans', 3000.00, 'g', '2025-04-04 10:30:00', -80.00),
('Coffee Beans', 2920.00, 'g', '2025-04-05 11:00:00', -60.00),
('Coffee Beans', 2860.00, 'g', '2025-04-05 18:30:00', -40.00),
('Coffee Beans', 2800.00, 'g', '2025-04-06 07:45:00', -60.00),
('Coffee Beans', 2740.00, 'g', '2025-04-06 12:45:00', -60.00),

-- Regular Milk 
('Regular Milk', 10000.00, 'ml', '2025-03-30 07:30:00', -200.00),
('Regular Milk', 9800.00, 'ml', '2025-03-30 13:45:00', -150.00),
('Regular Milk', 9600.00, 'ml', '2025-03-31 08:45:00', -250.00),
('Regular Milk', 9350.00, 'ml', '2025-04-01 09:00:00', -300.00),
('Regular Milk', 9050.00, 'ml', '2025-04-02 10:15:00', -200.00),
('Regular Milk', 8850.00, 'ml', '2025-04-03 11:30:00', -180.00),
('Regular Milk', 8600.00, 'ml', '2025-04-04 14:00:00', -250.00),
('Regular Milk', 8350.00, 'ml', '2025-04-05 09:30:00', -200.00),
('Regular Milk', 8150.00, 'ml', '2025-04-06 08:00:00', -150.00),
('Regular Milk', 8000.00, 'ml', '2025-04-06 12:00:00', -150.00),

-- Skim Milk
('Skim Milk', 4000.00, 'ml', '2025-03-30 08:15:00', -200.00), 
('Skim Milk', 3800.00, 'ml', '2025-03-31 11:30:00', -200.00),  
('Skim Milk', 3600.00, 'ml', '2025-04-02 14:00:00', -200.00),  
('Skim Milk', 3400.00, 'ml', '2025-04-04 09:45:00', -400.00),  
('Skim Milk', 3000.00, 'ml', '2025-04-06 10:30:00', -200.00),   

-- Almond Milk
('Almond Milk', 3000.00, 'ml', '2025-03-30 10:00:00', -200.00), 
('Almond Milk', 2800.00, 'ml', '2025-04-01 13:20:00', -200.00),  
('Almond Milk', 2600.00, 'ml', '2025-04-03 16:45:00', -200.00),  
('Almond Milk', 2400.00, 'ml', '2025-04-05 12:15:00', -400.00),  
('Almond Milk', 2000.00, 'ml', '2025-04-06 12:45:00', -400.00),  

-- Oat Milk
('Oat Milk', 5000.00, 'ml', '2025-03-30 09:30:00', -200.00), 
('Oat Milk', 4800.00, 'ml', '2025-03-31 15:00:00', -200.00),    
('Oat Milk', 4600.00, 'ml', '2025-04-02 10:30:00', -200.00),    
('Oat Milk', 4400.00, 'ml', '2025-04-04 17:30:00', -400.00),    
('Oat Milk', 4000.00, 'ml', '2025-04-06 11:45:00', -200.00),   

-- Soy Milk
('Soy Milk', 3500.00, 'ml', '2025-03-30 11:00:00', -200.00),
('Soy Milk', 3300.00, 'ml', '2025-04-01 14:10:00', -200.00),    
('Soy Milk', 3100.00, 'ml', '2025-04-03 12:40:00', -200.00),    
('Soy Milk', 2900.00, 'ml', '2025-04-05 15:20:00', -400.00),

-- Matcha Powder
('Matcha Powder', 200.00, 'g', '2025-03-30 11:00:00', -5.00),
('Matcha Powder', 195.00, 'g', '2025-03-31 15:00:00', -5.00),  
('Matcha Powder', 190.00, 'g', '2025-04-01 16:30:00', -5.00),   
('Matcha Powder', 185.00, 'g', '2025-04-03 12:00:00', -5.00),
('Matcha Powder', 180.00, 'g', '2025-04-04 13:45:00', -5.00),
('Matcha Powder', 175.00, 'g', '2025-04-05 16:45:00', -5.00),
('Matcha Powder', 170.00, 'g', '2025-04-05 10:20:00', -5.00),

-- Sugar Syrup (15ml per matcha drink - paired with matcha powder data)
('Sugar Syrup', 800.00, 'ml', '2025-03-30 11:00:00', -15.00),
('Sugar Syrup', 785.00, 'ml', '2025-03-31 15:00:00', -15.00),  
('Sugar Syrup', 770.00, 'ml', '2025-04-01 16:30:00', -15.00),    
('Sugar Syrup', 755.00, 'ml', '2025-04-03 12:00:00', -15.00),    
('Sugar Syrup', 740.00, 'ml', '2025-04-04 13:45:00', -15.00),    
('Sugar Syrup', 725.00, 'ml', '2025-04-05 16:45:00', -15.00),  
('Sugar Syrup', 710.00, 'ml', '2025-04-06 10:20:00', -15.00), 

-- Chocolate Syrup 
('Chocolate Syrup', 1000.00, 'ml', '2025-03-30 09:00:00', -60.00),  
('Chocolate Syrup', 940.00, 'ml', '2025-03-30 14:30:00', -45.00), 
('Chocolate Syrup', 895.00, 'ml', '2025-03-31 10:30:00', -60.00),
('Chocolate Syrup', 835.00, 'ml', '2025-04-01 13:15:00', -60.00),
('Chocolate Syrup', 775.00, 'ml', '2025-04-02 11:20:00', -45.00), 
('Chocolate Syrup', 730.00, 'ml', '2025-04-03 08:45:00', -60.00),
('Chocolate Syrup', 670.00, 'ml', '2025-04-04 16:00:00', -45.00), 
('Chocolate Syrup', 625.00, 'ml', '2025-04-05 11:20:00', -60.00),
('Chocolate Syrup', 565.00, 'ml', '2025-04-06 10:15:00', -45.00),
('Chocolate Syrup', 520.00, 'ml', '2025-04-06 13:15:00', -45.00),


-- Whipped Cream
('Whipped Cream', 500.00, 'g', '2025-03-30 08:00:00', -20.00),  
('Whipped Cream', 480.00, 'g', '2025-03-30 12:00:00', -40.00), 
('Whipped Cream', 440.00, 'g', '2025-03-31 14:00:00', -40.00),  
('Whipped Cream', 400.00, 'g', '2025-04-01 14:30:00', -40.00), 
('Whipped Cream', 360.00, 'g', '2025-04-02 09:45:00', -40.00), 
('Whipped Cream', 320.00, 'g', '2025-04-03 10:00:00', -40.00), 
('Whipped Cream', 280.00, 'g', '2025-04-04 17:00:00', -60.00), 
('Whipped Cream', 220.00, 'g', '2025-04-05 13:15:00', -80.00),   
('Whipped Cream', 140.00, 'g', '2025-04-06 09:45:00', -40.00),   
('Whipped Cream', 100.00, 'g', '2025-04-06 13:30:00', -20.00),

-- Vanilla Syrup
('Vanilla Syrup', 750.00, 'ml', '2025-03-30 08:30:00', -45.00),
('Vanilla Syrup', 705.00, 'ml', '2025-03-31 11:45:00', -30.00),
('Vanilla Syrup', 675.00, 'ml', '2025-04-01 15:20:00', -45.00),
('Vanilla Syrup', 630.00, 'ml', '2025-04-03 09:30:00', -30.00),
('Vanilla Syrup', 600.00, 'ml', '2025-04-04 12:15:00', -45.00),
('Vanilla Syrup', 555.00, 'ml', '2025-04-05 14:50:00', -60.00),
('Vanilla Syrup', 495.00, 'ml', '2025-04-06 11:50:00', -60.00),


-- Caramel Syrup
('Caramel Syrup', 600.00, 'ml', '2025-03-30 10:15:00', -30.00),
('Caramel Syrup', 570.00, 'ml', '2025-03-31 13:30:00', -45.00),
('Caramel Syrup', 525.00, 'ml', '2025-04-02 08:20:00', -30.00),
('Caramel Syrup', 495.00, 'ml', '2025-04-03 14:10:00', -45.00),
('Caramel Syrup', 450.00, 'ml', '2025-04-05 10:40:00', -60.00),
('Caramel Syrup', 390.00, 'ml', '2025-04-06 10:45:00', -60.00),

-- Chocolate Sprinkles
('Chocolate Sprinkles', 200.00, 'g', '2025-03-30 11:30:00', -4.00),  
('Chocolate Sprinkles', 196.00, 'g', '2025-03-31 09:15:00', -8.00),   
('Chocolate Sprinkles', 188.00, 'g', '2025-03-31 16:45:00', -4.00),  
('Chocolate Sprinkles', 184.00, 'g', '2025-04-02 10:50:00', -8.00),  
('Chocolate Sprinkles', 176.00, 'g', '2025-04-03 14:20:00', -4.00),  
('Chocolate Sprinkles', 172.00, 'g', '2025-04-04 15:30:00', -12.00),  
('Chocolate Sprinkles', 160.00, 'g', '2025-04-05 12:20:00', -16.00), 
('Chocolate Sprinkles', 144.00, 'g', '2025-04-06 10:00:00', -8.00),  
('Chocolate Sprinkles', 136.00, 'g', '2025-04-06 12:30:00', -4.00);

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