SET SQL_SAFE_UPDATES = 0;
-- Eliminar datos de una tabla
DELETE FROM `Group`;
DELETE FROM Course;
DELETE FROM Professor;
DELETE FROM Campus;

-- Resetear el valor de AUTO_INCREMENT manualmente
ALTER TABLE `Group` AUTO_INCREMENT = 1;
ALTER TABLE Course AUTO_INCREMENT = 1;
ALTER TABLE Professor AUTO_INCREMENT = 1;
ALTER TABLE Campus AUTO_INCREMENT = 1;

-- Consultar los datos
SELECT g.year, g.semester, g.course_code, co.course_name, p.professor_name, g.group_number, ca.campus_name  
FROM `Group` g
JOIN Course co ON g.course_code = co.course_code
JOIN Professor p ON g.professor_id = p.professor_id
JOIN Campus ca ON g.campus_id = ca.campus_id;

-- Consultar todos los datos de Professor
SELECT * FROM Career;

-- Insertar un nuevo registro en Career
INSERT INTO Career (career_name) VALUES ('Ingeniería en computación');

-- Eliminar datos de Student
DELETE FROM Student;
ALTER TABLE Student AUTO_INCREMENT = 1;

-- Consultar todos los datos de Student
SELECT * FROM Student;

-- Eliminar datos de ExerciseAspect
DELETE FROM ExerciseAspect;

-- Eliminar datos de StudentSolution
DELETE FROM StudentSolution;
ALTER TABLE StudentSolution AUTO_INCREMENT = 1;

-- Eliminar datos de Exercise
DELETE FROM Exercise;
ALTER TABLE Exercise AUTO_INCREMENT = 1;

-- Eliminar datos de Aspect
DELETE FROM Aspect;
ALTER TABLE Aspect AUTO_INCREMENT = 1;

SELECT * FROM Exercise;
SELECT * FROM Aspect;
SELECT * FROM ExerciseAspect;

SELECT e.name as ejercicio, a.aspect_name as aspecto
FROM ExerciseAspect ea
JOIN Exercise e ON e.exercise_id = ea.exercise_id
JOIN Aspect a ON a.aspect_id = ea.aspect_id;

SELECT * FROM StudentSolution;