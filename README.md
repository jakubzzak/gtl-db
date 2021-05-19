db scripts for gtl

1. Run the sql_generator.py. It will generate new SQL scripts to the final_output folder.
2. Run the SQL queries in the following order:
- **create_db.sql**
- all the procedures from the **stored_procedure** folder
- triggers from the **triggers** folder
- **exec_insert_campus.sql** from the **hardcoded** folder
- files from the **final output**:
    - exec_insert_campus.sql
    - exec_insert_librarians.sql
    - exec_insert_books.sql
    - exec_insert_library_wishlist_items.sql
    - exec_insert_customers.sql
    - exec_insert_cards.sql
    - exec_insert_customer_wishlist_items.sql
    - exec_insert_loans.sql
