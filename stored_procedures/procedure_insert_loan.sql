create or alter procedure insertLoan @book_isbn varchar(30), @customer_ssn varchar(20), @issued_by varchar(20),
                            @loaned_at datetime, @returned_at datetime as

insert into loan values (newid(), @book_isbn, @customer_ssn, @issued_by, @loaned_at, @returned_at);

go
