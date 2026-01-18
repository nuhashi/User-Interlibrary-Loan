import sqlite3

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, email TEXT)''')
    # Updated orders table to include more details
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (order_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, 
                       book_title TEXT, author TEXT, status TEXT)''')
    conn.commit()
    conn.close()

# --- SYSTEM LOGIC ---
class ILLSystem:
    def __init__(self):
        self.current_user = None

    def register(self):
        print("\n--- Create New Patron Account ---")
        username = input("Choose Username: ")
        password = input("Choose Password: ")
        email = input("Enter Email: ")
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                           (username, password, email))
            conn.commit()
            conn.close()
            print(f"Success! Account created for {username}.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")

    def login(self):
        print("\n--- Patron Login ---")
        username = input("Username: ")
        password = input("Password: ")
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.current_user = {"id": user[0], "name": user[1], "email": user[3]}
            return True
        print("Login failed.")
        return False

    # NEW: Function to request a book
    def request_book(self):
        print("\n--- Request a Book (Interlibrary Loan) ---")
        title = input("Book Title: ")
        author = input("Author Name: ")
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (user_id, book_title, author, status) VALUES (?, ?, ?, ?)", 
                       (self.current_user['id'], title, author, "Pending/Processing"))
        conn.commit()
        conn.close()
        print(f"Success! Your request for '{title}' has been submitted.")

    def view_orders(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, book_title, author, status FROM orders WHERE user_id=?", (self.current_user['id'],))
        orders = cursor.fetchall()
        conn.close()
        print(f"\n--- Your Loan Requests ({self.current_user['name']}) ---")
        if not orders:
            print("No requests found.")
        for o in orders:
            print(f"ID: {o[0]} | Title: {o[1]} | Author: {o[2]} | Status: {o[3]}")

    def delete_order(self):
        self.view_orders()
        order_id = input("\nEnter the Order ID to cancel/delete: ")
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        # Ensures a user can only delete their own orders
        cursor.execute("DELETE FROM orders WHERE order_id=? AND user_id=?", (order_id, self.current_user['id']))
        conn.commit()
        conn.close()
        print(f"Request {order_id} has been cancelled.")

    def update_email(self):
        new_mail = input("New email: ")
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email=? WHERE id=?", (new_mail, self.current_user['id']))
        conn.commit()
        conn.close()
        print("Email updated!")

# --- MAIN LOOP ---
def main():
    init_db()
    system = ILLSystem()
    
    while True:
        print("\n==============================")
        print("   INTERLIBRARY LOAN SYSTEM   ")
        print("==============================")
        print("1. Login")
        print("2. Register (New Patron)")
        print("3. Exit")
        choice = input("\nSelect Option: ")

        if choice == '1':
            if system.login():
                while True:
                    print(f"\n--- Welcome, {system.current_user['name']} ---")
                    print("1. Request a Book")
                    print("2. View/Check Status")
                    print("3. Delete/Cancel Request")
                    print("4. Update Email")
                    print("5. Logout")
                    sub_choice = input("Select: ")
                    
                    if sub_choice == '1': system.request_book()
                    elif sub_choice == '2': system.view_orders()
                    elif sub_choice == '3': system.delete_order()
                    elif sub_choice == '4': system.update_email()
                    elif sub_choice == '5': break
        elif choice == '2':
            system.register()
        elif choice == '3':
            break

if __name__ == "__main__":
    main()