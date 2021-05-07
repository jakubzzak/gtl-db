import random
import math
import re
from datetime import timedelta, date, datetime


def wrap(data: [int, str]) -> str:
    return '\'' + str(data) + '\''


def refactor_book_export(readfile: str, writefile: str) -> None:
    resource_type = [
        'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK',
        'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK',
        'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK', 'BOOK',
        'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE', 'ARTICLE',
        'JOURNAL', 'JOURNAL', 'JOURNAL', 'JOURNAL', 'JOURNAL', 'JOURNAL',
        'REFERENCE', 'REFERENCE', 'REFERENCE',
        'MAP',
    ]
    resource_type_len = len(resource_type)

    with open(readfile, "r") as readFile:
        with open(writefile, "w") as writeFile:
            countLine = 0
            for line in readFile:
                if len(line.strip()) == 0:
                    continue
                line = line.replace("MOCKDATA", "book")
                new_line = line.split("VALUES(")
                values = new_line[1].split(",")
                values[3] = values[3].split(');')[0]  # removes the end bracket
                random_resource_type = resource_type[random.randint(0, resource_type_len - 1)]
                values.append(wrap(''))  # description
                if random.randint(0, 1000) < 8:  # is_loanable
                    values.append(wrap(0))
                else:
                    values.append(wrap(1))
                num_of_book = math.floor(10 - math.sqrt(random.randint(0, 100)))
                if num_of_book != 10:
                    num_of_book += 1
                else:
                    num_of_book = 0
                values.append(wrap(num_of_book))  # total_copies
                values.append(wrap(num_of_book))  # available_copies
                values.append(wrap(random_resource_type))  # description
                for i in range(len(values)):
                    if len(values[i]) == 0:
                        continue
                    if values[i][0] == '\'' and '\'' in values[i][1:len(values[i]) - 1]:
                        values[i] = '\'' + values[i][1:len(values[i]) - 1].replace('\'', '\'\'').strip() + '\''
                    elif values[i][0] == '\'':
                        values[i] = '\'' + values[i][1:len(values[i]) - 1].strip() + '\''
                new_line[1] = ','.join(values)
                writeFile.write('VALUES('.join(new_line) + ');\n')
                countLine += 1


def refactor_user_data_export():
    role = [
        'departmental_associate', 'departmental_associate',
        'reference', 'reference', 'reference', 'reference',
        'check_out', 'check_out', 'check_out', 'check_out', 'check_out', 'check_out',
        'assistant', 'assistant', 'assistant', 'assistant', 'assistant', 'assistant', 'assistant', 'assistant',
        'assistant'
    ]

    with open("user_data.sql", "r") as readFile:
        with open("user_data_export.sql", "w") as writeFile:
            count = 0
            for line in readFile:
                if len(line.strip()) == 0:
                    continue
                line = line.replace("MOCKDATA", "user_data")
                new_line = line.split('(')
                values = new_line[1].split(",")
                values = values[:-1]
                if count == 0:
                    values.append('\'CHIEF\');')
                else:
                    values.append('\'' + role[random.randint(0, len(role) - 1)].upper() + '\');')
                new_line[1] = ','.join(values)
                writeFile.write('('.join(new_line) + '\n')
                count += 1


def refactor_address_export():
    states = [
        'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark', 'Denmark',
        'Denmark',
        'Slovakia',
        'Poland', 'Poland', 'Poland', 'Poland',
        'Germany', 'Germany'
    ]

    with open("address.sql", "r") as readFile:
        with open("insert_data_scripts/address_export2.sql", "w") as writeFile:
            count = 0
            for line in readFile:
                if len(line.strip()) == 0:
                    continue
                line = line.replace("MOCKDATA", "address").strip()
                new_line = line.split('VALUES(')
                values = new_line[1].split(",")
                if len(values) != 4:
                    continue

                values[1] = '\'' + str(random.randint(1, 6500)) + '\''
                values.insert(3, '\'' + str(random.randint(2000, 99999)) + '\'')
                # values[3] = '\'' + states[random.randint(0, len(states)-1)] + '\');'

                new_line[1] = ','.join(values)
                writeFile.write('VALUES('.join(new_line[:2]) + '\n')
                count += 1


def refactor_customer_export():
    campus = [
        'Hobrovej 85, Aalborg', 'Lerpyttervej 43, Thisted', 'Mylius Erichsens Vej 137, Aalborg SØ',
        'Selma Lagerløfs Vej 2, Aalborg Øst', 'Skolevangen 45, Hjørring', 'Sofiendalsvej 60, Aalborg SV'
    ]
    customer_type = ['student'] * 50
    customer_type.append('professor')

    address_ids = []
    with open('address_export.sql', 'r') as readAddress:
        for line in readAddress:
            if len(line.strip()) == 0:
                continue
            values = re.split(',|\(|\);', line)
            address_ids.append(values[1])

    books_loaned_already = 0
    for fileName in ['bookFirstHalf.sql', 'bookSecondHalf.sql']:
        with open(fileName, 'r') as readBook:
            for line in readBook:
                if len(line.strip()) == 0:
                    continue
                values = re.split(',|\(|\);', line)
                books_loaned_already += (int(values[-3]) - int(values[-2]))

    with open('customer.sql', 'r') as readFile:
        with open('customer_export.sql', 'w') as writeFile:
            count = 0
            for line in readFile:
                if len(line.strip()) == 0:
                    continue
                line = line.replace("MOCKDATA", "customer").strip()
                values = re.split(',|\(|\);', line)
                values[2] = 'N\'' + campus[random.randint(0, len(campus) - 1)] + '\''
                values[3] = address_ids.pop(random.randint(0, len(address_ids) - 1))
                if books_loaned_already > 5:
                    loan_count = random.randint(0, 5)
                    values[-3] = str(loan_count)
                    books_loaned_already -= loan_count
                elif books_loaned_already > 0:
                    values[-3] = str(books_loaned_already)
                    books_loaned_already = 0
                else:
                    values[-3] = str(0)
                values[-2] = '\'' + customer_type[random.randint(0, len(customer_type) - 1)].upper() + '\''
                writeFile.write(values[0] + '(' + ','.join(values[1:-1]) + ');\n')
                count += 1
    print('done')


