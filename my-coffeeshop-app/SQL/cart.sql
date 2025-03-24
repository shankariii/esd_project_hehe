-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 24, 2025 at 05:05 AM
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
<<<<<<< Updated upstream
CREATE DATABASE IF NOT EXISTS `cart` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
=======
--
CREATE DATABASE IF NOT EXISTS `cart` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
>>>>>>> Stashed changes
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
) ENGINE=InnoDB AUTO_INCREMENT=10016 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `user_id`, `outlet_id`, `totalPrice`) VALUES
(10000, 'vPWKyHuXm9N', 1, 11.3),
(10001, 'vPWKyHuXm9N', 2, 12.9),
(10003, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 4.6),
(10004, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 7.6),
(10005, 'vPWKyHuXm9N', 1, 10.3),
(10006, 'vPWKyHuXm9N', 2, 5.9),
(10008, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 7.6),
(10009, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 4.5),
(10010, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 10.6),
(10011, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 4.5),
(10012, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 6.05),
(10013, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 5),
(10014, 'PyfmvD0fIdYaEtMXkiBIZJO0GAG3', 2, 5.25),
(10015, 'iTeYSJ3xoBQuDdI0uXravnQgbqo2', 2, 10);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
