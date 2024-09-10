USE [Poliglot]
GO
DROP PROCEDURE IF EXISTS SP_Insert_Group
GO
CREATE PROCEDURE SP_Insert_Group
    @year SMALLINT,
    @semester TINYINT,
    @code CHAR(6),
    @course VARCHAR(50),
    @group TINYINT,
    @professor VARCHAR(50),
    @campus VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @professor_id INT;
    DECLARE @campus_id TINYINT;
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;

    BEGIN TRY
        BEGIN TRANSACTION;

        -- profesor exist?
        SELECT @professor_id = professor_id FROM Professor WHERE professor_name = @professor;
        IF @professor_id IS NULL
        BEGIN
            INSERT INTO Professor (professor_name) VALUES (@professor);
            SET @professor_id = SCOPE_IDENTITY(); 
        END

        -- campus exist?
        SELECT @campus_id = campus_id FROM Campus WHERE campus_name = @campus;
        IF @campus_id IS NULL
        BEGIN
            INSERT INTO Campus (campus_name) VALUES (@campus);
            SET @campus_id = SCOPE_IDENTITY(); 
        END

        -- course exist?
        IF NOT EXISTS (SELECT 1 FROM Course WHERE course_code = @code)
        BEGIN
            INSERT INTO Course (course_code, course_name) VALUES (@code, @course);
        END

        INSERT INTO [Group] ([year], semester, course_code, professor_id, group_number, campus_id)
        VALUES (@year, @semester, @code, @professor_id, @group, @campus_id);

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