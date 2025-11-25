
import pymysql
import pymysql.cursors
class mydb:
    def __init__(
        self,
        host="localhost",
        user="root",
        password="30102004",
        database="miniblog2",
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            if (
                self.connection is None
                or not self.connection.open
            ):
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset="utf8mb4",
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=False,   # manual commit for safety
                )
        except Exception as e:
            print("❌ Database connection error:", e)
            raise e

        return self.connection

    def get_db(self):
  
        return self.connect()
