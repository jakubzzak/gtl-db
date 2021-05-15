import pandas as pd
import numpy as np
import random


# @ssn 0 varchar(20), @email 1 varchar(100), @password 2 varchar(60), @first_name 3 varchar(100),
# @last_name 4 varchar(100), @campus_id 5 int, @user_type 6 varchar(20),
# @can_reserve 7 bit, @can_borrow 8 bit, @books_borrowed 9 smallint, @books_reserved 10 smallint,
# @is_active 11 bit, @street 12 varchar(150), @street_number 13 varchar(50), @city 14 varchar(100),
# @post_code 15 varchar(20),
# @country 16 varchar(100), @phone_country_code 17 as varchar(5), @phone_number 18 varchar(15),
# @phone_type 19 varchar(30)

def yield_sql_exec(dataframe, procedure):
    for index, row in dataframe.iterrows():
        args = ','.join([str(i) if type(i) == int else '\'' + str(i) + '\'' for i in list(row.values)])
        yield "exec {procedure} {args}; go;".format(procedure=procedure, args=args)


if __name__ == '__main__':
    df = pd.read_csv('online_generator_scripts/users.csv')

    rows = len(df.index)
    df.insert(5, 'campus_id', np.random.randint(1, 8, rows))
    df.insert(6, 'user_type', random.choices(['STUDENT', 'PROFESSOR'], (rows, 150), k=rows))
    df.insert(7, 'can_reserve', random.choices([0, 1], (20, rows), k=rows))
    df.insert(8, 'can_borrow', random.choices([0, 1], (20, rows), k=rows))
    df.insert(9, 'books_borrowed', 0),
    df.insert(10, 'books_reserved', 0),
    df.insert(11, 'is_active', random.choices([0, 1], (1000, rows), k=rows)),
    df.insert(13, 'street_number', np.random.randint(1, 200, rows)),
    df.insert(15, 'post_code', np.random.randint(1, 10000, rows)),
    df.insert(17, 'phone_country_code', np.random.randint(1, 999, rows)),
    df.insert(19, 'phone_type', random.choices(['HOME', 'OFFICE', 'MOBILE'], (500, 700, rows), k=rows))

    with pd.option_context('expand_frame_repr', False):
        print(df.head(10))

    with open('final_output/exec_insert_users.sql', mode='w+') as file:
        print('set nocount on;', file=file)
        for sql_statement in yield_sql_exec(df, 'insertCustomer'):
            print(sql_statement, file=file)
        print('set nocount off;', file=file)

