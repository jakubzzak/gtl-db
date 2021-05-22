drop procedure  if exists  find_book;
drop type if exists resource_types;
CREATE TYPE resource_types
AS TABLE
(
    item varchar(30)
);
GO

create or alter procedure find_book @order_by varchar(100), @offset int, @limit int,
    @sought_types as dbo.resource_types readonly, @with_types bit,
    @title varchar(max), @with_title bit,
    @author varchar(max), @with_author bit,
    @area varchar(max), @with_area bit
as
    begin
SELECT * FROM book
WHERE deleted=0
  AND (resource_type IN (select * from @sought_types) or @with_types = 0)
  AND (title like '%' + @title + '%' or @with_title = 0)
  AND (author like '%' + @author + '%' or @with_author = 0)
  AND (subject_area like '%' + @area + '%' or @with_area = 0)
            ORDER BY case @order_by
                when 'title' then book.title
                when 'author' then book.author
                when 'isbn' then book.isbn
            end
            OFFSET @offset ROWS
FETCH NEXT @limit ROW ONLY;
end
go;
