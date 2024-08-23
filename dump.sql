-- Crea il database se non esiste
CREATE DATABASE IF NOT EXISTS ChatRPS;
USE ChatRPS;

-- Crea la tabella `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL UNIQUE,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crea la tabella `conversations`
DROP TABLE IF EXISTS `conversations`;
CREATE TABLE `conversations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `start_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Crea la tabella `messages`
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `prompt` text NOT NULL,
  `response` text NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserisci record di prova nella tabella `users`
INSERT INTO `users` (`name`, `lastname`, `username`, `email`, `password`) VALUES
('Alfio', 'Spoto', 'nameisalfio', 'alfio.spoto@mail.it', 'hashed_password_1'),
('Gabriele', 'Ruggieri', 'gabryruggieri', 'gabriele.ruggieri@mail.it', 'hashed_password_2');

-- Inserisci record di prova nella tabella `conversations`
INSERT INTO `conversations` (`user_id`, `start_time`) VALUES
(1, '2024-08-23 10:00:00'),
(2, '2024-08-23 11:00:00');

-- Inserisci record di prova nella tabella `messages`
INSERT INTO `messages` (`conversation_id`, `prompt`, `response`, `timestamp`) VALUES
(1, 'Hello', 'Hi there!', '2024-08-23 10:01:00'),
(1, 'How are you?', 'I am fine, thank you!', '2024-08-23 10:02:00'),
(2, 'What’s up?', 'Not much, just working.', '2024-08-23 11:01:00'),
(2, 'Same here, busy with projects.', 'Glad to hear that!', '2024-08-23 11:02:00');
