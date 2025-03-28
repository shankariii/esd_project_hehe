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
