# BMBME_EQUIPMENT-COMPANY
import json
import os
import re

# File paths for customer and admin data
customer_database_file = "customer_database.txt"
admin_database_file = "admin_database.txt"


# Helper functions to load and save data
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Load customer and admin data
admin_database = load_data(admin_database_file)
customer_database = load_data(customer_database_file)


# Show customer menu
def show_customer_menu():
    print("\n--- Customer Menu ---")
    print("1. View Profile")
    print("2. Edit Profile")
    print("3. Logout")
    choice = input("Choose an option: ")
    if choice == "1":
        print("Displaying profile...")  # Add logic to display customer profile here
    elif choice == "2":
        print("Edit profile option...")  # Add logic to edit customer profile here
    elif choice == "3":
        print("Logging out...")  # Logic to log out and return to login menu
    else:
        print("Invalid choice, returning to menu...")
        show_customer_menu()


# Show admin menu
def show_admin_menu():
    print("\n--- Admin Menu ---")
    print("1. View All Customers")
    print("2. Edit Customer")
    print("3. Add Customer")
    print("4. Logout")
    choice = input("Choose an option: ")
    if choice == "1":
        print("Displaying all customers...")  # Add logic to view all customers here
    elif choice == "2":
        print("Edit customer option...")  # Add logic to edit customer details here
    elif choice == "3":
        print("Add customer option...")  # Add logic to add a new customer here
    elif choice == "4":
        print("Logging out...")  # Logic to log out and return to login menu
    else:
        print("Invalid choice, returning to menu...")
        show_admin_menu()


# Generate unique customer ID
def generate_customer_id():
    return len(customer_database) + 1  # Simple ID generation logic


# Save customer data
def save_customer_database():
    save_data(customer_database_file, customer_database)


# Validate email format
def is_valid_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None


# Validate phone number format
def is_valid_phone_number(phone_number):
    return phone_number.isdigit() and len(phone_number) == 10


# Main login function
def login():
    while True:
        do_you_want_to_register = input('Do you want to register (YES/NO/EXIT): ').strip().upper()
        if do_you_want_to_register == "EXIT":
            print("Exiting the system. Goodbye!")
            exit()  # Gracefully terminate the program

        elif do_you_want_to_register == "YES":
            print("Fill registration form")
            first_name = input("Enter your first name (this will be your username): ").strip()
            last_name = input("Enter your last name: ").strip()
            phone_number = input("Enter your phone number: ").strip()
            email_address = input("Enter your email address (this will be your password): ").strip()

            # Validate inputs
            if not first_name or not last_name or not phone_number or not email_address:
                print("\nError: Please fill in all required fields for registration!")
                continue  # Restart registration if fields are missing

            if not is_valid_email(email_address):
                print("\nError: Invalid email address format!")
                continue  # Restart registration if email is invalid

            if not is_valid_phone_number(phone_number):
                print("\nError: Invalid phone number. Must be 10 digits.")
                continue  # Restart registration if phone number is invalid

            # Check if email or username exists
            if any(c["firstname"].lower() == first_name.lower() for c in customer_database) or \
                    any(c["emailaddress"].lower() == email_address.lower() for c in customer_database):
                print("\nA user with this email address or username already exists!")
                continue  # Restart registration if user exists

            customer_id = generate_customer_id()  # Generate new customer ID
            new_customer = {
                "customerid": customer_id,
                "firstname": first_name,
                "lastname": last_name,
                "phonenumber": phone_number,
                "emailaddress": email_address
            }

            customer_database.append(new_customer)
            save_customer_database()  # Save updated customer data
            print("\nRegistration Successful! Please log in now.")
            continue  # Restart login process

        elif do_you_want_to_register == "NO":
            print("Login")
            user_type = input('Enter type ADMIN / CUSTOMER: ').strip().upper()

            # ADMIN login
            if user_type == "ADMIN":
                admin_name = input("Enter admin username: ").strip()
                admin_password = input("Enter admin password: ").strip()

                admin = next((a for a in admin_database if
                              a["firstname"].lower() == admin_name.lower() and a["emailaddress"] == admin_password),
                             None)

                if admin:
                    print(f"Welcome, Admin {admin_name}!")
                    show_admin_menu()
                else:
                    print("Invalid admin username or password. Please try again.")

            # CUSTOMER login
            elif user_type == "CUSTOMER":
                customer_name = input("Enter customer username: ").strip()
                customer_password = input("Enter customer password: ").strip()

                # Check if the customer exists in the database
                customer = next((c for c in customer_database if c["firstname"].lower() == customer_name.lower() and c[
                    "emailaddress"] == customer_password), None)

                if customer:
                    print(f"Welcome {customer['firstname']} {customer['lastname']}!")
                    show_customer_menu()
                else:
                    print("Invalid username or password. Please try again.")

            else:
                print("Unknown user type! Please enter either ADMIN or CUSTOMER.")

        else:
            print("\nInvalid input! Please answer YES or NO or EXIT.")


# Main Program
if __name__ == "__main__":
    print("Welcome to E-TEC BME System!")
    login()
