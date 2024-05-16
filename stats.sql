CREATE TABLE IF NOT EXISTS `Team` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `Player` (
	`id` integer primary key NOT NULL UNIQUE,
	`name` TEXT NOT NULL,
	`team_id` INTEGER NOT NULL,
FOREIGN KEY(`team_id`) REFERENCES `Team`(`id`)
);
CREATE TABLE IF NOT EXISTS `PlayerStats` (
	`id` integer primary key NOT NULL UNIQUE,
	`at_bats` INTEGER NOT NULL,
	`game_date` REAL NOT NULL,
	`hits` INTEGER NOT NULL,
	`home_runs` INTEGER NOT NULL,
	`walks` INTEGER NOT NULL,
	`player_id` INTEGER NOT NULL,
FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`)
);

FOREIGN KEY(`team_id`) REFERENCES `Team`(`id`)
FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`)