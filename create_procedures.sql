use gtl
go

DROP PROC IF EXISTS dbo.fillCampusTable;

go

CREATE PROCEDURE dbo.fillCampusTable(
    @rowsNumber int
)
AS
BEGIN
    SET NOCOUNT ON

    declare @address_rows_count int = (select count(*) from address)
    declare @current_rows_count int = (select count(*) from campus)

    DECLARE @iteration INT = 0

    WHILE @rowsNumber - @current_rows_count > @iteration
        BEGIN

            INSERT INTO campus VALUES (rand() * @address_rows_count + 1)

            SET @iteration += 1
        END

    SET NOCOUNT OFF
END

go

exec dbo.fillCampusTable @rowsNumber = 7;