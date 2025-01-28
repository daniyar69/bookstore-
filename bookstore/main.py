import sqlite3

class Bookstore:
    def __init__(self, db_name="bookstore.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author VARCHAR(255) NOT NULL,
                year DATE NOT NULL,
                genre TEXT NOT NULL,
                price REAL NOT NULL,
                amount INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def add_book(self, title, author, year, genre, price, amount):
        self.cursor.execute('''
            INSERT INTO books (title, author, year, genre, price, amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, author, year, genre, price, amount))
        self.connection.commit()

    def delete_book(self, book_id):
        self.cursor.execute('''
            DELETE FROM books WHERE id = ?
        ''', (book_id,))
        self.connection.commit()

    def update_book(self, book_id, **kwargs):
        for key, value in kwargs.items():
            self.cursor.execute(f'''
                UPDATE books SET {key} = ? WHERE id = ?
            ''', (value, book_id))
        self.connection.commit()

    def search_books(self, **criteria):
        query = "SELECT * FROM books WHERE " + " AND ".join([f"{key} LIKE ?" for key in criteria.keys()])
        values = [f"%{value}%" for value in criteria.values()]
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def get_book(self, book_id):
        self.cursor.execute('''SELECT * FROM books WHERE id = ?''', (book_id,))
        return self.cursor.fetchone()

    def get_all_books(self):
        self.cursor.execute('''SELECT * FROM books''')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

class Person:
    def __init__(self, bookstore):
        self.bookstore = bookstore

    def search_books(self, **criteria):
        return self.bookstore.search_books(**criteria)

    def buy_book(self, book_id):
        book = self.bookstore.get_book(book_id)
        if book:
            if book[-1] > 0:  # Проверяем количество книг
                self.bookstore.update_book(book_id, amount=book[-1] - 1)
                print(f"Вы купили книгу: {book[1]}.")
            else:
                print("Эта книга закончилась.")
        else:
            print("Книга не найдена.")

def menu():
    bookstore = Bookstore()
    person = Person(bookstore)

    while True:
        try:
            print("\n--- Меню ---")
            print("1. Добавить книгу (администратор)")
            print("2. Удалить книгу (администратор)")
            print("3. Обновить данные книги (администратор)")
            print("4. Поиск книги")
            print("5. Купить книгу")
            print("6. Показать все книги")
            print("7. Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                title = input("Название: ")
                author = input("Автор: ")
                year = input("Год выпуска (YYYY-MM-DD): ")
                genre = input("Жанр: ")
                price = float(input("Цена: "))
                amount = int(input("Количество: "))
                bookstore.add_book(title, author, year, genre, price, amount)
                print("Книга добавлена.")

            elif choice == "2":
                book_id = int(input("ID книги: "))
                bookstore.delete_book(book_id)
                print("Книга удалена.")

            elif choice == "3":
                book_id = int(input("ID книги: "))
                field = input("Поле для обновления (title, author, year, genre, price, amount): ")
                value = input("Новое значение: ")
                bookstore.update_book(book_id, **{field: value})
                print("Книга обновлена.")

            elif choice == "4":
                criteria = {}
                title = input("Название (оставьте пустым, если не нужно): ")
                if title:
                    criteria['title'] = title
                author = input("Автор (оставьте пустым, если не нужно): ")
                if author:
                    criteria['author'] = author
                year = input("Год выпуска (оставьте пустым, если не нужно): ")
                if year:
                    criteria['year'] = year
                genre = input("Жанр (оставьте пустым, если не нужно): ")
                if genre:
                    criteria['genre'] = genre

                books = person.search_books(**criteria)
                if books:
                    for book in books:
                        print(book)
                else:
                    print("Книги не найдены.")

            elif choice == "5":
                book_id = int(input("ID книги: "))
                person.buy_book(book_id)

            elif choice == "6":
                books = bookstore.get_all_books()
                if books:
                    for book in books:
                        print(book)
                else:
                    print("Книг пока нет в базе данных.")

            elif choice == "7":
                print("Выход из программы.")
                bookstore.close()
                break

            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}. Попробуйте снова.")

if __name__ == "__main__":
    menu()
