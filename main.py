import psycopg2

conn = psycopg2.connect(database='customers_db', user='postgres', password='4160084SQL')
with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE phone_number;
        DROP TABLE personal_data;
        """)
    conn.commit()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS personal_data(
            id SERIAL PRIMARY KEY,
            name VARCHAR(120) UNIQUE NOT NULL,
            email VARCHAR(40) UNIQUE NOT NULL,
            phone_number INTEGER UNIQUE
            );
            """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id SERIAL PRIMARY KEY,
            number NUMERIC NOT NULL,
            description VARCHAR(40) NOT NULL,
            personal_data_id INTEGER NOT NULL REFERENCES personal_data(id)
            );
            """)
    conn.commit()

    cur.execute("""
        INSERT INTO personal_data(name,email) VALUES('Alexandr Pegov','pegov@gmail.com') RETURNING id, name,email;
        """)
    # conn.commit()

    print(cur.fetchone())

    cur.execute("""
            INSERT INTO phone_number(personal_data_id,number,description) VALUES(1,89161111111,'mobile') RETURNING id,personal_data_id,number,description;
            """)
    conn.commit()

    cur.execute("""
                INSERT INTO phone_number(personal_data_id,number,description) VALUES(1,849512222222,'home') RETURNING id,personal_data_id,number,description;
                """)
    print(cur.fetchall())
conn.close()



if __name__ == '__main__':
    pass