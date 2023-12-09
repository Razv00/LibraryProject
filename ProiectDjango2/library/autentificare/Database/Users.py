
class Users:
    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor

    def createUserTable(self):
        self.cursor.execute(
            """
            CREATE TABLE userss (
                id integer PRIMARY KEY,
                name VARCHAR2(100) UNIQUE NOT NULL,
                password VARCHAR2(40)
                )
            """
        )
        self.cursor.execute(
            """
            CREATE SEQUENCE userss_seq
                START WITH 1
                INCREMENT BY 1
                NOMAXVALUE
                NOCACHE
            """
        )

    def createUserTrigger(self):
        self.cursor.execute(
            """
            CREATE OR REPLACE TRIGGER userss_trigger
                BEFORE INSERT ON userss
                FOR EACH ROW
            BEGIN
                :new.id := userss_seq.NEXTVAL;
            END;
            """
        )
    ## GET USER
    def getUserDataByName(self, name):
        self.cursor.execute(
            "SELECT *  "
            "FROM userss "
            "WHERE name=:name",
            {"name": name}
        )
        user_data = self.cursor.fetchone()
        return user_data

    def getUserDataById(self, id):
        self.cursor.execute(
            "SELECT * "
            " FROM userss"
            " where id=:id",
            {"id": id}
        )
        user_data = self.cursor.fetchone()
        return user_data

    ##INSERT USER
    def insertUser(self,name,password):
        self.cursor.execute(
            """
            INSERT INTO userss (name, password)
            VALUES (:name,:password)
            """,
            {"name": name, "password": password}
        )

        self.conn.commit()