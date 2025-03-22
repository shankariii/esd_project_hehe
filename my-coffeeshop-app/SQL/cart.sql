-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 22, 2025 at 02:07 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cart`
--

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
) ENGINE=InnoDB AUTO_INCREMENT=10008 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `user_id`, `outlet_id`, `totalPrice`) VALUES
(10000, 'vPWKyHuXm9N', 1, 11.3),
(10001, 'vPWKyHuXm9N', 2, 12.9),
(10003, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 4.6),
(10004, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 7.6),
(10005, 'vPWKyHuXm9N', 1, 10.3),
(10006, 'vPWKyHuXm9N', 2, 5.9);

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
CREATE TABLE IF NOT EXISTS `cart_items` (
  `cart_items_id` int NOT NULL AUTO_INCREMENT,
  `cart_id_fk` int DEFAULT NULL,
  `drink_id` int DEFAULT NULL,
  `Quantity` int DEFAULT NULL,
  PRIMARY KEY (`cart_items_id`),
  KEY `cart_id_fk` (`cart_id_fk`)
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

-- --------------------------------------------------------

--
-- Table structure for table `cart_item_customisation`
--

DROP TABLE IF EXISTS `cart_item_customisation`;
CREATE TABLE IF NOT EXISTS `cart_item_customisation` (
  `cic_id` int NOT NULL AUTO_INCREMENT,
  `cart_item_id_fk` int DEFAULT NULL,
  `customisationId_fk` int DEFAULT NULL,
  PRIMARY KEY (`cic_id`),
  KEY `cart_item_id_fk` (`cart_item_id_fk`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart_item_customisation`
--

INSERT INTO `cart_item_customisation` (`cic_id`, `cart_item_id_fk`, `customisationId_fk`) VALUES
(1, 1, 4),
(2, 2, 2);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`cart_id_fk`) REFERENCES `cart` (`cart_id`);

--
-- Constraints for table `cart_item_customisation`
--
ALTER TABLE `cart_item_customisation`
  ADD CONSTRAINT `cart_item_customisation_ibfk_1` FOREIGN KEY (`cart_item_id_fk`) REFERENCES `cart_items` (`cart_items_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
