DB scripts for GTL, realistic data initialization
==

To successfully initialize mssql database with this data follow the following steps in this particular order:

- Run the **sql_generator.py** to generate new SQL insert data scripts to the final_output folder
- Execute **create_db.sql** script against your database
- Run all the procedures found in **stored_procedure/** folder
- Create triggers sored in **triggers/** folder
- UCN campuses need to be added respectively, run **exec_insert_campus.sql** from the **hardcoded/** folder
- In the end execute all of the following files in **final output/** folder in this specific order:
    - exec_insert_librarians.sql
    - exec_insert_books.sql
    - exec_insert_library_wishlist_items.sql
    - exec_insert_customers.sql
    - exec_insert_cards.sql
    - exec_insert_customer_wishlist_items.sql
    - exec_insert_loans.sql
