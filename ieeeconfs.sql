-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 30, 2018 at 09:32 AM
-- Server version: 10.1.30-MariaDB
-- PHP Version: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ieeeconfs`
--

-- --------------------------------------------------------

--
-- Table structure for table `author in paper`
--

CREATE TABLE `author in paper` (
  `PaperNum` int(20) NOT NULL,
  `AuthorNum` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `authors`
--

CREATE TABLE `authors` (
  `AuthorNum` int(20) NOT NULL,
  `FullName` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `keyword in paper`
--

CREATE TABLE `keyword in paper` (
  `PaperNum` int(20) NOT NULL,
  `KeywordNum` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `keywords`
--

CREATE TABLE `keywords` (
  `KeywordNum` int(20) NOT NULL,
  `text` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `papers`
--

CREATE TABLE `papers` (
  `PaperNum` int(20) NOT NULL,
  `title` varchar(20) NOT NULL,
  `PaperCitationCount` int(20) DEFAULT NULL,
  `abstract` varchar(100) NOT NULL,
  `html url` varchar(30) NOT NULL,
  `Publication Title` varchar(20) NOT NULL,
  `Author Affiliations` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `author in paper`
--
ALTER TABLE `author in paper`
  ADD PRIMARY KEY (`PaperNum`,`AuthorNum`),
  ADD KEY `AuthorNum` (`AuthorNum`);

--
-- Indexes for table `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`AuthorNum`);

--
-- Indexes for table `keyword in paper`
--
ALTER TABLE `keyword in paper`
  ADD PRIMARY KEY (`PaperNum`,`KeywordNum`),
  ADD KEY `KeywordNum` (`KeywordNum`);

--
-- Indexes for table `keywords`
--
ALTER TABLE `keywords`
  ADD PRIMARY KEY (`KeywordNum`);

--
-- Indexes for table `papers`
--
ALTER TABLE `papers`
  ADD PRIMARY KEY (`PaperNum`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `authors`
--
ALTER TABLE `authors`
  MODIFY `AuthorNum` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `keywords`
--
ALTER TABLE `keywords`
  MODIFY `KeywordNum` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `papers`
--
ALTER TABLE `papers`
  MODIFY `PaperNum` int(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `author in paper`
--
ALTER TABLE `author in paper`
  ADD CONSTRAINT `author in paper_ibfk_1` FOREIGN KEY (`PaperNum`) REFERENCES `papers` (`PaperNum`),
  ADD CONSTRAINT `author in paper_ibfk_2` FOREIGN KEY (`AuthorNum`) REFERENCES `authors` (`AuthorNum`);

--
-- Constraints for table `keyword in paper`
--
ALTER TABLE `keyword in paper`
  ADD CONSTRAINT `keyword in paper_ibfk_1` FOREIGN KEY (`PaperNum`) REFERENCES `papers` (`PaperNum`),
  ADD CONSTRAINT `keyword in paper_ibfk_2` FOREIGN KEY (`KeywordNum`) REFERENCES `keywords` (`KeywordNum`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
