USE poliglot;

DROP PROCEDURE IF EXISTS SP_Insert_Student;

DELIMITER //

CREATE PROCEDURE SP_Insert_Student(
    IN p_student_id BIGINT,
    IN p_student_name VARCHAR(50),
    IN p_career_id SMALLINT,
    IN p_gender VARCHAR(6),
    IN p_email VARCHAR(100)
)
BEGIN
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_error = TRUE;

    START TRANSACTION;

    IF NOT EXISTS (SELECT 1 FROM Student WHERE student_id = p_student_id) THEN
        INSERT INTO Student (student_id, student_name, career_id, gender, email) 
        VALUES (p_student_id, p_student_name, p_career_id, p_gender, p_email);
    END IF;

    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error en SP_Insert_Group';
    ELSE
        COMMIT;
    END IF;
END //

DELIMITER ;