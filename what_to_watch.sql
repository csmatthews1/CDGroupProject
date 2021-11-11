-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema what_to_watch
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `what_to_watch` ;

-- -----------------------------------------------------
-- Schema what_to_watch
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `what_to_watch` DEFAULT CHARACTER SET utf8 ;
USE `what_to_watch` ;

-- -----------------------------------------------------
-- Table `what_to_watch`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `what_to_watch`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `what_to_watch`.`services`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `what_to_watch`.`services` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `logo_url` VARCHAR(255) NULL,
  `website` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `what_to_watch`.`videos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `what_to_watch`.`videos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(255) NULL,
  `title` VARCHAR(255) NULL,
  `img_url` VARCHAR(255) NULL,
  `info_url` VARCHAR(255) NULL,
  `type` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `user_id` INT NOT NULL,
  `service_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recommendations_users_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_recommendations_streaming service1_idx` (`service_id` ASC) VISIBLE,
  CONSTRAINT `fk_recommendations_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `what_to_watch`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recommendations_streaming service1`
    FOREIGN KEY (`service_id`)
    REFERENCES `what_to_watch`.`services` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `what_to_watch`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `what_to_watch`.`reviews` (
  `user_id` INT NOT NULL,
  `video_id` INT NOT NULL,
  `comments` TEXT NULL,
  `rating` INT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`user_id`, `video_id`),
  INDEX `fk_users_has_recommendations_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_users_has_recommendations_recommendations1_idx` (`video_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_recommendations_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `what_to_watch`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_recommendations_recommendations1`
    FOREIGN KEY (`video_id`)
    REFERENCES `what_to_watch`.`videos` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
