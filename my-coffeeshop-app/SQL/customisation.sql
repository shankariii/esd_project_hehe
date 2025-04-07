-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 06, 2025 at 03:49 AM
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
-- Database: `customisation`
CREATE DATABASE IF NOT EXISTS customisation DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE customisation;

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
  `CIID` int NOT NULL,
  PRIMARY KEY (`customisation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `customisation`
--

INSERT INTO `customisation` (`customisation_id`, `customisation_type`, `name`, `price_diff`, `CIID`) VALUES
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
