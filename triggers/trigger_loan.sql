create trigger insert_loan_before on loan instead of insert as
begin
    declare @available_copies int
    select @available_copies = available_copies from book, inserted where isbn = inserted.book_isbn
    if (@available_copies < 1)
        raiserror ('Not enough books on stock', 10, 11)
    else
        begin
            if((select returned_at from inserted) is null)
                update book set available_copies -= 1 from inserted where isbn = inserted.book_isbn
            insert into loan select * from inserted
        end
end

create trigger book_returned_update_count on loan instead of update as
    begin
        if((select returned_at from deleted) is null and (select returned_at from inserted) is not null)
            update book set available_copies += 1 from inserted where isbn = inserted.book_isbn
        insert into loan select * from inserted
    end
