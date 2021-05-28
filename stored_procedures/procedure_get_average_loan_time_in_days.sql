create or
alter procedure get_average_loan_time_in_days
as
begin
    SELECT AVG(DATEDIFF(DAY, loaned_at, returned_at)) AS average_loan_length_in_days
    FROM loan l
    WHERE l.returned_at IS NOT NULL;
end
go