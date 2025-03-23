-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 22, 2025 at 03:49 PM
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
-- Database: `drink`
CREATE DATABASE IF NOT EXISTS `drink` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `drink`;

-- --------------------------------------------------------

--
-- Table structure for table `customisation`
--

DROP TABLE IF EXISTS `customisation`;
CREATE TABLE IF NOT EXISTS `customisation` (
  `customisation_id` int NOT NULL,
  `customisation_type` varchar(10) NOT NULL,
  `name` varchar(32) NOT NULL,
  `price_diff` decimal(4,2) NOT NULL,
  PRIMARY KEY (`customisation_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customisation`
--

INSERT INTO `customisation` (`customisation_id`, `customisation_type`, `name`, `price_diff`) VALUES
(1, "S", "Small", 0.00),
(2, "S", "Medium", 0.50),
(3, "S", "Large", 0.80),
(4, "M", "Regular", 0.00),
(5, "M", "Skim", 0.00),
(6, "M", "Almond", 0.75),
(7, "M", "Oat", 0.75),
(8, "M", "Soy", 0.75),
(9, "A", "Vanialla Syrup", 0.50),
(10, "A", "Caramel Syrup", 0.50),
(11, "A", "Hazelnut Syrup", 0.50),
(12, "A", "Whipped Syrup", 0.50),
(13, "A", "Choclate Sprinkles", 0.25);

-- --------------------------------------------------------

--
-- Table structure for table `drink_ingredients`
--

DROP TABLE IF EXISTS `drink_ingredients`;
CREATE TABLE IF NOT EXISTS `drink_ingredients` (
  `drink_ingredient_id` int NOT NULL AUTO_INCREMENT,
  `drink_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `quantity` int NOT NULL,
  `unit` varchar(15) NOT NULL,
  PRIMARY KEY (`drink_ingredient_id`),
  KEY `drink_id_fk` (`drink_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drink_ingredients`
--

INSERT INTO `drink_ingredients` (`drink_ingredient_id`, `drink_id`, `ingredient_id`, `quantity`, `unit`) VALUES
(1, 1, 3, 2, 'ounces'),
(2, 2, 4, 100, 'ml');

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
  PRIMARY KEY (`drink_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `drink_menu`
--

INSERT INTO `drink_menu` (`drink_id`, `drink_name`, `description`, `price`, `image`, `prep_time_min`) VALUES
(1, 'Espresso', 'A bold and concentrated shot of rich, aromatic coffee, perfect for those who love a strong caffeine kick.', 3.00, 'espresso.png', 2.00),
(2, 'Latte', 'Smooth and creamy, this espresso-based drink is blended with steamed milk and topped with a light layer of foam for a balanced, velvety taste.', 4.50, 'latte.webp', 4.00),
(3, 'Cappuccino', 'A classic favorite with equal parts espresso, steamed milk, and frothy foam, delivering a rich, robust flavor with a light, airy texture.', 4.00, 'cappuccino.png', 6.00),
(4, 'Americano', 'A simple yet satisfying mix of espresso and hot water, creating a smooth, mellow coffee with a slightly lighter body than a traditional espresso.', 5.50, 'americano.png', 1.00);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
