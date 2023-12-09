import cx_Oracle


class Books:
    def __init__(self,conn,cursor):
        self.conn = conn
        self.cursor = cursor

    def createTableBooks(self):
        self.cursor.execute(
            """
            CREATE TABLE books(
                id integer PRIMARY KEY,
                titlu VARCHAR(100) UNIQUE NOT NULL,
                autor VARCHAR(100) NOT NULL,
                editura VARCHAR(100)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE SEQUENCE books_seq
                START WITH 1
                INCREMENT BY 1
                NOMAXVALUE
                NOCACHE
            """
        )

    def addUniqueConstraint(self):
        try:
            self.cursor.execute(
                """
                ALTER TABLE books
                ADD CONSTRAINT unq_titlu UNIQUE (titlu)
                """
            )
            self.conn.commit()
            print("Contrangere adaugata cu succes")
        except cx_Oracle.DatabaseError as e:
            print("Eroare la adaugarea constrangerii unique: ", e)

    def createBooksTrigger(self):
        self.cursor.execute(
            """
            CREATE OR REPLACE TRIGGER books_trigger
                BEFORE INSERT ON books
                FOR EACH ROW
            BEGIN
                :new.id := books_seq.NEXTVAL;
            END;
            """
        )

    def insertDataIntoBooksTable(self, titlu, autor, editura,user_id):
        try:
            if user_id is not None:
                self.cursor.execute(
                    """
                    INSERT INTO books(titlu,autor,editura,user_id)
                    VALUES (:titlu, :autor, :editura,:user_id)
                    """,
                    {"titlu": titlu, "autor": autor, "editura": editura, "user_id": user_id}
                )
            else:
                self.cursor.execute(
                    """
                    INSERT INTO books(titlu, autor, editura)
                    VALUES (:titlu, :autor, :editura)
                    """,
                    {"titlu": titlu, "autor": autor, "editura": editura}
                )

            self.conn.commit()
            print("Books inserted succesfully")
        except cx_Oracle.DatabaseError as e:
            print("Error while inserting books : ",e)

    def getBooksById(self, id):
        self.cursor.execute(
            """
            SELECT * FROM BOOKS WHERE id=:id
            """
            , {"id": id}
        )
        books_data = self.cursor.fetchone()
        return books_data

    def getBooksByTitle(self, titlu):
        self.cursor.execute(
            """
            SELECT * FROM BOOKS WHERE titlu=:titlu
            """
            , {"titlu": titlu}
        )
        books_data = self.cursor.fetchone()
        return books_data

    def getBooksByAuthor(self, autor):
        self.cursor.execute(
            """
            SELECT * FROM BOOKS WHERE autor=:autor
            """
            , {"autor": autor}
        )
        books_data = self.cursor.fetchall()
        return books_data

    def getBooksByEditura(self, editura):
        self.cursor.execute(
            """
            SELECT * FROM BOOKS WHERE editura=:editura
            """
            , {"editura": editura}
        )
        books_data = self.cursor.fetchall()
        return books_data

    def deleteBooksTable(self):
        self.cursor.execute(
            """
            drop table books
            """
        )
        self.conn.commit()

    def addForeignKeyConstraintAndUserIdColumn(self):
        try:
            self.cursor.execute(
                """
                ALTER TABLE books
                ADD user_id integer
                """
            )

            # Add foreign key constraint to the newly added user_id column
            self.cursor.execute(
                """
                ALTER TABLE books
                ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES userss(id)
                """
            )
            print("Foreign key constraint added successfully!")
        except cx_Oracle.DatabaseError as e:
            print("Error adding foreign key constraint:", e)