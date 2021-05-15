import datetime
import random
import uuid
from datetime import timedelta
from random import randrange
import time
import numpy as np
import pandas as pd


def random_dates(start, end, n):
    start_u = start.value // 10 ** 9
    end_u = end.value // 10 ** 9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def write_to_sql_exec(filename, dataframe, procedure):
    with open('final_output/{filename}'.format(filename=filename), mode='w+') as file:
        print('set nocount on;', file=file)
        for sql_statement in yield_sql_exec(dataframe, procedure):
            print(sql_statement, file=file)
        print('set nocount off;', file=file)


def yield_sql_exec(dataframe, procedure):
    for index, row in dataframe.iterrows():
        args = ','.join([str(i) if type(i) == int else '\'' + str(i) + '\'' for i in list(row.values)])
        yield "exec {procedure} {args}; go;".format(procedure=procedure, args=args)


def generate_users_df():
    # @ssn 0 varchar(20), @email 1 varchar(100), @password 2 varchar(60), @first_name 3 varchar(100),
    # @last_name 4 varchar(100), @campus_id 5 int, @user_type 6 varchar(20),
    # @can_reserve 7 bit, @can_borrow 8 bit, @books_borrowed 9 smallint, @books_reserved 10 smallint,
    # @is_active 11 bit, @street 12 varchar(150), @street_number 13 varchar(50), @city 14 varchar(100),
    # @post_code 15 varchar(20),
    # @country 16 varchar(100), @phone_country_code 17 as varchar(5), @phone_number 18 varchar(15),
    # @phone_type 19 varchar(30)

    users_df = pd.read_csv('online_generator_scripts/users.csv')

    user_rows = len(users_df.index)
    users_df.insert(5, 'campus_id', np.random.randint(1, 8, user_rows))
    users_df.insert(6, 'user_type', random.choices(['STUDENT', 'PROFESSOR'], (user_rows, 150), k=user_rows))
    users_df.insert(7, 'can_reserve', random.choices([0, 1], (20, user_rows), k=user_rows))
    users_df.insert(8, 'can_borrow', random.choices([0, 1], (20, user_rows), k=user_rows))
    users_df.insert(9, 'books_borrowed', 0),
    users_df.insert(10, 'books_reserved', 0),
    users_df.insert(11, 'is_active', random.choices([0, 1], (1000, user_rows), k=user_rows)),
    users_df.insert(13, 'street_number', np.random.randint(1, 200, user_rows)),
    users_df.insert(15, 'post_code', np.random.randint(1, 10000, user_rows)),
    users_df.insert(17, 'phone_country_code', np.random.randint(1, 999, user_rows)),
    users_df.insert(19, 'phone_type', random.choices(['HOME', 'OFFICE', 'MOBILE'], (500, 700, user_rows), k=user_rows))
    users_df.insert(20, 'registered_at', random_dates(pd.to_datetime(start_date), pd.to_datetime("now"), user_rows))

    return users_df


def generate_cards_df(print_tail=False):
    cards = []
    for index, user_row in users_df.iterrows():
        delta = timedelta(365 * 4)
        soonest_expiration = user_row['registered_at'] + delta
        expiration_date = random_date(soonest_expiration, soonest_expiration + timedelta(7))
        cards.append({
            'customer_ssn': user_row['ssn'],
            'expiration_date': expiration_date,
            'photo_path': uuid.uuid4()
        })

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(books_df.tail(10))

    return pd.DataFrame(cards)


def generate_books_df(print_tail=False):
    books_df = pd.read_csv('online_generator_scripts/books.csv')
    book_rows = len(books_df.index)
    books_df['is_loanable'] = random.choices([0, 1], (1000, book_rows), k=book_rows)
    books_df['resource_type'] = random.choices(
        ['BOOK', 'JOURNAL', 'ARTICLE', 'MAP', 'REFERENCE'],
        (1000, 50, 60, 15, 15), k=book_rows)
    books_df['total_copies'] = np.random.randint(0, 100, book_rows)
    books_df['title'] = books_df['title'].str.replace(r"[\"\',]", '')
    books_df['author'] = books_df['title'].str.replace(r"[\"\',]", '')
    books_df['subject_area'] = books_df['title'].str.replace(r"[\"\',]", '')
    books_df['description'] = books_df['title'].str.replace(r"[\"\',]", '')

    # @isbn 1 varchar(30), @title 2 varchar(150), @author 3 varchar(100), @subject_area 4 varchar(100),
    # @description 5 varchar(max), @is_loanable 6 bit, @resource_type 7 varchar(30),
    # @total_copies 8 int

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(books_df.tail(10))

    return books_df


def generate_customer_wishlist_df(print_tail=False):
    wishlist_items = []
    for i in range(1, 10000):
        ssn = users_df.sample()['ssn'].values[0]
        isbn = books_df.sample()['isbn'].values[0]
        requested_at = random_date(
            datetime.datetime.strptime('2011-05-15', '%Y-%m-%d'),
            datetime.datetime.now()
        )
        picked_up = random.choices([0, 1], (1, 15), k=1)[0]
        wishlist_items.append({
            'ssn': ssn,
            'isbn': isbn,
            'requested_at': requested_at,
            'picked_up': picked_up
        })

    customer_wishlist_items_df = pd.DataFrame(wishlist_items)

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(customer_wishlist_items_df.tail(10))

    return customer_wishlist_items_df


def generate_librarian_df(print_tail=False):
    librarians_df = pd.read_csv('online_generator_scripts/librarians.csv')
    librarians_rows = len(librarians_df)
    librarians_df['position'] = random.choices(
        ['LIBRARIAN', 'ASSOCIATE', 'REFERENCE', 'CHECK-OUT', 'ASSISTANT'],
        (5, 2, 1, 3, 2), k=librarians_rows)
    librarians_df['campus'] = np.random.randint(1, 8, librarians_rows)

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(librarians_df.tail(10))

    return librarians_df

def generate_loans_df():
    pass


if __name__ == '__main__':
    start_date = '2011-05-15'

    books_df = generate_books_df()
    write_to_sql_exec('exec_insert_books.sql', books_df, 'insertBook')

    users_df = generate_users_df()
    write_to_sql_exec('exec_insert_users.sql', users_df, 'insertCustomer')

    cards_df = generate_cards_df()
    write_to_sql_exec('exec_insert_cards.sql', cards_df, 'insertCard')

    customer_wishlist_items_df = generate_customer_wishlist_df(True)
    write_to_sql_exec('exec_insert_customer_wishlist_item.sql', customer_wishlist_items_df, 'insertCustomerWishlistItem')

    librarians_df = generate_librarian_df(True)
    write_to_sql_exec('exec_insert_librarians.sql', librarians_df, 'insertLibrarian')
    #
    # loans_df = generate_loans_df()
    # write_to_sql_exec('exec_insert_books.sql', loans_df, 'insertLoan')
    #
