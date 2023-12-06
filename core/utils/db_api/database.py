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
            phone_number TEXT,
            username TEXT DEFAULT "null",
            fullname TEXT DEFAULT "null"
            );
            """
        self.execute(sql, commit=True)
    

    def create_table_channels(self):
        sql = """
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            channel_name TEXT,
            invite_link TEXT
            );
            """
        self.execute(sql, commit=True)

    def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            admin_id INTEGER,
            admin_name TEXT
            );
            """
        self.execute(sql, commit=True)



    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    
    # Users table functions
    # add a user to the database
    def add_user(self, user_id: int, phone_number: str = "--", status: str = "active", username: str = "null", fullname: str = "null"):
        # sql = "INSERT OR IGNORE INTO users (id, status, phone_number) VALUES (?, ?, ?)"
        sql = "INSERT OR IGNORE INTO users (id, status, phone_number, username, fullname) VALUES (?, ?, ?, ?, ?)"
        self.execute(sql, (user_id, status, phone_number, username, fullname), commit=True)

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
    
    def update_user(self, user_id, phone_number):
        sql = "UPDATE users SET phone_number = ? WHERE id = ?"
        self.execute(sql=sql,
            parameters=(phone_number, user_id,),
            commit=True
        )
    

    def contact(self, user_id):
        sql = "SELECT phone_number FROM users WHERE id = ?"
        response = self.execute(sql, parameters=(user_id,), fetchone=True)
        return response[0]

    def erase_users(self):
        sql = "DELETE FROM users"
        self.execute(sql=sql, commit=True)
    



    # Channels table functions
    # add a channel to the database
    def add_channel(self, channel_id: int, channel_name: str, invite_link: str):
        sql = "INSERT OR IGNORE INTO channels (channel_id, channel_name, invite_link) VALUES (?, ?, ?)"
        self.execute(sql, (channel_id, channel_name, invite_link), commit=True)
    
    def get_channels(self):
        sql = "SELECT channel_id FROM channels"
        all = self.execute(sql, fetchall=True)
        return [item[0] for item in all]
    
    def get_channels_data(self):
        sql = "SELECT * FROM channels"
        return self.execute(sql, fetchall=True)
    
    def in_channel(self, channel_id):
        return channel_id in self.get_channels()
    
    def delete_channel(self, channel_id):
        sql = "DELETE FROM channels WHERE channel_id = ?"
        self.execute(sql, (channel_id,), commit=True)
    
    def erase_channels(self):
        sql = "DELETE FROM channels"
        self.execute(sql=sql, commit=True)
    




    # Admins table functions
    # add a admin to the database
    def add_admin(self, admin_id: int, admin_name: str):
        sql = "INSERT OR IGNORE INTO admins (admin_id, admin_name) VALUES (?, ?)"
        self.execute(sql, (admin_id, admin_name), commit=True)
    
    def get_admins(self):
        sql = "SELECT admin_id, admin_name FROM admins"
        all = self.execute(sql, fetchall=True)
        return all
    
    def is_admin(self, admin_id):
        return admin_id in [admin[0] for admin in self.get_admins()]
    
    def delete_admin(self, admin_id):
        sql = "DELETE FROM admins WHERE admin_id = ?"
        self.execute(sql, (admin_id,), commit=True)
    
    def erase_admins(self):
        sql = "DELETE FROM admins"
        self.execute(sql, commit=True)
    

    
    
    