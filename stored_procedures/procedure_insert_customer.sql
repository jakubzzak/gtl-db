create or alter procedure insertCustomer @ssn varchar(20), @email varchar(100), @password varchar(60), @first_name varchar(100),
                                @last_name varchar(100), @campus_id int, @user_type varchar(20),
                                @can_reserve bit, @can_borrow bit, @books_borrowed smallint, @books_reserved smallint,
                                @is_active bit, @street varchar(150), @street_number varchar(50), @city varchar(100), @post_code varchar(20),
                                @country varchar(100), @phone_country_code as varchar(5), @phone_number varchar(15), @phone_type varchar(30),
                                @registered_at datetime as
begin try
    begin transaction declare @address_id varchar(30)
    declare @address_output table (id varchar(100))
    insert into address(street, number, city, post_code, country) output Inserted.id into @address_output values (@street, @street_number, @city, @post_code, @country)
    select @address_id = id from @address_output
    insert into customer values (@ssn, @email, @password, @first_name, @last_name, @campus_id, @user_type, @address_id, @can_reserve,
            @can_borrow, @books_borrowed, @books_reserved, @is_active, @registered_at);
    insert into phone_number values(@ssn, @phone_country_code, @phone_number, @phone_type)
    commit transaction;
end try begin catch
    rollback transaction;
end catch;
go
