USE poliglot;
DROP PROCEDURE IF EXISTS SP_Insert_Group;
DELIMITER //
CREATE PROCEDURE SP_Insert_Group(
    IN year SMALLINT,
    IN semester TINYINT,
    IN code CHAR(6),
    IN course VARCHAR(50),
    IN group_number TINYINT,
    IN professor VARCHAR(50),
    IN campus VARCHAR(50)
)
BEGIN
    DECLARE v_professor_id INT DEFAULT NULL;
    DECLARE v_campus_id TINYINT DEFAULT NULL;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_error = TRUE;
    
    START TRANSACTION;
    
    SELECT professor_id INTO v_professor_id 
    FROM Professor 
    WHERE professor_name = professor 
    LIMIT 1;
    IF v_professor_id IS NULL THEN
        INSERT INTO Professor (professor_name) VALUES (professor);
        SET v_professor_id = LAST_INSERT_ID(); 
    END IF;
    
    SELECT campus_id INTO v_campus_id 
    FROM Campus 
    WHERE campus_name = campus 
    LIMIT 1;
    IF v_campus_id IS NULL THEN
        INSERT INTO Campus (campus_name) VALUES (campus);
        SET v_campus_id = LAST_INSERT_ID(); 
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM Course WHERE course_code = code) THEN
        INSERT INTO Course (course_code, course_name) VALUES (code, course);
    END IF;
    
    INSERT INTO `Group` (year, semester, course_code, professor_id, group_number, campus_id)
    VALUES (year, semester, code, v_professor_id, group_number, v_campus_id);
    
    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error en SP_Insert_Group';
    ELSE
        COMMIT;
    END IF;
END //
DELIMITER ;