create procedure insertLibrarian @ssn varchar(20), @email varchar(100), @password varchar(60), @first_name varchar(100),
                                @last_name varchar(100), @position varchar(30), @campus int as
begin try
begin transaction
    insert into librarian values (@ssn, @email, @password, @first_name, @last_name, @position, @campus);
    commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
