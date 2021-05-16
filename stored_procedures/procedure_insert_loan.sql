create or alter procedure insertLoan @book_isbn varchar(30), @customer_ssn varchar(20), @issued_by varchar(20),
                            @loaned_at datetime, @returned_at datetime as
begin try
    begin transaction;
        declare @available_copies int;
        select @available_copies = available_copies from book where book.isbn = @book_isbn;
        if (@available_copies > 0) insert into loan output inserted.id values (newid(), @book_isbn, @customer_ssn, @issued_by, @loaned_at, @returned_at);

        if(@returned_at is null) update book set available_copies = available_copies - 1 where book.isbn = @book_isbn

    commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
