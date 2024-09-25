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
    DECLARE v_id BIGINT DEFAULT NULL;
    DECLARE v_error_message TEXT;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_error_message = MESSAGE_TEXT;
        SET v_error = TRUE;
    END;

    SELECT anonymous_id INTO v_id 
    FROM Student
    WHERE student_id = a_id
    LIMIT 1;
    IF v_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe el estudiante';
    END IF;
    
    START TRANSACTION;
        
    INSERT INTO StudentSolution (anonymous_id, exercise_id, solution, grade) VALUES (v_id, a_exercise_id, a_solution, a_grade);
    
    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    ELSE
        COMMIT;
    END IF;
END //
DELIMITER ;