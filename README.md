DB scripts for GTL
==
###real data initialization

To successfully initialize mssql database with this data follow the following steps in this particular order:

- Run the **sql_generator.py** to generate new SQL insert data scripts to the final_output folder
- Execute **create_db.sql** script against your database
- Run all the procedures found in **stored_procedure/** folder
- Create triggers stored in **triggers/** folder
- Execute views from **views/** folder
- UCN campuses need to be added respectively, run **exec_insert_campus.sql** from the **hardcoded/** folder
- In the end execute all of the following files in **final_output/** folder in this specific order:
    - exec_insert_librarians.sql
    - exec_insert_books.sql
    - exec_insert_library_wishlist_items.sql
    - exec_insert_customers.sql
    - exec_insert_cards.sql
    - exec_insert_customer_wishlist_items.sql
    - exec_insert_loans.sql

Now when your database is ready take a look at:
- https://github.com/jakubzzak/georgia-tech-library (React FE)
- https://github.com/jakubzzak/gtl-backend (Flask BE) 
  
to set up the rest.

###Live demo at https://www.gtl.cybik.sk

test customer:
email=petersagan@ucn.dk, passwd=petertest

test librarian:
email=rockybalboa@ucn.dk, passwd=rockytest
