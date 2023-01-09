import psycopg2
import configparser
from contextlib import closing

config = configparser.ConfigParser()
config.read('setting.ini')
user = config['user']['user']
pas = config['pass']['password']


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


def _get_num_id(cursor, personal_id: int):
    """Функция выдает список номеров телефонов клиента по id"""
    cursor.execute("""
                 SELECT id, number FROM personal_data 
                 LEFT JOIN  phone_number USING (personal_id)
                 WHERE personal_id=%s;
                 """, (personal_id,))
    return cur.fetchall()


def _get_cust_data_id(cursor, personal_id: int):
    """Функция выдает список данных клиента по id"""
    cursor.execute("""
                SELECT name, surname, email, personal_id FROM personal_data 
                WHERE personal_id=%s;
                """, (personal_id,))
    return cur.fetchall()

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
    print('Структура базы данных успешно создана')
    conn.commit()

# 2. Добавление нового клиента
def add_new_cust(name, surname, email):
    cur.execute("""
        INSERT INTO personal_data(name, surname, email) VALUES (%s, %s, %s) RETURNING personal_id;
        """, (name, surname, email))
    print(f'Новый клиент внесен в базу данных c идентификатором: {cur.fetchone()[0]}')

# 3. Добавление номера телефона для существующего клиента
def add_cust_ph(surname, number, description):
    cur.execute("""
        INSERT INTO phone_number(personal_id, number, description) VALUES (%s, %s, %s) RETURNING personal_id;
        """, (_get_cust_id(cur, surname), number, description))
    print(f'Номер телефона внесен в базу данных клиенту c идентификатором: {cur.fetchone()[0]}')

# 4. Функция, позволяющая изменить данные о клиенте
def change_data(personal_id, name=None, surname=None, email=None, number=None):
    custom = _get_cust_data_id(cur, personal_id)
    if custom == []:
        print(f'Клиент с идентификатором {personal_id} не найден')
    else:
        if name is None:
            name = _get_cust_data_id(cur, personal_id)[0][0]
        if surname is None:
            surname = _get_cust_data_id(cur, personal_id)[0][1]
        if email is None:
            email = _get_cust_data_id(cur, personal_id)[0][2]
        new_data = (name, surname, email, personal_id)
        if new_data != custom[0]:
            print(f'\nПервоначальные данные по клиенту:\n{_get_cust_data_id(cur, personal_id)}')
            cur.execute("""
                            UPDATE personal_data
                            SET name=%s, surname=%s, email=%s WHERE personal_id=%s;
                            """, new_data)
            print(
                f'\nИзменения внесены в базу данных.\nНовая информация по клиенту:\n{_get_cust_data_id(cur, personal_id)}')
        else:
            print(f'Телефон(ы) клиента:\n{_get_num_id(cur, personal_id)}\n')
            id_num = input('Введите id номера, который нужно изменить: ')
            cur.execute("""
                            UPDATE phone_number SET number=%s WHERE id=%s;
                            """, (number, id_num))
            print(f'\nИзменения внесены в базу данных.\nНовый список телефонов:\n{_get_num_id(cur, personal_id)}')
    conn.commit()

# 5. Функция, позволяющая удалить телефон для существующего клиента
def del_ph_cust(personal_id):
    print(f'Найдены телефоны клиента:\n{_get_num_id(cur, personal_id)}')
    id = input('Введите id телефона, который нужно удалить:')
    cur.execute("""
        DELETE FROM phone_number
        WHERE id=%s;
        """, (id,))
    print(f'\nДанные изменены.\nНайдены телефоны клиента:\n{_get_num_id(cur, personal_id)}')
    conn.commit()

# 6. Функция, позволяющая удалить существующего клиента
def del_cust(personal_id):
    if _get_cust_data_id(cur, personal_id) == []:
        print(f'Клиент с идентификатором {personal_id} не найден')
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
            f'\nДанные изменены.\nКлиент с идентификатором {personal_id} удален из базы данных:\n{_get_cust_data_id(cur, personal_id)}')
    conn.commit()

if __name__ == '__main__':

    with closing(psycopg2.connect(database='customers_db', user=user, password=pas)) as conn:
        with conn.cursor() as cur:

            # _drop_tab()

            # create_tabs()
            # add_new_cust('Denis', 'Maka12rov', 'makarov_d@gmail.com')
            # add_cust_ph('Makarov', 84992586023, 'рабочий')
            # change_data(1, number='84955552288')

            # del_ph_cust(1)
            # del_cust(1)