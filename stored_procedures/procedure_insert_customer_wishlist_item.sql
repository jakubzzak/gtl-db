create or alter procedure insertCustomerWishlistItem @customer_ssn varchar(20), @book_isbn varchar(30), @requested_at datetime,
                                            @picked_up bit as
begin try
    begin transaction insert into customer_wishlist_item(customer_ssn, book_isbn, requested_at, picked_up)
                      values (@customer_ssn, @book_isbn, @requested_at, @picked_up); commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
