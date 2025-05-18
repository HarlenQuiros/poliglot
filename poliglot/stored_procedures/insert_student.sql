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
    DECLARE v_student_hash BINARY(32);  
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET v_error = TRUE;

    SET v_student_hash = UNHEX(SHA2(p_student_id, 256));

    START TRANSACTION;

    IF NOT EXISTS (SELECT 1 FROM Student WHERE student_id = v_student_hash) THEN
        INSERT INTO Student (student_id, student_name, career_id, gender, email) 
        VALUES (v_student_hash, p_student_name, p_career_id, p_gender, p_email);
    END IF;

    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error en SP_Insert_Student';
    ELSE
        COMMIT;
    END IF;
END //

DELIMITER ;