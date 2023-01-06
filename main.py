import psycopg2
import configparser
from pprint import pprint
from contextlib import closing


config = configparser.ConfigParser()
config.read('setting.ini')
user = config['user']['user']
pas = config['pass']['password']

with closing (psycopg2.connect(database='customers_db', user=user, password=pas)) as conn:

    with conn.cursor() as cur:

        # 1. Создание структуры БД
        def create_tabs():
            cur.execute("""
                CREATE TABLE IF NOT EXISTS personal_data(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(120) UNIQUE NOT NULL,
                    email VARCHAR(40) UNIQUE NOT NULL
                    );
                    """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phone_number(
                    id SERIAL PRIMARY KEY,
                    number NUMERIC UNIQUE NOT NULL,
                    description VARCHAR(40) NOT NULL,
                    personal_data_id INTEGER NOT NULL REFERENCES personal_data(id)
                    );
                    """)
            conn.commit()


        # Запрос находит id клиента по имени
        def _get_cust_id(cursor, name: str) -> int:
            cursor.execute("""
                SELECT id FROM personal_data WHERE name=%s;
                """, (name,))
            return cur.fetchone()[0]


        ID = _get_cust_id(cur, 'Alexa')



        # if ID == NONE:
        #     print('нет такого', ID)
        # else:
        #     print('V')

        # 2. Добавление нового клиента
        def add_new_cust(name, email):
            cur.execute("""
                    INSERT INTO personal_data(name, email) VALUES (%s, %s);
                    """, (name, email))
            conn.commit()

        # 3. Добавление номера телефона для существующего клиента
        def add_cust_ph(name, number, description):
            cur.execute("""
                    INSERT INTO phone_number(personal_data_id, number, description) VALUES (%s, %s, %s);
                    """, (_get_cust_id(cur, name), number, description))
            conn.commit()

        # create_tabs()
        # add_new_cust('Alexandr Pegov', 'peg47ov@gmail.com')
        # add_cust_ph('Alexandr Pegov', 89166582244, 'мобильный')



        # print(cur.fetchone())
        #
        # cur.execute("""
        #         INSERT INTO phone_number(personal_data_id,number,description) VALUES(1,89161111111,'mobile') RETURNING id,personal_data_id,number,description;
        #         """)
        # conn.commit()
        #
        # cur.execute("""
        #             INSERT INTO phone_number(personal_data_id,number,description) VALUES(1,84952222222,'home') RETURNING id,personal_data_id,number,description;
        #             """)
        #
        # conn.commit()
        # print(cur.fetchone())





            # create_tabs()
            # add_cust('Alexandr Pegov', 'pegov@gmail.com')