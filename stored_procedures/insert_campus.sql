create procedure insertCampus @street varchar(150), @number varchar(50), @city varchar(100), @post_code varchar(20), @country varchar(100) as
begin try
    begin transaction declare @id varchar(30)
    declare @table table
                   (
                       id varchar(100)
                   )
    insert into address(street, number, city, post_code, country)
    output Inserted.id into @table
    values (@street, @number, @city, @post_code, @country)
    select @id = id from @table
    insert into campus values (@id); commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
