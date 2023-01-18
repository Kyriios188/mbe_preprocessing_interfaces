-- --------------------------------------------------------
-- Hôte:                         localhost
-- Version du serveur:           10.6.10-MariaDB - mariadb.org binary distribution
-- SE du serveur:                Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour epitaxy_db
CREATE DATABASE IF NOT EXISTS `epitaxy_db` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `epitaxy_db`;

-- Listage de la structure de la table epitaxy_db. curvature
CREATE TABLE IF NOT EXISTS `curvature` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `step_fk` bigint(20) unsigned DEFAULT NULL,
  `rel_time` double unsigned DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `step_fk` (`step_fk`),
  CONSTRAINT `step_fk` FOREIGN KEY (`step_fk`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11902 DEFAULT CHARSET=utf8mb3;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. experiment
CREATE TABLE IF NOT EXISTS `experiment` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(10) NOT NULL DEFAULT '0' COMMENT 'Ex: ''A1417''',
  `experiment_group` varchar(50) DEFAULT '0' COMMENT 'Ex: ''Bragg''',
  `start_time` datetime DEFAULT NULL COMMENT 'Datetime début expérience',
  `end_time` datetime DEFAULT NULL COMMENT 'Datetime fin expérience',
  `n_layers` smallint(5) unsigned DEFAULT 0 COMMENT 'Nombre de ''vrais'' couches',
  `label` float unsigned DEFAULT 0 COMMENT 'Pourcentage d''écart à l''objectif',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. layer
CREATE TABLE IF NOT EXISTS `layer` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `element` varchar(20) DEFAULT NULL COMMENT 'The element of the layer (ex: AlGaAs)',
  `percentage` float unsigned DEFAULT NULL COMMENT 'The percentage of the element of the layer',
  `nm_size` float unsigned DEFAULT NULL COMMENT 'The size of the layer in nanometers',
  PRIMARY KEY (`id`),
  CONSTRAINT `FK_layer_step` FOREIGN KEY (`id`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb3;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. other_step
CREATE TABLE IF NOT EXISTS `other_step` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL COMMENT 'init, end, degaz, etc.',
  PRIMARY KEY (`id`) USING BTREE,
  CONSTRAINT `other_step_ibfk_1` FOREIGN KEY (`id`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. reflectivity
CREATE TABLE IF NOT EXISTS `reflectivity` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `step_fk` bigint(20) unsigned DEFAULT NULL,
  `rel_time` double unsigned DEFAULT NULL,
  `nm_value` double DEFAULT NULL,
  `reflectivity_value` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `step_fk` (`step_fk`) USING BTREE,
  CONSTRAINT `reflectivity_ibfk_1` FOREIGN KEY (`step_fk`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1561908 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. roughness
CREATE TABLE IF NOT EXISTS `roughness` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `step_fk` bigint(20) unsigned DEFAULT NULL,
  `rel_time` double unsigned DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `step_fk` (`step_fk`) USING BTREE,
  CONSTRAINT `roughness_ibfk_1` FOREIGN KEY (`step_fk`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11884 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. step
CREATE TABLE IF NOT EXISTS `step` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `experiment_fk` bigint(20) unsigned DEFAULT NULL,
  `line` tinytext DEFAULT NULL COMMENT 'The raw string corresponding to the step',
  `line_index` smallint(5) unsigned DEFAULT NULL COMMENT 'The index of the string in the log file',
  `step_number` smallint(5) unsigned DEFAULT NULL COMMENT 'The number in the beginning of the line for every step (ex: 0001 for init)',
  `abs_start` datetime DEFAULT NULL,
  `abs_end` datetime DEFAULT NULL,
  `rel_start` double unsigned DEFAULT NULL,
  `rel_end` double unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `experiment_fk` (`experiment_fk`),
  CONSTRAINT `FK__experiment` FOREIGN KEY (`experiment_fk`) REFERENCES `experiment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb3;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table epitaxy_db. wafer_temperature
CREATE TABLE IF NOT EXISTS `wafer_temperature` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `step_fk` bigint(20) unsigned DEFAULT NULL,
  `rel_time` double unsigned DEFAULT NULL,
  `value` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `step_fk` (`step_fk`) USING BTREE,
  CONSTRAINT `wafer_temperature_ibfk_1` FOREIGN KEY (`step_fk`) REFERENCES `step` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=337975 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;

-- Les données exportées n'étaient pas sélectionnées.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
