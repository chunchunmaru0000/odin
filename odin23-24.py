import sqlite3
import datetime
import pandas as pd


# documentation

'''
# DatabaseManager Class

## Overview
The `DatabaseManager` class serves as a utility for interacting with a database. It provides methods to establish
a connection, manage tables, execute queries, and perform operations such as insertion, deletion,
and updating of records.
## Methods
### \_\_init\_\_()
- Constructor method initializing the class instance.
### connection(database_name: str)
- Establishes a connection to the specified database. Any connection errors are handled and reported.
### close() -> None
- Closes the connection to the database. Any errors during the closing operation are caught and reported.
### create_table(table_name: str, properties: dict) -> None
- Creates a table in the database with the given name and properties. Any errors during table creation are reported.
### insert(table_name: str, properties: dict) -> None
- Inserts a new record into the specified table with the provided properties. This method handles different data types
and displays an error message if the insertion fails.
### query(request: str)
- Executes the SQL query specified by the request and returns the results. Any exceptions raised during 
the query execution are caught and reported.
### delete_user_by_id(user_id: int)
- Deletes a user from the 'users' table based on the provided user ID. It provides feedback on successful deletion 
or reports any errors encountered.
### update_user_by_id(user_id: int, properties: dict)
- Updates the user with the specified ID in the 'users' table using the provided properties. The method handles 
different data types and displays an error message if the update operation fails.

This class encapsulates database management functionality and error handling, making it a 
versatile tool for interacting with databases in various applications.
'''


class DatabaseManager:
    def __init__(self):
        self.connect = 0
        self.cursor = 0

    def connection(self, database_name):
        try:
            self.connect = sqlite3.connect(database_name)
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(f'failed connection, error: {e}')

    def close(self) -> None:
        try:
            self.cursor.close()
            self.connect.commit()
            self.connect.close()
            print('connection successfully closed')
        except Exception as e:
            print(f'failed close, error: {e}')

    def create_table(self, table_name: str, properties: dict) -> None:
        try:
            properties = ", ".join([f'{item[0]} {item[1]}' for item in properties.items()])
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({properties})')
            print('creation successfully completed')
        except Exception as e:
            print(f'failed creation, error: {e}')

    def insert(self, table_name, properties: dict) -> None:
        try:
            values = ", ".join([f"{chr(39) if type(value).__name__ == 'str' else ''}{value}{chr(39) if type(value).__name__ == 'str' else ''}" for value in properties.values()])
            print(f'INSERT INTO {table_name} ({", ".join(properties.keys())}) values({values})')
            self.cursor.execute(f'INSERT INTO {table_name} ({", ".join(properties.keys())}) values({values})')
            self.connect.commit()
            print('insertion successfully completed')
        except Exception as e:
            print(f'failed insertion, error: {e}')

    def query(self, request: str):
        try:
            self.cursor.execute(request)
            print('query successfully completed')
            return self.cursor.fetchall()
        except Exception as e:
            print(f'failed query, error: {e}')

    def delete_user_by_id(self, user_id: int):
        try:
            self.cursor.execute(f'delete from users where id={user_id}')
            print(f'user с id {user_id} successfully deleted')
        except Exception as e:
            print(f'failed deletion, error: {e}')

    def update_user_by_id(self, user_id: int, properties: dict):
        try:
            properties = ", ".join([f'{item[0]}={chr(39) if type(item[1]).__name__ == "str" else ""}{item[1]}{chr(39) if type(item[1]).__name__ == "str" else ""}' for item in properties.items()])
            self.cursor.execute(f'update users set {properties} where id={user_id}')
            print(f'user with id {user_id} successfully updated')
        except Exception as e:
            print(f'failed updation, error: {e}')


class Solution:
    # создание
    @staticmethod
    def creating_tables(base: DatabaseManager):
        base.create_table('users',
                          {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                           'name': 'TEXT',
                           'age': 'INTEGER',
                           'email': 'TEXT'
                           })

        # жаль sqlLite нет timestamp как в mysql
        base.create_table('orders',
                          {'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                           'user_id': 'INTEGER',
                           'buying_time': 'TEXT',
                           'price': 'REAL',
                           'FOREIGN KEY(user_id)': 'REFERENCES users(id)'
                           })

    # заполнение
    @staticmethod
    def primer_zapolneniya_tablici(base: DatabaseManager):
        base.insert('users', {'name': 'Вова',
                                                 'age': 8,
                                                 'email': 'bebra228@gmail.com'})
        [base.insert('users', {'name': f'чел{i}',
                                                 'age': 20+i,
                                                 'email': f'chel{i}@gmail.com'})
         for i in range(100)]

        base.insert('orders', {'user_id': 1, 'buying_time': str(datetime.datetime.now()), 'price': 100})
        base.insert('orders', {'user_id': 3, 'buying_time': str(datetime.datetime.now()), 'price': 1000})
        base.insert('orders', {'user_id': 4, 'buying_time': str(datetime.datetime.now()), 'price': 10000})
        base.insert('orders', {'user_id': 2, 'buying_time': str(datetime.datetime.now()), 'price': 1000})
        base.insert('orders', {'user_id': 1, 'buying_time': str(datetime.datetime.now()), 'price': 1000000})
        base.insert('orders', {'user_id': 9, 'buying_time': str(datetime.datetime.now()), 'price': 1488})
        base.insert('orders', {'user_id': 9, 'buying_time': str(datetime.datetime.now()), 'price': 1488})

    # запросы
    @staticmethod
    def quires(base: DatabaseManager):
        pd.set_option('display.max_columns', None)
        print('#'*100)
        print('Получить всех пользователей старше определенного возраста')
        df1 = base.query('select name, age from users where age > 25')
        df1 = {'name': [*map(lambda x: x[0], df1)],
               'age': [*map(lambda x: x[1], df1)]}
        df1 = pd.DataFrame(df1)
        print(df1)

        print('#'*100)
        print('Найти все заказы, сделанные конкретным пользователем')
        df2 = base.query('select * from orders where user_id = 1')
        df2 = {'id заказов сделанные Вова(user_id = 1)': [*map(lambda x: x[0], df2)],
               'user_id': [*map(lambda x: x[1], df2)],
               'buying_time': [*map(lambda x: x[2], df2)],
               'price': [*map(lambda x: x[3], df2)]}
        df2 = pd.DataFrame(df2)
        print(df2)

        print('#'*100)
        print('Вычислить общую сумму заказов для каждого пользователя.')
        df3 = base.query('select user_id, sum(price) from orders group by user_id')
        df3 = {'user_id': [*map(lambda x: x[0], df3)],
               'sum(price)': [*map(lambda x: x[1], df3)]}
        df3 = pd.DataFrame(df3)
        print(df3)

    @staticmethod
    def deletion_example(base: DatabaseManager):
        base.delete_user_by_id(13)

    @staticmethod
    def updation_example(base: DatabaseManager):
        base.update_user_by_id(7, {'age': 400, 'name': 'Ящер'})


if __name__ == '__main__':
    database = DatabaseManager()
    database.connection('23-24zadanie.db')
    
    Solution.creating_tables(database)
    Solution.primer_zapolneniya_tablici(database)
    Solution.updation_example(database)
    Solution.quires(database)
    Solution.deletion_example(database)
    
    database.close()
