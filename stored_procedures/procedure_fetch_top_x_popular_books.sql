create or
alter procedure fetch_top_x_popular_books @limit integer
as
begin
    SELECT TOP (@limit) b.isbn,
                        b.title,
                        b.author,
                        b.resource_type,
                        b.total_copies,
                        b.available_copies,
                        count(*) AS count
    FROM loan l
             JOIN book b ON b.isbn = l.book_isbn
    GROUP BY b.isbn, b.title, b.author, b.resource_type, b.total_copies, b.available_copies
    ORDER BY count DESC, title;
end