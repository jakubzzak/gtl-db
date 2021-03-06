create or alter view not_returned_loans as
select ssn,
       first_name + ' ' + last_name as name,
       customer.email,
       customer.type,
       loaned_at,
       case customer.type
           when 'STUDENT' then CONVERT(date, dateadd(week, 3, loaned_at))
           when 'PROFESSOR' then CONVERT(date, dateadd(month, 3, loaned_at))
           else CONVERT(date, dateadd(week, 3, loaned_at))
           end as due_date,
       case customer.type
           when 'STUDENT' then CONVERT(date, dateadd(week, 4, loaned_at))
           when 'PROFESSOR' then CONVERT(date, dateadd(week, 2, dateadd(month, 3, loaned_at)))
           else CONVERT(date, dateadd(week, 4, loaned_at))
           end as grace_period_end,
       book_isbn,
       book.title,
       book.author
from loan
         join customer on loan.customer_ssn = ssn
         join book on book.isbn = loan.book_isbn
where loan.returned_at is null;

go