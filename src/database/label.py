class Label:
    @staticmethod
    def insert(db, text, color):
        with db.connection.cursor() as cursor:
            sql = "INSERT INTO label(text, color) VALUES (%s, %s)"
            cursor.execute(sql, (text, color))
        db.connection.commit()

    @staticmethod
    def get_all(db):
        with db.connection.cursor() as cursor:
            sql = "SELECT * FROM label"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result