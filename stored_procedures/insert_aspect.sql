USE poliglot;
DROP PROCEDURE IF EXISTS SP_Insert_Aspect;
DELIMITER //
CREATE PROCEDURE SP_Insert_Aspect(
    IN a_exercise_id INT,
    IN a_keywords_json JSON
)
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE n INT DEFAULT JSON_LENGTH(a_keywords_json);
    DECLARE v_aspect_id INT DEFAULT NULL;
    DECLARE v_aspect_name VARCHAR(30);
    DECLARE v_error_message TEXT;
    DECLARE v_error BOOLEAN DEFAULT FALSE;
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1
            v_error_message = MESSAGE_TEXT;
        SET v_error = TRUE;
    END;

    START TRANSACTION;

    WHILE i < n DO
        SET v_aspect_name = JSON_UNQUOTE(JSON_EXTRACT(a_keywords_json, CONCAT('$[', i, ']')));
        
        SELECT aspect_id INTO v_aspect_id 
        FROM Aspect 
        WHERE aspect_name = v_aspect_name 
        LIMIT 1;
        IF v_aspect_id IS NULL THEN
            INSERT INTO Aspect (aspect_name) VALUES (v_aspect_name);
            SET v_aspect_id = LAST_INSERT_ID();
        END IF;
        
        INSERT INTO ExerciseAspect (exercise_id, aspect_id) 
        VALUES (a_exercise_id, v_aspect_id);
        
        SET i = i + 1;
		SET v_aspect_id = NULL;
    END WHILE;
    
    IF v_error THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_error_message;
    ELSE
        COMMIT;
    END IF;
END //
DELIMITER ;