-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 24, 2025 at 05:06 AM
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
  `cic_id` int NOT NULL,
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
