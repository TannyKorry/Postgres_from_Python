import psycopg2
import configparser
from contextlib import closing

config = configparser.ConfigParser()
config.read('setting.ini')
user = config['user']['user']
pas = config['pass']['password']

with closing(psycopg2.connect(database='customers_db', user=user, password=pas)) as conn:
    with conn.cursor() as cur:

        def _drop_tab():
            """Функция удаления таблиц"""
            cur.execute("""
                DROP TABLE phone_number;
                DROP TABLE personal_data;
                """)
            conn.commit()


        def _get_cust_id(cursor, surname: str) -> int:
            """Запрос находит id клиента по фамилии"""
            cursor.execute("""
                    SELECT personal_id FROM personal_data WHERE surname=%s;
                    """, (surname,))
            return cur.fetchone()[0]


        def _get_cust_data(cursor):
            """Функция выдает список данных по клиентам и номерам телефонов"""
            cursor.execute("""
                    SELECT * FROM personal_data LEFT JOIN phone_number USING (personal_id);
                    """)
            return cur.fetchall()


        def _get_cust_data_id(cursor, personal_id: int):
            """Функция выдает список данных клиента по id"""
            cursor.execute("""
                        SELECT name, surname, email, personal_id FROM personal_data 
                        WHERE personal_id=%s;
                        """, (personal_id,))
            return cur.fetchall()


        def _get_cust_id_num(cursor, number: str) -> int:
            """Функция находит id клиента по номеру телефона"""
            cursor.execute("""
                        SELECT personal_data.id FROM personal_data LEFT JOIN phone_number USING (personal_id) 
                        WHERE number=%s;
                        """, (number,))
            return cur.fetchone()[0]


        def _get_num_id(cursor, personal_id: int):
            """Функция выдает список номера телефонов клиента по id"""
            cursor.execute("""
                         SELECT id, number FROM personal_data 
                         LEFT JOIN  phone_number USING (personal_id)
                         WHERE personal_id=%s;
                         """, (personal_id,))
            return cur.fetchall()


        ################################################################################################################
        # 1. Создание структуры БД
        def create_tabs():
            cur.execute("""
                CREATE TABLE IF NOT EXISTS personal_data(
                    personal_id SERIAL PRIMARY KEY,
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
                    personal_id INTEGER REFERENCES personal_data(personal_id)
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
                    INSERT INTO phone_number(personal_id, number, description) VALUES (%s, %s, %s);
                    """, (_get_cust_id(cur, surname), number, description))
            conn.commit()


        # 4. Функция, позволяющая изменить данные о клиенте
        def change_data(personal_id, name=None, surname=None, email=None, number=None): # МЕНЯЕТ ВСЕ КРОМЕ ТЕЛЕФОНА
            custom = _get_cust_data_id(cur, personal_id)[0]
            if name is None:
                name = _get_cust_data_id(cur, personal_id)[0][0]
            if surname is None:
                surname = _get_cust_data_id(cur, personal_id)[0][1]
            if email is None:
                email = _get_cust_data_id(cur, personal_id)[0][2]
            new_data = (name, surname, email, personal_id)
            if new_data != custom:
                print(f'\nПервоначальные данные по клиенту:\n{_get_cust_data_id(cur, personal_id)}')
                cur.execute("""
                    UPDATE personal_data
                    SET name=%s, surname=%s, email=%s WHERE personal_id=%s;
                    """, new_data)
                print(f'\nИзменения внесены в базу данных.\nНовая информация по клиенту:\n{_get_cust_data_id(cur, personal_id)}')
            else:
                print(f'Телефон(ы) клиента:\n{_get_num_id(cur, personal_id)}')
                cur.execute("""
                    UPDATE phone_number SET number=%s WHERE personal_id=%s;
                    """, (number, personal_id))
                print(_get_num_id(cur, personal_id))

            conn.commit()


        # 5. Функция, позволяющая удалить телефон для существующего клиента ГОТОВО!
        def del_ph_cust(personal_id):
            print(f'Найдены телефоны клиента:\n{_get_num_id(cur, personal_id)}')
            id = input('Введите id телефона, который нужно удалить:')
            cur.execute("""
                DELETE FROM phone_number
                WHERE id=%s;
                """, (id,))
            print(f'\nДанные изменены.\nНайдены телефоны клиента:\n{_get_num_id(cur, personal_id)}')
            conn.commit()

        # 6. Функция, позволяющая удалить существующего клиента ГОТОВО!
        def del_cust(personal_id):
            if _get_cust_data_id(cur, personal_id) == []:
                print(f'Клиент с этим идентификатором {personal_id} не найден')
            else:
                print(f'Найдены данные клиента:\n{_get_cust_data_id(cur, personal_id)}')
                cur.execute("""
                    DELETE FROM phone_number
                    WHERE personal_id=%s;
                    """, (personal_id,))
                cur.execute("""
                    DELETE FROM personal_data
                    WHERE personal_id=%s;
                    """, (personal_id,))
                print(
                    f'\nДанные изменены.\nКлиент с идентификатором {personal_id} удален:\n{_get_cust_data_id(cur, personal_id)}')
            conn.commit()


        # 7. Функция, позволяющая найти клиента по его данным (имени, фамилии, email или телефону)

        if __name__ == '__main__':
            # _drop_tab()
            # create_tabs()
            # add_new_cust('Svetlana', 'Kozyreva', 'sveta@mail.ru')
            # add_cust_ph('Makarov', 84992586023, 'рабочий')
            # change_data(1, number='84955552288')
            # print(_get_cust_id_num(cur, '84955552233'))
            # del_ph_cust(1)
            del_cust(1)
#[(2, 'Alexandr', 'Pegov', 'pegov@gmail.com', 1, '84955552233', 'рабочий'), (2, 'Alexandr', 'Pegov', 'pegov@gmail.com', 2, '89161566861', 'мобильный'), (1, 'Denis', 'Makarov', 'makarov_d@gmail.com', 3, '89257617896', 'мобильный'), (1, 'Denis', 'Makarov', 'makarov_d@gmail.com', 4, '84992586023', 'рабочий'), (3, 'Svetlana', 'Kozyreva', 'sveta@mail.ru', None, None, None)]
