CREATE TABLE `Aspect` (
	`aspect_id` SMALLINT NOT NULL AUTO_INCREMENT,
	`aspect_name` VARCHAR(30) NOT NULL,
	`description` VARCHAR(100) NOT NULL,
	PRIMARY KEY (`aspect_id`)
);

CREATE TABLE `Campus` (
	`campus_id` TINYINT NOT NULL AUTO_INCREMENT,
	`campus_name` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`campus_id`)
);

CREATE TABLE `Career` (
	`career_id` SMALLINT NOT NULL AUTO_INCREMENT,
	`career_name` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`career_id`)
);

CREATE TABLE `Course` (
	`course_code` CHAR(6) NOT NULL,
	`course_name` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`course_code`)
);

CREATE TABLE `Professor` (
    `professor_id` INT AUTO_INCREMENT NOT NULL,
    `professor_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`professor_id`)
);

CREATE TABLE `Group` (
    `group_id` INT AUTO_INCREMENT NOT NULL,
    `year` SMALLINT NOT NULL,
    `semester` TINYINT NOT NULL,
    `course_code` CHAR(6) NOT NULL,
    `professor_id` INT NOT NULL,
    `group_number` TINYINT NOT NULL,
    `campus_id` TINYINT NOT NULL,
    PRIMARY KEY (`group_id`),
    FOREIGN KEY (`course_code`) REFERENCES `Course`(`course_code`),
    FOREIGN KEY (`professor_id`) REFERENCES `Professor`(`professor_id`),
    FOREIGN KEY (`campus_id`) REFERENCES `Campus`(`campus_id`)
);

CREATE TABLE `Exercise` (
	`exercise_id` INT NOT NULL AUTO_INCREMENT,
	`statement` TEXT NOT NULL, 
	`group_id` INT NOT NULL,
	PRIMARY KEY (`exercise_id`),
    FOREIGN KEY (`group_id`) REFERENCES `Group`(`group_id`)
);

CREATE TABLE `ExerciseAspect` (
    `exercise_id` INT NOT NULL,
    `aspect_id` SMALLINT NOT NULL,
    PRIMARY KEY (`exercise_id`, `aspect_id`),
    FOREIGN KEY (`exercise_id`) REFERENCES `Exercise`(`exercise_id`),
    FOREIGN KEY (`aspect_id`) REFERENCES `Aspect`(`aspect_id`)
);

CREATE TABLE `Metric` (
    `metric_id` TINYINT AUTO_INCREMENT NOT NULL,
    `metric_name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(150) NOT NULL,
    PRIMARY KEY (`metric_id`)
);

CREATE TABLE `SubMetric` (
    `metric_id` TINYINT NOT NULL,
    `name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(100) NOT NULL,
    `submetric_id` INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`submetric_id`),
    FOREIGN KEY (`metric_id`) REFERENCES `Metric`(`metric_id`)
);

CREATE TABLE `ExerciseMetric` (
    `exercise_id` INT NOT NULL,
    `submetric_id` INT NOT NULL,
    PRIMARY KEY (`exercise_id`, `submetric_id`),
    FOREIGN KEY (`exercise_id`) REFERENCES `Exercise`(`exercise_id`),
    FOREIGN KEY (`submetric_id`) REFERENCES `SubMetric`(`submetric_id`)
);

CREATE TABLE `ExerciseSolution` (
    `solution_id` BIGINT AUTO_INCREMENT NOT NULL,
    `exercise_id` INT NOT NULL,
    `solution` BLOB NOT NULL,
    PRIMARY KEY (`solution_id`),
    FOREIGN KEY (`exercise_id`) REFERENCES `Exercise`(`exercise_id`)
);

CREATE TABLE `Student` (
    `anonymous_id` BIGINT AUTO_INCREMENT NOT NULL,
    `student_id` BIGINT NOT NULL,
    `student_name` VARCHAR(50) NOT NULL,
    `career_id` SMALLINT NOT NULL,
    `gender` VARCHAR(6) NOT NULL,
    `ct_score` SMALLINT NOT NULL DEFAULT 0,
    PRIMARY KEY (`anonymous_id`),
    FOREIGN KEY (`career_id`) REFERENCES `Career`(`career_id`)
);

CREATE TABLE `StudentMetric` (
    `anonymous_id` BIGINT NOT NULL,
    `metric_id` TINYINT NOT NULL,
    `grade` SMALLINT NOT NULL,
    PRIMARY KEY (`anonymous_id`, `metric_id`),
    FOREIGN KEY (`anonymous_id`) REFERENCES `Student`(`anonymous_id`),
    FOREIGN KEY (`metric_id`) REFERENCES `Metric`(`metric_id`)
);

CREATE TABLE `StudentSolution` (
    `anonymous_id` BIGINT NOT NULL,
    `exercise_id` INT NOT NULL,
    `solution` BLOB NOT NULL,
    `grade` DECIMAL(3, 0) NOT NULL,
    `student_solution_id` BIGINT NOT NULL,
    `delivered_date` DATE NOT NULL,
    PRIMARY KEY (`student_solution_id`),
    FOREIGN KEY (`anonymous_id`) REFERENCES `Student`(`anonymous_id`),
    FOREIGN KEY (`exercise_id`) REFERENCES `Exercise`(`exercise_id`)
);

CREATE TABLE `StudentMetricSolution` (
    `student_solution_id` BIGINT NOT NULL,
    `submetric_id` INT NOT NULL,
    `grade` INT NOT NULL,
    PRIMARY KEY (`student_solution_id`, `submetric_id`),
    FOREIGN KEY (`submetric_id`) REFERENCES `SubMetric`(`submetric_id`)
);

CREATE TABLE `SubMetricCategory` (
    `submetric_id` INT NOT NULL,
    `min_range` DECIMAL(6, 2) NOT NULL,
    `max_range` DECIMAL(6, 2) NOT NULL,
    `description` VARCHAR(50) NOT NULL,
    FOREIGN KEY (`submetric_id`) REFERENCES `SubMetric`(`submetric_id`)
);