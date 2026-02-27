import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    quantity INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    member_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    FOREIGN KEY(book_id) REFERENCES books(book_id),
    FOREIGN KEY(member_id) REFERENCES members(member_id)
)
""")

conn.commit()

# Functions
def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    quantity = int(input("Enter Quantity: "))
    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (?, ?, ?)",
                   (title, author, quantity))
    conn.commit()
    print("Book added successfully!")

def view_books():
    cursor.execute("SELECT * FROM books")
    for book in cursor.fetchall():
        print(book)

def add_member():
    name = input("Enter Member Name: ")
    cursor.execute("INSERT INTO members (name) VALUES (?)", (name,))
    conn.commit()
    print("Member added successfully!")

def issue_book():
    book_id = int(input("Enter Book ID: "))
    member_id = int(input("Enter Member ID: "))
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=7)

    cursor.execute("INSERT INTO issues (book_id, member_id, issue_date, due_date, return_date) VALUES (?, ?, ?, ?, ?)",
                   (book_id, member_id, issue_date.strftime("%Y-%m-%d"),
                    due_date.strftime("%Y-%m-%d"), None))
    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id = ?", (book_id,))
    conn.commit()
    print("Book issued successfully!")

def return_book():
    issue_id = int(input("Enter Issue ID: "))
    return_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("UPDATE issues SET return_date = ? WHERE issue_id = ?", (return_date, issue_id))
    conn.commit()
    print("Book returned successfully!")

# Menu
while True:
    print("\n--- Library Management System ---")
    print("1. Add Book")
    print("2. View Books")
    print("3. Add Member")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        add_member()
    elif choice == "4":
        issue_book()
    elif choice == "5":
        return_book()
    elif choice == "6":
        break
    else:
        print("Invalid choice!")

conn.close()
