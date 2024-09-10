USE [Poliglot]
GO
DROP PROCEDURE IF EXISTS SP_Insert_Student
GO
CREATE PROCEDURE SP_Insert_Student
    @student_id BIGINT,
    @student_name VARCHAR(50),
    @career_id SMALLINT,
    @gender VARCHAR(6)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- already exist?
        IF NOT EXISTS (SELECT 1 FROM Student WHERE student_id = @student_id)
        BEGIN
            INSERT INTO Student (student_id, student_name, career_id, gender) VALUES (@student_id, @student_name, @career_id, @gender);
        END

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        SELECT 
            @ErrorMessage = ERROR_MESSAGE(),
            @ErrorSeverity = ERROR_SEVERITY(),
            @ErrorState = ERROR_STATE();

        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH;
END