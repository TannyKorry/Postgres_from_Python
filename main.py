import psycopg2

conn = psycopg2.connect(database='customers_db', user='postgres', password='4160084SQL')
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personal_data (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            surname VARCHAR(80) NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL,
            phone_number INTEGER UNIQUE
            );
            """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phone_number (
                id SERIAL PRIMARY KEY,
                number INTEGER NOT NULL,
                description VARCHAR(40) NOT NULL,
                personal_data_id INTEGER NOT NULL REFERENCES personal_data(id)
                );
                """)
    conn.commit()
conn.close()



if __name__ == '__main__':
    pass