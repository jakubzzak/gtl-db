create or
alter procedure find_book @order_by varchar(100) = 'title',
                          @offset int = 0,
                          @limit int = 10,
                          @search_group varchar(30) = 'EVERYTHING',
                          @title varchar(max) = null,
                          @author varchar(max) = null,
                          @area varchar(max) = null
as
begin
    SELECT *
    FROM book
    WHERE deleted = 0
      AND (@search_group = 'EVERYTHING' or resource_type = @search_group)
      AND (
            (@title is not null and title like '%' + @title + '%')
            OR
            (@author is not null and author like '%' + @author + '%')
            OR
            (@area is not null and subject_area like '%' + @area + '%')
        )
    ORDER BY case @order_by
                 when 'title' then book.title
                 when 'author' then book.author
                 else book.isbn
                 end
    OFFSET @offset ROWS FETCH NEXT @limit ROW ONLY;
end
go;
