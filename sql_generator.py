import datetime
import gc
import random
import uuid
from datetime import timedelta
from random import randrange

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
        args_list = []
        for i in list(row.values):
            if type(i) == int:
                args_list.append(str(i))
            elif str(i) == 'NaT' or str(i) == 'nan':
                args_list.append('null')
            else:
                args_list.append('\'' + str(i) + '\'')

        args = ','.join(args_list)
        if index % 1000 == 0:
            print('Yielded {i} rows'.format(i=index))
            yield "go;"
        yield "exec {procedure} {args};".format(procedure=procedure, args=args)
    yield "go;"


def generate_users_df(print_tail=False):
    # @ssn 0 varchar(20), @email 1 varchar(100), @password 2 varchar(60), @first_name 3 varchar(100),
    # @last_name 4 varchar(100), @campus_id 5 int, @user_type 6 varchar(20),
    # @can_reserve 7 bit, @can_borrow 8 bit, @books_borrowed 9 smallint, @books_reserved 10 smallint,
    # @is_active 11 bit, @street 12 varchar(150), @street_number 13 varchar(50), @city 14 varchar(100),
    # @post_code 15 varchar(20),
    # @country 16 varchar(100), @phone_country_code 17 as varchar(5), @phone_number 18 varchar(15),
    # @phone_type 19 varchar(30)

    users_df = pd.read_csv('online_generator_seeds/users.csv')

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

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(users_df.tail(10))

    return users_df


def generate_cards_df(print_tail=False):
    cards = []
    for index, user_row in users_df.iterrows():
        four_years_to_expire = timedelta(365 * 4)
        soonest_expiration = user_row['registered_at'] + four_years_to_expire
        expiration_date = random_date(soonest_expiration, soonest_expiration + timedelta(7))
        cards.append({
            'customer_ssn': user_row['ssn'],
            'expiration_date': expiration_date,
            'photo_path': uuid.uuid4()
        })

        if expiration_date < datetime.datetime.now() - timedelta(365 * 4) and random.randint(1, 100) < 25:
            four_years_to_expire = timedelta(365 * 4)
            soonest_expiration = expiration_date + four_years_to_expire
            expiration_date = random_date(soonest_expiration, soonest_expiration + timedelta(7))
            cards.append({
                'customer_ssn': user_row['ssn'],
                'expiration_date': expiration_date,
                'photo_path': uuid.uuid4()
            })

    cards_df = pd.DataFrame(cards)

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(cards_df.tail(10))

    return cards_df


def generate_books_df(max_copies, print_tail=False):
    books_df = pd.read_csv('online_generator_seeds/books.csv')
    book_rows = len(books_df.index)
    books_df['is_loanable'] = random.choices([0, 1], (1000, book_rows), k=book_rows)
    books_df['resource_type'] = random.choices(
        ['BOOK', 'JOURNAL', 'ARTICLE', 'MAP', 'REFERENCE'],
        (1000, 50, 60, 15, 15), k=book_rows)
    books_df['total_copies'] = np.random.randint(0, max_copies, book_rows)
    books_df['title'] = books_df['title'].str.replace(r"[\"\',]", '')
    books_df['author'] = books_df['author'].str.replace(r"[\"\',]", '')
    books_df['subject_area'] = books_df['subject_area'].str.replace(r"[\"\',]", '')
    books_df['description'] = books_df['description'].str.replace(r"[\"\',]", '')

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
            datetime.datetime.strptime(start_date, '%Y-%m-%d'),
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
    librarians_df = pd.read_csv('online_generator_seeds/librarians.csv')
    librarians_rows = len(librarians_df)
    librarians_df['position'] = random.choices(
        ['LIBRARIAN', 'ASSOCIATE', 'REFERENCE', 'CHECK-OUT', 'ASSISTANT'],
        (5, 2, 1, 3, 2), k=librarians_rows)
    librarians_df['campus'] = np.random.randint(1, 8, librarians_rows)

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(librarians_df.tail(10))

    return librarians_df


def generate_loans_df(loans_count, print_tail=False):
    def get_returned_date(loaned_at):
        if loaned_at > datetime.datetime.now() - timedelta(random.randint(14, 28)):
            if random.randint(0, 100) < 5:
                returned_at = loaned_at + timedelta(random.randint(14, 60))
                if returned_at > datetime.datetime.now():
                    returned_at = None
            else:
                returned_at = None
        else:
            if random.randint(0, 100) > 5:
                returned_at = loaned_at + timedelta(random.randint(14, 60))
            else:
                returned_at = None
        return returned_at

    book_isbn = books_df.sample(loans_count, replace=True).reset_index()['isbn']
    customer_ssn = users_df.sample(loans_count, replace=True).reset_index()['ssn']
    issued_by = librarians_df.sample(loans_count, replace=True).reset_index()['ssn']
    loaned_at = random_dates(pd.to_datetime(start_date), pd.to_datetime("now"), loans_count).to_series()
    returned_at = loaned_at.apply(get_returned_date).reset_index(name='returned_at', drop=True)
    loaned_at = loaned_at.reset_index(name='loaned_at', drop=True)

    loans_df = pd.concat([book_isbn, customer_ssn, issued_by, loaned_at, returned_at], axis=1)
    loans_df = loans_df.sort_values(0).reset_index(drop=True)

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(loans_df.tail(10))
    return loans_df


def generate_library_wishlist_items(print_tail=True):
    library_wishlist_items_df = pd.read_csv('online_generator_seeds/library_wishlist_items.csv')
    library_wishlist_items_df['description'] = library_wishlist_items_df[library_wishlist_items_df.columns[1:]].apply(
        lambda x: ', '.join(x.dropna().astype(str)) if random.randint(1, 100) < 90 else None,
        axis=1
    )
    del library_wishlist_items_df['desc1']
    del library_wishlist_items_df['desc2']
    del library_wishlist_items_df['desc3']
    del library_wishlist_items_df['desc4']

    if print_tail:
        with pd.option_context('expand_frame_repr', False):
            print(library_wishlist_items_df.tail(10))
    return library_wishlist_items_df


if __name__ == '__main__':
    start_date = '2011-05-15'

    library_wishlist_items_df = generate_library_wishlist_items(True)
    write_to_sql_exec('exec_insert_library_wishlist_items.sql', library_wishlist_items_df, 'insertLibraryWishlistItem')

    books_df = generate_books_df(18, True)
    write_to_sql_exec('exec_insert_books.sql', books_df, 'insertBook')

    users_df = generate_users_df(True)
    write_to_sql_exec('exec_insert_customers.sql', users_df, 'insertCustomer')

    cards_df = generate_cards_df(True)
    write_to_sql_exec('exec_insert_cards.sql', cards_df, 'insertCard')

    customer_wishlist_items_df = generate_customer_wishlist_df(True)
    write_to_sql_exec('exec_insert_customer_wishlist_items.sql', customer_wishlist_items_df,
                      'insertCustomerWishlistItem')

    librarians_df = generate_librarian_df(True)
    write_to_sql_exec('exec_insert_librarians.sql', librarians_df, 'insertLibrarian')

    loans_df = generate_loans_df(500000, True)
    write_to_sql_exec('exec_insert_loans.sql', loans_df, 'insertLoan')
