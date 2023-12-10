import psycopg2

with psycopg2.connect(database="clients", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        def create_tables(cur):
            cur.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(40) NOT NULL,
                    last_name VARCHAR(40) NOT NULL,
                    email VARCHAR(80) UNIQUE NOT NULL
                );
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS phones (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES clients(id),
                    phone VARCHAR(20) UNIQUE
                );
            ''')

        def add_client(cur, first_name, last_name, email):
            cur.execute('''
                INSERT INTO clients (first_name, last_name, email) VALUES (%s, %s, %s)
            ''', (first_name, last_name, email))

        def add_phone(cur, client_id, phone):
            cur.execute('''
                INSERT INTO phones (client_id, phone) VALUES (%s, %s)
            ''', (client_id, phone))

        def change_client(cur, client_id, new_first_name=None, new_last_name=None, new_email=None):
            update_query = 'UPDATE clients SET '
            update_values = []
            if new_first_name:
                update_query += 'first_name = %s, '
                update_values.append(new_first_name)
            if new_last_name:
                update_query += 'last_name = %s, '
                update_values.append(new_last_name)
            if new_email:
                update_query += 'email = %s, '
                update_values.append(new_email)

            update_query = update_query.rstrip(', ')

            update_query += ' WHERE id = %s'
            update_values.append(client_id)
            cur.execute(update_query, tuple(update_values))

        def delete_phone(cur, client_id, phone):
            cur.execute('''
                DELETE FROM phones WHERE client_id = %s AND phone = %s
            ''', (client_id, phone))

        def delete_client(cur, client_id):
            cur.execute('''
                DELETE FROM clients WHERE id = %s
            ''', (client_id,))

        def find_client(cur, first_name=None, last_name=None, email=None):
            search_query = 'SELECT * FROM clients WHERE '
            search_values = []
            if first_name:
                search_query += 'first_name = %s AND '
                search_values.append(first_name)
            if last_name:
                search_query += 'last_name = %s AND '
                search_values.append(last_name)
            if email:
                search_query += 'email = %s AND '
                search_values.append(email)

            search_query = search_query.rstrip(' AND ')

            cur.execute(search_query, tuple(search_values))
            return cur.fetchall()


