create or alter procedure insertLibraryWishlistItem @title varchar(100), @description varchar(max) as
begin try
    begin transaction insert into library_wishlist_item(title, description)
                      values (@title, @description); commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
