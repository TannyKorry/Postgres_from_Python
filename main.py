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
        # ВСПОМОГАТЕЛЬНЫЕ
        # Удаление таблиц
        def _drop_tab():
            cur.execute("""
                DROP TABLE phone_number;
                DROP TABLE personal_data;
                """)
            conn.commit()

        # Запрос находит id клиента по фамилии
        def _get_cust_id(cursor, surname: str) -> int:
            cursor.execute("""
                    SELECT id FROM personal_data WHERE surname=%s;
                    """, (surname,))
            return cur.fetchone()[0]

        # Функция выдает список данных по клиентам и номерам телефонов
        def _get_cust_data(cursor):
            cursor.execute("""
                    SELECT * FROM personal_data JOIN phone_number ON personal_data.id=personal_data_id 
                    ORDER BY personal_data.id;
                    """)
            return cur.fetchall()

        # Запрос находит id клиента по номеру телефона
        def _get_cust_id_num(cursor, number: str) -> int:
            cursor.execute("""
                        SELECT personal_data.id FROM personal_data JOIN phone_number ON personal_data.id=personal_data_id 
                        WHERE number=%s;
                        """, (number,))
            return cur.fetchone()[0]
####################################################################################################################################
        # 1. Создание структуры БД
        def create_tabs():
            cur.execute("""
                CREATE TABLE IF NOT EXISTS personal_data(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(20),
                    surname VARCHAR(30),
                    email VARCHAR(40) UNIQUE NOT NULL
                    );
                    """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phone_number(
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(15) UNIQUE NOT NULL,
                    description VARCHAR(40),
                    personal_data_id INTEGER NOT NULL REFERENCES personal_data(id)
                    );
                    """)
            conn.commit()

        # 2. Добавление нового клиента
        def add_new_cust(name, surname, email):
            cur.execute("""
                    INSERT INTO personal_data(name, surname, email) VALUES (%s, %s, %s);
                    """, (name, surname, email))
            conn.commit()

        # 3. Добавление номера телефона для существующего клиента
        def add_cust_ph(surname, number, description):
            cur.execute("""
                    INSERT INTO phone_number(personal_data_id, number, description) VALUES (%s, %s, %s);
                    """, (_get_cust_id(cur, surname), number, description))
            conn.commit()

        # 4. Функция, позволяющая изменить данные о клиенте
        def change_data(id, name=None,surname=None, email=None):
            _get_cust_data(cur)



            cur.execute("""
                        UPDATE personal_data SET name=%s, surname=%s, email=%s WHERE id=%s;
                        """, (name, surname, email, id))
            conn.commit()


        # 5. Функция, позволяющая удалить телефон для существующего клиента
        def del_ph_cust(id):
            pass
        # 6. Функция, позволяющая удалить существующего клиента
        def del_cust(id):
            pass

        # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email или телефону)
        #  _get_cust_data(cur, ): # Функция выдает список данных по клиентам и номерам телефонов
        #



        if __name__ == '__main__':
            # _drop_tab()
            # create_tabs()
            # add_new_cust('Denis', 'Makarov', 'makarov_d@gmail.com')
            # add_cust_ph('Pegov', 84955552233, 'рабочий')
            print(_get_cust_data(cur))
            # change_data(1,'Alexandr', 'Pegov', 'pegov@gmail.com')
            # print(_get_cust_id_num(cur, '84955552233'))