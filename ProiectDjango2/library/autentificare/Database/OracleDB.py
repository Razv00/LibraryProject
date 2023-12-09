import cx_Oracle

from ..Database.Books import Books
from ..Database.Users import Users


class OracleDB:

    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = cx_Oracle.connect('razvan/parola@//localhost:1521/orcl')
            self.cursor = self.conn.cursor()
            print("Oracle initializat cu succes")
        except cx_Oracle.DatabaseError as e:
            print("There is a problem with Oracle", e)

        self.books = Books(self.conn, self.cursor)
        self.users = Users(self.conn, self.cursor)

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = OracleDB()
    try:
        # db.createBooksTrigger()
        # db.addUniqueConstraint()
        # db.insertDataIntoBooksTable("ana123", "autor", "mere")
        # db.insertDataIntoBooksTable("ana221412", "autor", "mere")
        # db.insertDataIntoBooksTable("ana2332", "autor", "mere")
        # print(db.getBooksByTitle("ana123"))
        # print(db.getBooksByEditura("mere"))
        # print(db.getBooksByAuthor("autor"))
        # print(db.getBooksById(1))
        db.books.addForeignKeyConstraintAndUserIdColumn()

        db.books.insertDataIntoBooksTable("Book 3", "Author 3", "Publisher 3",
                                    user_id=1)  # Assuming user_id 100 doesn't exist
        db.users.getUserDataByName("razvan")
    finally:
        db.closeConnection()
        # db.insertDataIntoBooksTable("1","2","3")
