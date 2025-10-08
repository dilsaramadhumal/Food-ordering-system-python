import utils.session
import sqlite3
import hashlib

# Database setup
conn = sqlite3.connect('food_ordering.db')
c = conn.cursor()

# Create tables

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS restaurants (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY,
                restaurant_id INTEGER,
                name TEXT,
                price REAL,
                FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                item_id INTEGER,
                quantity INTEGER,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (item_id) REFERENCES menu_items(id)
            )''')


# Passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Functions
def register():
    username = input("Enter username: ")
    password = hash_password(input("Enter password: "))
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Registration successful!")

def login():
    username = input("Enter username: ")
    password = hash_password(input("Enter password: "))
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    
    if user:
        print("Login successful! Welcome,", user[1])
    else:
        print("Invalid username or password.")


# Main menu
def main_menu():
    print("Welcome to my Food Ordering System!")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    choice = input("Please enter your choice: ")
    if choice == '1':
        login()
    elif choice == '2':
        register()
    elif choice == '3':
        print("Goodbye!")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main_menu()


# Function to browse menu of a selected restaurant
def browse_menu(restaurant_id):
    c.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,))
    restaurant = c.fetchone()
    print(f"\nMenu for {restaurant[1]}:")
    c.execute("SELECT * FROM menu_items WHERE restaurant_id=?", (restaurant_id,))
    menu_items = c.fetchall()
    for item in menu_items:
        print(f"{item[0]}. {item[2]} - ${item[3]}")
    item_choice = input("Please enter the number of the item you'd like to add to your cart (or 0 to go back): ")
    if item_choice == '0':
        main_menu()
    else:
        quantity = int(input("Quantity: "))
        add_to_cart(int(item_choice), quantity)

#----------------------------------------------------------------------------------------------------------------------

def browse_restaurants():
    c.execute("SELECT * FROM restaurants")
    restaurants = c.fetchall()
    print("Available Restaurants:")
    for restaurant in restaurants:
        print(f"{restaurant[0]}. {restaurant[1]}")
    restaurant_choice = input("Please enter the number of the restaurant you'd like to browse: ")
    browse_menu(int(restaurant_choice))

#-----------------------------------------------------------------------------------------------------------------------


# Function to add items to the cart
def add_to_cart(item_id, quantity):
    c.execute("SELECT * FROM menu_items WHERE id=?", (item_id,))
    item = c.fetchone()
    print(f"{item[2]} added to cart.")
    cart.append((item[2], item[3], quantity))
    view_cart()

# Function to view the cart
def view_cart():
    print("\nYour Cart:")
    total = 0
    for i, item in enumerate(cart, start=1):
        total += item[1] * item[2]
        print(f"{i}. {item[0]} - ${item[1]} x {item[2]}")
    print(f"\nTotal: ${total}")
    cart_menu()

# Function to display cart menu
def cart_menu():
    print("\n1. Checkout")
    print("2. Remove Item")
    print("3. Back to Menu")
    choice = input("Please enter your choice: ")
    if choice == '1':
        checkout()
    elif choice == '2':
        remove_item()
    elif choice == '3':
        main_menu()
    else:
        print("Invalid choice.")
        cart_menu()

# Function to remove item from the cart
def remove_item():
    view_cart()
    item_to_remove = int(input("Enter the number of the item you want to remove: ")) - 1
    if 0 <= item_to_remove < len(cart):
        del cart[item_to_remove]
        print("Item removed from cart.")
        view_cart()
    else:
        print("Invalid item number.")
        remove_item()

# Function to place the order
def checkout():
    total = sum(item[1] * item[2] for item in cart)
    print(f"Order placed successfully! Your total is ${total}.")
    cart.clear()
    main_menu()

# Define the cart as a global list
cart = []

# Update main menu function
def main_menu():
    print("\n1. Browse Restaurants")
    print("2. View Cart")
    print("3. Logout")
    choice = input("Please enter your choice: ")
    if choice == '1':
        browse_restaurants()
    elif choice == '2':
        view_cart()
    elif choice == '3':
        print("Logged out successfully. Goodbye!")
    else:
        print("Invalid choice.")
        main_menu()

# Modify the if __name__ == "__main__" block
if __name__ == "__main__":
    main_menu()