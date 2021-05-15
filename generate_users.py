import random
from datetime import timedelta, datetime
from random import randrange
import numpy as np
import pandas as pd
import uuid
import math

# @ssn 0 varchar(20), @email 1 varchar(100), @password 2 varchar(60), @first_name 3 varchar(100),
# @last_name 4 varchar(100), @campus_id 5 int, @user_type 6 varchar(20),
# @can_reserve 7 bit, @can_borrow 8 bit, @books_borrowed 9 smallint, @books_reserved 10 smallint,
# @is_active 11 bit, @street 12 varchar(150), @street_number 13 varchar(50), @city 14 varchar(100),
# @post_code 15 varchar(20),
# @country 16 varchar(100), @phone_country_code 17 as varchar(5), @phone_number 18 varchar(15),
# @phone_type 19 varchar(30)

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


if __name__ == '__main__':
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
    users_df.insert(20, 'registered_at', random_dates(pd.to_datetime('2011-05-15'), pd.to_datetime("now"), user_rows))

    write_to_sql_exec('exec_insert_users.sql', users_df, 'insertCustomer')

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

        max_wishlist = 15
        wishlist_count = max_wishlist - math.sqrt(random.randint(0, max_wishlist**2))
        if wishlist_count >= 15:
            wishlist_count = 0
        else:
            wishlist_count += 1

    cards_df = pd.DataFrame(cards)
    write_to_sql_exec('exec_insert_cards.sql', cards_df, 'insertCard')
