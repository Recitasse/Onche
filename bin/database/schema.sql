-- MySQL Script généré par OQG BDD GENERATOR
-- Author: raphael
-- 2024-06-01 17:14:52.968461
-- Model: Onche	 Version: 0.8.3
-- Made by Recitasse 31/05/2024

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `Onche` DEFAULT CHARACTER SET utf8mb4;
USE `Onche` ;

-- -----------------------------------------------------
-- Table `Onche`.`stickers`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`stickers` (
  stickers_id INT NOT NULL AUTO_INCREMENT,
  stickers_nom VARCHAR(1000) NOT NULL,
  stickers_collection INT NOT NULL,
  PRIMARY KEY (`stickers_id`),
  UNIQUE INDEX `stickers_nom_UNIQUE` (`stickers_nom` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Tables des stickers au format onche';


-- -----------------------------------------------------
-- Table `Onche`.`badges`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`badges` (
  badges_id INT NOT NULL AUTO_INCREMENT,
  badges_nom VARCHAR(100) NOT NULL,
  PRIMARY KEY (`badges_id`),
  UNIQUE INDEX `badges_nom_UNIQUE` (`badges_nom` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Tables des badges';


-- -----------------------------------------------------
-- Table `Onche`.`topic`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`topic` (
  topic_id INT NOT NULL AUTO_INCREMENT,
  topic_oid INT NOT NULL,
  topic_operateur INT NOT NULL,
  topic_nom VARCHAR(3000) NOT NULL,
  topic_date TIMESTAMP(2) NOT NULL DEFAULT CURRENT_TIMESTAMP(2),
  topic_message INT NOT NULL,
  topic_lien VARCHAR(1000) NOT NULL,
  topic_forum TINYINT(15) NOT NULL,
  PRIMARY KEY (`topic_id`),
  UNIQUE INDEX `topic_oid_UNIQUE` (`topic_oid` ASC) VISIBLE,
  INDEX `createur_idx` (`topic_operateur` ASC) VISIBLE,
  CONSTRAINT `createur`
    FOREIGN KEY (`topic_operateur`)
    REFERENCES `Onche`.`onchois` (`onchois_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Tables des onchois';


-- -----------------------------------------------------
-- Table `Onche`.`pined`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`pined` (
  pined_id INT NOT NULL AUTO_INCREMENT,
  pined_userid INT NOT NULL,
  pined_badgeid INT NOT NULL,
  PRIMARY KEY (`pined_id`),
  INDEX `pins_idx` (`pined_badge` ASC) VISIBLE,
  INDEX `piners_idx` (`pined_onchois` ASC) VISIBLE,
  CONSTRAINT `pins`
    FOREIGN KEY (`pined_badge`)
    REFERENCES `Onche`.`badges` (`badges_badgeid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `piners`
    FOREIGN KEY (`pined_onchois`)
    REFERENCES `Onche`.`onchois` (`onchois_userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Répertorie les onchois badgés';


-- -----------------------------------------------------
-- Table `Onche`.`onchois`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`onchois` (
  onchois_id INT NOT NULL AUTO_INCREMENT,
  onchois_oid INT NOT NULL,
  onchois_niveau INT NOT NULL DEFAULT 1,
  onchois_nom VARCHAR(100) NOT NULL,
  onchois_sexe VARCHAR(30) NOT NULL,
  onchois_age INT NULL,
  onchois_qualite INT NOT NULL DEFAULT 5,
  onchois_message INT NOT NULL DEFAULT 0,
  onchois_date DATETIME(0) NOT NULL,
  PRIMARY KEY (`onchois_id`),
  UNIQUE INDEX `onchois_nom_UNIQUE` (`onchois_nom` ASC) VISIBLE
  UNIQUE INDEX `onchois_oid_UNIQUE` (`onchois_oid` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Tables des onchois';


-- -----------------------------------------------------
-- Table `Onche`.`messages`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Onche`.`messages` (
  messages_id INT NOT NULL AUTO_INCREMENT,
  messages_oid INT NOT NULL,
  messages_user INT NOT NULL,
  messages_topic INT NOT NULL,
  messages_message LONGTEXT NOT NULL,
  messages_touser INT NULL,
  messages_date DATETIME(0) NOT NULL,
  PRIMARY KEY (`messages_id`),
  INDEX `posteur_idx` (`messages_user` ASC) VISIBLE,
  INDEX `sujet_idx` (`messages_topic` ASC) VISIBLE,
  INDEX `reponseur_idx` (`messages_touser` ASC) VISIBLE,
  CONSTRAINT `posteur`
    FOREIGN KEY (`messages_user`)
    REFERENCES `Onche`.`onchois` (`onchois_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `sujet`
    FOREIGN KEY (`messages_topic`)
    REFERENCES `Onche`.`topic` (`topic_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `reponseur`
    FOREIGN KEY (`messages_touser`)
    REFERENCES `Onche`.`onchois` (`onchois_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_general_ci
COMMENT = 'Tous les messages du forum';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;