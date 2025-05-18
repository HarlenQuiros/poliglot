USE poliglot;

DROP PROCEDURE IF EXISTS SP_Insert_Solution;

DELIMITER //

CREATE PROCEDURE SP_Insert_Solution(
    IN a_id BIGINT,
    IN a_exercise_id INT,
    IN a_solution BLOB,
    IN a_grade DECIMAL(3, 0)
)
BEGIN
    DECLARE v_error_message TEXT;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE v_student_hash BINARY(32); 
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_error_message = MESSAGE_TEXT;
        SET v_error = TRUE;
    END;

    SET v_student_hash = UNHEX(SHA2(a_id, 256));

    IF NOT EXISTS (SELECT 1 FROM Student WHERE student_id = v_student_hash) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe el estudiante';
    END IF;
    
    START TRANSACTION;
        
    INSERT INTO StudentSolution (student_id, exercise_id, solution, grade) 
    VALUES (v_student_hash, a_exercise_id, a_solution, a_grade);
    
    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    ELSE
        COMMIT;
    END IF;
END //

DELIMITER ;