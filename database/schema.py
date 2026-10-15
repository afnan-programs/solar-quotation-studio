from database.connection import get_connection

def initialize_database():
    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            phone TEXT,
            logo_filename TEXT

            
            )
            """
               )
        connection.execute(
            """ 
            CREATE TABLE IF NOT EXISTS quotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quotation_number TEXT NOT NULL UNIQUE,
            company_id INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            customer_address TEXT,
            city TEXT,
            connection_type TEXT DEFAULT 'Three Phase',
            system_type TEXT DEFAULT 'Hybrid',
            system_capacity_kw REAL,
            subtotal REAL NOT NULL DEFAULT 0,
            discount REAL NOT NULL DEFAULT 0,
            grand_total REAL NOT NULL DEFAULT 0,
            terms TEXT,
            FOREIGN KEY (company_id) REFERENCES companies(id)
            )
"""
        )

    connection.execute("""
      CREATE TABLE IF NOT EXISTS quotation_items (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        quotation_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        quantity REAL NOT NULL,
        unit_price REAL NOT NULL,
        line_total REAL NOT NULL,
        FOREIGN KEY (quotation_id) REFERENCES quotations(id)
        ON DELETE CASCADE )
        
        """
    )
if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
