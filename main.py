import psycopg2

conn = psycopg2.connect(database='customers_db', user='postgres', password='4160084SQL')
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS personal_data (
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            surname VARCHAR(80) NOT NULL,
            email VARCHAR(40) NOT NULL,
            phone_number INTEGER UNIQUE
            );
            """)
    conn.commit()
conn.close()



if __name__ == '__main__':
    pass