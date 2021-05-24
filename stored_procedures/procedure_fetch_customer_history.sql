create or
alter procedure fetch_customer_history @customer_ssn varchar(30)
as
begin
    SELECT b.title, l.loaned_at, l.returned_at
    FROM loan l
             JOIN customer c ON c.ssn = l.customer_ssn
             JOIN book b ON b.isbn = l.book_isbn
    WHERE l.customer_ssn = @customer_ssn
    ORDER BY loaned_at desc;
end