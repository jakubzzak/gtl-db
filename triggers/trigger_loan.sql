create trigger insert_loan_before on loan instead of insert as
begin
    declare @available_copies int, @is_loanable bit, @can_borrow bit, @books_borrowed int, @customer_type varchar(20);
    select @available_copies = available_copies, @is_loanable = is_loanable from book, inserted where isbn = inserted.book_isbn;
    select @can_borrow = can_borrow, @books_borrowed = books_borrowed, @customer_type = type from customer, inserted where inserted.customer_ssn = customer.ssn;
    if (@is_loanable = 0)
        raiserror ('This book is not loanable', 10, 11)
    else if (@available_copies < 1)
        raiserror ('Not enough books on stock', 10, 11)
    else if (@can_borrow = 0)
        raiserror ('This user is not entitled to borrow a book ', 10, 11)
    else if (@books_borrowed > 5)
        raiserror ('User cannot have more than 5 books at a time', 10, 11)
    else
        begin
            if((select returned_at from inserted) is null)
                update book set available_copies -= 1 from inserted where isbn = inserted.book_isbn
                update customer set books_borrowed += 1 from inserted where ssn = inserted.customer_ssn
            insert into loan select * from inserted
        end
end
go
create trigger book_returned_update_count on loan instead of update as
    begin
        if((select returned_at from deleted) is null and (select returned_at from inserted) is not null)
            update book set available_copies += 1 from inserted where isbn = inserted.book_isbn
            update customer set books_borrowed -= 1 from inserted where ssn = inserted.customer_ssn
        insert into loan select * from inserted
    end;
go;
