import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()

    def sql_query(self, query: str):
        answer = self.cur.execute(query)
        return answer.fetchall()

    def insert_into(self, table_name: str, params: dict):
        values = ", ".join([f"'{str(i)}'" for i in params.values()])
        columns = ", ".join(params.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.sql_query(query)

    def select_from(self, table_name: str, columns: list, where: dict = None,
                    join_table: str = None, join_columns: tuple = None):
        columns = ", ".join(columns)
        query = f"SELECT {columns} FROM {table_name}"
        if join_table:
            join_table = f" JOIN {join_table} on {join_table}.{join_columns[0]} = {table_name}.{join_columns[1]}"
            query += join_table
        if where:
            where = " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
            query += where
        return self.sql_query(query)

    def update_data(self, table_name: str, params: dict, where: dict = None):
        set_columns = ", ".join([f"{key} = '{value}'" for key, value in params.items()])
        query = f"UPDATE {table_name} SET {set_columns}"
        if where:
            where = " WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
            query += where
        return self.sql_query(query)

    def delete_from(self, table_name: str, where: dict):
        query = f"DELETE FROM {table_name} WHERE " + " AND ".join([f"{key} = '{value}'" for key, value in where.items()])
        return self.sql_query(query)


with SQLiteDB("dish.db") as db:
    db.update_data("user_order", {"order_price": 200}, {"id": 4})
