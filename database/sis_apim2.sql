-- phpMyAdmin SQL Dump
-- version 5.1.4
-- https://www.phpmyadmin.net/
--
-- Host: mysql-sis.alwaysdata.net
-- Generation Time: Dec 07, 2022 at 06:03 PM
-- Server version: 10.6.8-MariaDB
-- PHP Version: 7.4.19
-- Avant modification
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sis_apim2` :( ???
--

-- --------------------------------------------------------

--
-- Table structure for table `departements`
--

CREATE TABLE `departements` (
  `id` int(11) NOT NULL,
  `code` varchar(3) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `region_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `departements`
--

INSERT INTO `departements` (`id`, `code`, `nom`, `region_id`) VALUES
(5, '30', 'gard', 1),
(7, '32', 'gers', 1),
(8, '34', 'herault', 1),
(9, '46', 'lot', 1),
(10, '48', 'lozère', 1),
(11, '65', 'hautes-pyrénées', 1),
(12, '66', 'pyrénées-orientales', 1),
(14, '82', 'tarn-et-garonne', 1),
(16, '17', 'charente-maritime', 2),
(17, '19', 'corrèze', 2),
(18, '23', 'creuse', 2),
(19, '24', 'dordogne', 2),
(20, '33', 'gironde', 2),
(21, '40', 'landes', 2),
(22, '47', 'lot-et-garonne', 2),
(23, '64', 'pyrénées-atlantiques', 2),
(24, '79', 'deux-sèvres', 2),
(25, '86', 'vienne', 2),
(26, '87', 'haute-vienne', 2),
(30, '585', 'bananiumFirstDistrict', 1),
(33, '455', 'efgh', 28),
(36, '855', 'Rwanda', 44),
(37, '123', 'krote', 47),
(38, '420', 'montcuq', 60),
(39, '798', 'BoussatVille', 52);

-- --------------------------------------------------------

--
-- Table structure for table `regions`
--

CREATE TABLE `regions` (
  `id` int(11) NOT NULL,
  `code` int(11) NOT NULL,
  `nom` varchar(255) CHARACTER SET utf8mb3 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `regions`
--

INSERT INTO `regions` (`id`, `code`, `nom`) VALUES
(1, 76, 'occitanie'),
(2, 75, 'nouvelle-aquitaine'),
(22, 93, 'Provence-Alpes-Côte d\'Azur'),
(28, 0, 'abcd'),
(30, 666, 'mordor'),
(35, 23, 'region23'),
(44, 830, 'Kigali'),
(45, 9999, 'TestRegions'),
(47, 999, 'krotereg'),
(51, 800, 'Rwanda'),
(52, 2556, 'DeleteVille'),
(60, 667, 'ekip'),
(66, 455854, 'moi');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `departements`
--
ALTER TABLE `departements`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD UNIQUE KEY `nom` (`nom`),
  ADD KEY `region_id` (`region_id`);

--
-- Indexes for table `regions`
--
ALTER TABLE `regions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD UNIQUE KEY `nom` (`nom`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `departements`
--
ALTER TABLE `departements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `regions`
--
ALTER TABLE `regions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `departements`
--
ALTER TABLE `departements`
  ADD CONSTRAINT `departements_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `regions` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
