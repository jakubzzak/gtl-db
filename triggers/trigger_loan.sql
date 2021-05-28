create trigger insert_loan_instead
    on loan
    instead of insert as
begin
    declare @available_copies int, @is_loanable bit, @can_borrow bit, @books_borrowed int, @customer_type varchar(20);
    select @available_copies = available_copies, @is_loanable = is_loanable
    from book
             join inserted on isbn = inserted.book_isbn;
    select @can_borrow = can_borrow, @books_borrowed = books_borrowed, @customer_type = type
    from customer
             join inserted on inserted.customer_ssn = customer.ssn;
    if (@is_loanable = 0)
        raiserror ('This book is not loanable', 10, 11)
    else
        if (@available_copies < 1)
            raiserror ('Not enough books on stock', 10, 11)
        else
            if (@can_borrow = 0)
                raiserror ('This user is not entitled to borrow a book ', 10, 11)
            else
                if (@books_borrowed >= 5)
                    raiserror ('User cannot have more than 5 books at a time', 10, 11)
                else
                    begin
                        if ((select returned_at from inserted) is null)
                            begin
                                update book set available_copies -= 1 from inserted where isbn = inserted.book_isbn
                                update customer set books_borrowed += 1 from inserted where ssn = inserted.customer_ssn
                            end
                        insert into loan select * from inserted
                    end
end
    create trigger update_loan_instead
        on loan
        instead of update as
    begin
        if ((select returned_at from deleted) is null and (select returned_at from inserted) is not null)
            begin
                update book set available_copies += 1 from inserted where isbn = inserted.book_isbn
                update customer set books_borrowed -= 1 from inserted where ssn = inserted.customer_ssn
            end
        if ((select returned_at from deleted) is not null and (select returned_at from inserted) is null)
            begin
                update book set available_copies -= 1 from inserted where isbn = inserted.book_isbn
                update customer set books_borrowed += 1 from inserted where ssn = inserted.customer_ssn
            end
        update loan
        set loaned_at    = inserted.loaned_at,
            issued_by    = inserted.issued_by,
            book_isbn    = inserted.book_isbn,
            returned_at  = inserted.returned_at,
            customer_ssn = inserted.customer_ssn
        from inserted,
             deleted
        where loan.id = deleted.id
    end;
go
