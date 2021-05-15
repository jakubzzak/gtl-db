create procedure insertBook @isbn varchar(30), @title varchar(150), @author varchar(100), @subject_area varchar(100),
                            @description varchar(max), @is_loanable bit, @resource_type varchar(30),
                            @total_copies int as
begin try
    begin transaction insert into book
                      values (@isbn, @title, @author, @subject_area, @description, @is_loanable, @total_copies,
                              @total_copies, @resource_type); commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
