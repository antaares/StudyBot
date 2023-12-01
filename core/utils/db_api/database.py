import sqlite3





class Database:
    #  the constructor of the class
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
    


    # the property that returns the connection to the database
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    

    # the method that executes the query
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data
    


    
    




    # create a table of Users in the database
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            status TEXT,
            phone_number TEXT
            );
            """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    

    # add a user to the database
    def add_user(self, user_id: int, status: str, phone_number: str = "--"):
        sql = "INSERT OR IGNORE INTO users (id, status, phone_number) VALUES (?, ?, ?)"
        self.execute(sql, (user_id, status, phone_number), commit=True)


    # get a user from the database
    def all(self):
        sql = "SELECT id FROM users"
        all = self.execute(sql, fetchall=True)
        return [item[0] for item in all]
    

    def get_data(self):
        sql = "SELECT * FROM users"
        return self.execute(sql, fetchall=True)
    



    def restatus_users(self, inactives):
        sql = "UPDATE users SET status = 'inactive' WHERE id = ?"
        for user in inactives:
            self.execute(sql, (user,), commit=True)
    

    def inactive_users(self):
        sql = "SELECT id FROM users WHERE status = 'inactive'"
        all = self.execute(sql, fetchall=True)
        return [item[0] for item in all]

