"""database connection and handling"""

import pymysql


class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "password"

        self.connection = pymysql.connect(host=host, user=user, password=password, cursorclass=pymysql.cursors.DictCursor)

        with self.connection.cursor() as cursor:
            try:
               cursor.execute("CREATE DATABASE scrappy")
            except Exception as error:
                print(error)

            cursor.execute("USE scrappy")

            # create table category
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS category (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255))""")

            # create table status
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS status (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255), completion INT, color VARCHAR(255))""")

            # create table prio
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS prio (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, prio INT, text VARCHAR(255), color VARCHAR(255), icon VARCHAR(255))""")

            # create table label
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS label (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255), color VARCHAR(255))""")

            # create table user_group
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_group (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))""")

            # create table company
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS company (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))""")

            # create table user
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS user (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), password VARCHAR(255), first_name VARCHAR(255), last_name VARCHAR(255), company_id INT, FOREIGN KEY (company_id) REFERENCES company(id))""")

            # create table user_in_group
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS user_in_group (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, user_id INT, group_id INT, FOREIGN KEY (user_id) REFERENCES user(id), FOREIGN KEY (group_id) REFERENCES user_group(id))""")

            # create table comment
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS comment (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, header VARCHAR(255), text VARCHAR(500), created_by INT, created_at DATETIME, FOREIGN KEY (created_by) REFERENCES user(id))""")

            # create table ticket
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS ticket (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, header VARCHAR(255), text VARCHAR(500), category_id INT, status_id INT, comment_id INT, child_ticket INT, prio_id INT, assign_to INT, created_by INT, FOREIGN KEY (category_id) REFERENCES category(id), FOREIGN KEY (status_id) REFERENCES status(id), FOREIGN KEY (comment_id) REFERENCES comment(id), FOREIGN KEY (child_ticket) REFERENCES ticket(id), FOREIGN KEY (prio_id) REFERENCES prio(id), FOREIGN KEY (assign_to) REFERENCES user(id), FOREIGN KEY (created_by) REFERENCES user(id))""")

            # create table label_in_ticket
            cursor.execute("""CREATE TABLE IF NOT EXISTS label_in_tabel_(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ticket INT, label INT, FOREIGN KEY (ticket) REFERENCES ticket(id), FOREIGN KEY (label) REFERENCES label(id))""")


            # create roles
            #cursor.execute("""INSERT INTO user_group (name) VALUES ('admin'), ('default'), ('processor')""")

            # create default category
            #cursor.execute("""INSERT INTO category (text) VALUES ('Programmierung'), ('Server'), ('Bug')""")

        self.connection.commit()

    def get_all(self, table):
        with self.connection.cursor() as cursor:
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def get_one_by_id(self, table, _id):
        with self.connection.cursor() as cursor:
            sql = f"SELECT * FROM {table} WHERE id={_id}"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
