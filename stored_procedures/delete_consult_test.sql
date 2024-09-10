-- Eliminar datos de una tabla
DELETE FROM [Group];
GO
DELETE FROM Course;
GO
DELETE FROM Professor;
GO
DELETE FROM Campus;
GO
-- Resetear el valor de IDENTITY manualmente
DBCC CHECKIDENT ('Group', RESEED, 0);
GO
DBCC CHECKIDENT ('Course', RESEED, 0);
GO
DBCC CHECKIDENT ('Professor', RESEED, 0);
GO
DBCC CHECKIDENT ('Campus', RESEED, 0);

SELECT g.year, g.semester, g.course_code, co.course_name, p.professor_name, g.group_number, ca.campus_name  FROM [Group] g
JOIN Course co ON g.course_code = co.course_code
JOIN Professor p ON g.professor_id = p.professor_id
JOIN Campus ca ON g.campus_id = ca.campus_id;

SELECT * FROM Professor;

INSERT INTO Career (career_name) VALUES ('Ingeniería en computación');

DELETE FROM Student
GO
DBCC CHECKIDENT ('Student', RESEED, 0);

SELECT * FROM Student;