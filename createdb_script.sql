-- drop database if exists gtl
-- go
-- create database gtl
-- go
use gtl
go

drop table if exists stats;
drop table if exists loan;
drop table if exists librarian_wishlist_item;
drop table if exists librarian;
drop table if exists card;
drop table if exists phone_number;
drop table if exists customer_wishlist_item;
drop table if exists customer;
drop table if exists campus;
drop table if exists address;
drop table if exists book;

create table book
(
    isbn             varchar(30) primary key,
    title            varchar(150)                      not null,
    author           varchar(100)                      not null, -- ?
    subject_area     varchar(100)                      not null, -- ?
    description      varchar(max),
    is_loanable      bit default 1                     not null,
    total_copies     int check (total_copies >= 0)     not null,
    available_copies int check (available_copies >= 0) not null,
    resource_type    varchar(30)                       not null,
    check (available_copies <= book.total_copies),
);

create table address
(
    id        integer identity (1,1) primary key,
    street    varchar(150),
    number    varchar(50),
    city      varchar(100) not null,
    post_code varchar(20)  not null,
    country   varchar(100) not null,
)

-- 7 campuses in total
create table campus
(
    address_id integer references address primary key,
)

create table customer
(
    id              uniqueidentifier   not null primary key,
    ssn             varchar(20)        not null unique,
    email           varchar(100)       not null unique,
    password        varchar(60)        not null,
    first_name      varchar(100)       not null,
    last_name       varchar(100)       not null,
    campus_id       integer            not null references campus,
    type            varchar(20)        not null,
    home_address_id integer            not null references address,
    can_reserve     bit      default 1 not null,
    can_borrow      bit      default 1 not null,
    books_borrowed  smallint default 0 not null,
    books_reserved  smallint default 0 not null,
    is_active       bit      default 1 not null,
)

create table customer_wishlist_item
(
    id           uniqueidentifier primary key,
    customer_ssn varchar(20)   not null references customer,
    book_isbn    varchar(30)   not null references book,
    requested_at datetime,
    picked_up    bit default 0 not null,
)
create table phone_number
(
    customer_ssn varchar     not null,
    country_code varchar(5)  not null,
    number       varchar(15) not null,
    type         varchar(30) not null,
    primary key (country_code, number, customer_ssn)
)

create table card
(
    id              uniqueidentifier primary key,
    customer_ssn    varchar       not null,
    expiration_date date          not null,
    photo_path      varchar(150)  not null,
    is_active       bit default 1 not null,
)

create table librarian
(
    id         uniqueidentifier primary key,
    ssn        varchar(20)  not null unique,
    email      varchar(100) not null unique,
    password   varchar(60)  not null,
    first_name varchar(100) not null,
    last_name  varchar(100) not null,
    position   varchar(30)  not null,
)

create table librarian_wishlist_item
(
    id          uniqueidentifier primary key,
    title       varchar(100) not null,
    description varchar(max),
)

create table loan
(
    id           uniqueidentifier primary key,
    book_isbn    varchar(30)                        not null references book,
    customer_ssn varchar(20)                        not null references customer index ix_non_customer nonclustered,
    issued_by    uniqueidentifier                   not null references librarian,
    loaned_at    datetime default current_timestamp not null index ix_loaned_at clustered,
    returned_at  datetime, -- not creating non-clustured index here, coz it would take up on space and wouldnt make any difference
)

create table stats
(
    start_date  datetime,
    end_date    datetime,
    description varchar(max),
    value       varchar(150),
)