def refactor_wish_list_export():
    books_missing_ids = []
    for fileName in ['bookFirstHalf.sql', 'bookSecondHalf.sql']:
        with open(fileName, 'r') as readBook:
            for line in readBook:
                if len(line.strip()) == 0:
                    continue
                values = re.split(',|\(|\);', line)
                if int(values[-3]) == 0 and random.randint(0, 5) == 0:
                    books_missing_ids.append(values[1])
                elif int(values[-3]) == 1 and random.randint(0, 300) == 0:
                    books_missing_ids.append(values[1])
                elif int(values[-3]) == 2 and random.randint(0, 400) == 0:
                    books_missing_ids.append(values[1])

    with open('wish_list_export.sql', 'w') as writeFile:
        for book_id in books_missing_ids:
            writeFile.write(
                "INSERT INTO wish_list VALUES(" + book_id + "," + str(1 if random.randint(0, 15) == 0 else 0) + ");\n")


class Customer:

    def __init__(self, values):
        self.id = values[1]
        self.card_issued_at = datetime.strptime(values[-4][1:-1], '%m/%d/%Y').date()
        self.books_out = int(values[-3])


def refactor_loans_history_export(writeFileName, tableName, countRecords):
    books_ids = []
    books_out_ids = []
    customers = []

    with open("./insert_data_scripts/book_export.sql", 'r') as readBook:
        for line in readBook:
            if len(line.strip()) == 0 or 'INSERT' not in line:
                continue
            values = re.split(',|\(|\);', line)
            books_ids.append(values[1])
            for i in range(int(values[-3]) - int(values[-2])):
                books_out_ids.append(values[1])

    with open('./insert_data_scripts/customer_export.sql', 'r') as readCustomer:
        for line in readCustomer:
            if len(line.strip()) == 0 or 'INSERT' not in line:
                continue
            values = re.split(',|\(|\);', line)
            if random.randint(0, 4) > 0:
                customers.append(Customer(values))

    books_total_count = len(books_ids)
    books_out_count = len(books_out_ids)
    customers_count = len(customers)
    with open(writeFileName, 'w') as writeHistory:
        # todo: random history
        for i in range(0, countRecords - books_out_count):
            random_book_id = books_out_ids[random.randint(0, books_out_count - 1)]
            random_customer = customers[random.randint(0, customers_count - 1)]

            day_difference = (date.today() - random_customer.card_issued_at).days - 30
            date_out = random_customer.card_issued_at + timedelta(days=random.randint(0, max(1, day_difference)))
            if random.randint(0, 1500):
                date_in = date_out + timedelta(days=random.randint(1, 35))
                writeHistory.write(
                    "INSERT INTO " + tableName + " VALUES(" + random_book_id + "," + random_customer.id + ",'" + str(
                        date_out) + "','" + str(date_in) + "');\n")

            else:
                writeHistory.write(
                    "INSERT INTO " + tableName + " VALUES(" + random_book_id + "," + random_customer.id + ",'" + str(
                        date_out) + "'," + "null);\n")
        # todo: currently out
        for customer in customers:
            for count in range(customer.books_out):
                random_book_id = books_out_ids.pop(random.randint(0, books_out_count - 1))
                books_out_count -= 1
                date_out = date.today() - timedelta(days=random.randint(1, 35))
                writeHistory.write(
                    "INSERT INTO " + tableName + " VALUES(" + random_book_id + "," + customer.id + ",'" + str(
                        date_out) + "'," + "null);\n")


def clusterInserts(readFileName, writeFileName, groupLength=10000):
    with open(readFileName, "r") as readFile:
        with open(writeFileName, "w") as writeFile:
            writeFile.write('SET NOCOUNT ON;\n')
            counter = 0
            for line in readFile:
                writeFile.write(line)
                if counter + 1 == groupLength:
                    counter = 0
                    writeFile.write('GO;\n')
                else:
                    counter += 1
            writeFile.write('SET NOCOUNT OFF;\n')


def test():
    # temp = "..values('ahojky','nieco ine');"
    # print('temp here', re.split(',|\(|\);', temp))
    # temp = ['sth'] * 20
    # temp.append('sth else')
    # print(temp)

    issued_date = date.fromisoformat("2010-08-27")
    day_difference = (date.today() - issued_date).days - 30
    temp = issued_date + timedelta(days=random.randint(0, day_difference))
    print('random day out:', temp)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    goal_path = '/Users/jakubzzak/Developer/school/ucn/project1/db/data/'
    source_path = 'insert_data_scripts/'
    # test()

    # -- book --
    refactor_book_export(source_path + 'book_partial.sql', source_path + 'book_partial_formatted.sql')
    clusterInserts(source_path + 'book_partial_formatted.sql', goal_path + 'book.sql')
    # refactor_user_data_export()

    # -- address --
    # refactor_address_export()
    # clusterInserts('insert_data_scripts/address_export2.sql', goal_path + 'address.sql')

    # refactor_customer_export()
    # refactor_wish_list_export()
    # refactor_loans_history_export("loans_history_huge_old.sql", 'loans_history_huge', 10_000_000)
    # clusterInserts("loans_history_huge_old.sql", "loans_history_huge.sql", 10000)
