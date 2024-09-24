USE poliglot;
DROP PROCEDURE IF EXISTS SP_Insert_Exercise;
DELIMITER //
CREATE PROCEDURE SP_Insert_Exercise(
    IN a_name VARCHAR(50),
    IN a_statement TEXT,
    IN a_year SMALLINT,
    IN a_semester TINYINT,
    IN a_course_code CHAR(6),
    IN a_group_number TINYINT
)
BEGIN
    DECLARE v_group_id INT DEFAULT NULL;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_error = TRUE;
    
    SELECT group_id INTO v_group_id 
    FROM `Group`
    WHERE `year` = a_year AND semester = a_semester AND course_code = a_course_code AND group_number = a_group_number
    LIMIT 1;
    IF v_group_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe el grupo';
    END IF;
    
    START TRANSACTION;

    INSERT INTO Exercise (name, statement, group_id) VALUES (a_name, a_statement, v_group_id);
    
    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error en SP_Insert_Group';
    ELSE
        COMMIT;
        SELECT LAST_INSERT_ID() AS exercise_id;
    END IF;
END //
DELIMITER ;