-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 28, 2025 at 10:30 AM
-- Server version: 9.0.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory`
--

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
CREATE TABLE IF NOT EXISTS `inventory` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `ingredient` varchar(64) NOT NULL,
  `available_quantity` float NOT NULL,
  `unit` varchar(32) NOT NULL,
  `date_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `change_in_quantity` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`inventory_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `ingredient`, `available_quantity`, `unit`, `date_time`, `change_in_quantity`) VALUES
(1, 'Regular Milk', 100, 'ml', '2025-03-28 18:25:01', 100),
(2, 'Oat milk', 150, 'ml', '2025-03-28 18:25:01', -20),
(3, 'Whipped Cream', 200, 'ml', '2025-03-28 18:25:01', 300),
(4, 'Almond Milk', 300, 'ml', '2025-03-28 18:25:01', 200),
(5, 'Coffee Beans', 50, 'g', '2025-03-28 18:25:01', -20),
(6, 'Soy Milk', 75, 'ml', '2025-03-28 18:25:01', -50);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
