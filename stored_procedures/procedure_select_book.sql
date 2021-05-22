drop procedure  if exists  find_book;
drop type if exists resource_types;
CREATE TYPE resource_types
AS TABLE
(
    item varchar(30)
);
GO

create or alter procedure find_book @order_by varchar(100), @offset int, @limit int,
    @sought_types as dbo.resource_types readonly,
    @title varchar(max),
    @author varchar(max),
    @area varchar(max)
as
    begin
SELECT * FROM book
WHERE deleted=0
  AND (resource_type IN (select * from @sought_types))
  AND (title like '%' + @title + '%' or @title is null)
  AND (author like '%' + @author + '%' or @author is null)
  AND (subject_area like '%' + @area + '%' or @area is null)
            ORDER BY case @order_by
                when 'title' then book.title
                when 'author' then book.author
                when 'isbn' then book.isbn
            end
            OFFSET @offset ROWS
FETCH NEXT @limit ROW ONLY;
end
go;
