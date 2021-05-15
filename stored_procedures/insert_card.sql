create procedure insertCard @customer_ssn varchar(20), @expiration_date date, @photo_path varchar(150) as
begin try
begin transaction
    insert into card(customer_ssn, expiration_date, photo_path) values(@customer_ssn, @expiration_date, @photo_path);
    commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
