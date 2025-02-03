#CUSTOMER MENU

import json
import os
import datetime

# File paths for customer and view database
customer_database = "customer_database.txt"
view_database = "view_database.txt"
repair_requests_database = "repair_request_database.txt"

# Helper functions to load and save data
def load_data(filename):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return []
    with open(filename, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved successfully to {filename}.")

# Load data
customers = load_data(customer_database)
items = load_data(view_database)
repair_requests = load_data(repair_requests_database)

# Function to ensure customer has a unique ID
def ensure_customer_id(customer):
    if "customerid" not in customer:
        customer["customerid"] = f"id{len(customers) + 1:03d}"  # Use 'id' instead of 'cust'
        customers.append(customer)
        save_data(customer_database, customers)

# Generate invoice
def generate_invoice(customer, item, quantity, total_price):
    if not all(key in customer for key in ["firstname", "lastname", "emailaddress", "phonenumber", "customerid"]):
        print("Incomplete customer data. Cannot generate invoice.")
        return

    # Get current date for the invoice
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    invoice_details = f"""
    --- Invoice ---
    Date: {current_date}
    Customer: {customer['firstname']} {customer['lastname']}
    Email: {customer['emailaddress']}
    Phone: {customer['phonenumber']}

    Item Purchased:
    ID: {item['item_id']}
    Name: {item['name']}
    Quantity: {quantity}
    Price per Unit: {item['price']}
    Total Price: {total_price}

    Thank you for your purchase!

    E-TEC BME System
    """

    # Save the invoice as a .txt file with a unique name
    invoice_filename = f"invoice_{customer['customerid']}_{current_date.replace(':', '-').replace(' ', '_')}.txt"
    with open(invoice_filename, "w") as invoice_file:
        invoice_file.write(invoice_details)
    print("\nInvoice generated successfully!")
    print(f"Invoice saved as {invoice_filename}")

# Function to display customer menu
def customer_menu(customer):
    while True:
        print("\n--- Customer Menu ---")
        print("1. View Profile")
        print("2. Update Details")
        print("3. Purchase Equipment")
        print("4. Submit Repair Request")
        print("5. View Repair Status")
        print("6. Log Out")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            print("\n--- Your Profile ---")
            print(f"First Name: {customer['firstname']}")
            print(f"Last Name: {customer['lastname']}")
            print(f"Phone Number: {customer['phonenumber']}")
            print(f"Email Address: {customer['emailaddress']}")
        elif choice == "2":
            print("\n--- Update Details ---")
            customer['phonenumber'] = input("Enter new phone number: ").strip()
            customer['emailaddress'] = input("Enter new email address: ").strip()
            save_data(customer_database, customers)
            print("Details updated successfully!")
        elif choice == "3":
            print("\n--- Purchase Equipment ---")
            keyword = input("Enter a keyword to search for equipment: ").strip().lower()
            matching_items = [item for item in items if keyword in item['name'].lower()]

            if not matching_items:
                print("No matching equipment found.")
                continue
            for item in matching_items:
                print(f"ID: {item['item_id']}, Name: {item['name']}, Price: {item['price']}, Stock: {item['stock']}")

                item_id = input("Enter the ID of the item you want to purchase: ").strip()
                selected_item = next((item for item in items if item['item_id'] == item_id), None)

                if selected_item:
                    if int(selected_item['stock']) > 0:
                        print(f"Item '{selected_item['name']}' is available.")
                        quantity = int(input(f"How many units of '{selected_item['name']}' would you like to purchase? ").strip())

                        if quantity > 0 and quantity <= int(selected_item['stock']):
                            print(f"Purchasing {quantity} units of '{selected_item['name']}'.")
                            selected_item['stock'] = str(int(selected_item['stock']) - quantity)  # Decrease stock
                            print(f"Purchase successful! {quantity} unit(s) purchased.")

                            # Confirming the purchase
                            confirm_payment = input("Do you want to confirm payment? (YES/NO): ").strip().upper()
                            if confirm_payment == "YES":
                                card_number = input("Enter your card number:").strip()
                                if card_number.isdigit() and len(card_number) == 16:  # Simple validation
                                  total_price = selected_item['price'] * quantity
                                  print(f"Total Price: {total_price}")
                                  print(f"Payment of {total_price} confirmed. Thank you for your purchase!")

                                  # Generate and save invoice
                                  generate_invoice(customer, selected_item, quantity, total_price)
                                else:
                                  print("Invalid card number. Please try again.")
                            else:
                                print("Payment not successful")
                        else:
                            print("Invalid quantity. Either it's out of stock or the quantity is too high.")
                    else:
                        print("Sorry, this item is out of stock.")
                else:
                    print("Invalid item ID.")
        elif choice == "4":
                item_id = input("Enter the ID of the equipment for repair: ").strip()
                selected_item = next((item for item in items if item["item_id"] == item_id), None)
                if not selected_item:
                    print("Invalid item ID.")
                    continue

                issue = input("Describe the issue: ").strip()

                # Add pickup time input or calculation
                pickup_time = input("Enter your preferred pickup time (e.g., 2024-12-15 10:00 AM): ").strip()

                repair_request = {
                    "repair_id": f"rep{len(repair_requests) + 1:03d}",
                    "customer_id": customer["customerid"],
                    "item_id": item_id,
                    "issue_description": issue,
                    "status": "Pending",
                    "repair_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "pickup_time": pickup_time
                }
                repair_requests.append(repair_request)
                save_data(repair_requests_database, repair_requests)
                print("Repair Requests List:", repair_requests)
                print("Repair request submitted.")

        elif choice == "5":
            print("\n--- View Repair Status ---")

            print(repair_requests)
            customer_requests = [req for req in repair_requests if req["customerid"] == customer["customerid"]]
            print(f"Found customer requests: {customer_requests}")
            if customer_requests:
                print("\n--- Your Repair Requests ---")
                for req in customer_requests:
                    item = next((item for item in items if item["item_id"] == req["item_id"]), None)
                    print(f"Repair ID: {req['repair_id']}")
                    print(f"Equipment: {item['name'] if item else 'Unknown'}")
                    print(f"Issue: {req['issue_description']}")
                    print(f"Status: {req['status']}")
                    print(f"Repair Date: {req['repair_date']}")

                    # If repair is completed, provide pickup info and the pickup date
                    if req['status'] == 'Completed':
                        print(f"Pickup Date: {req['pickup_date']}")
                        print("Pickup Information: Please pick up your equipment at the main office.")

                    print("-" * 30)
            else:
                print("You have no repair requests.")

        elif choice == "6":
            print("Logging out. Returning to login page...")
            exit_choice = input("Do you want to exit from the system? (YES/NO): ").strip().upper()
            if exit_choice == "YES":
                print("Exiting the system. Thank you!")
                break
            else:
                print("Returning to customer menu...")
                continue

# Customer Login Function
def login():
    while True:
        print("Welcome to the E-TEC BME System!")
        user_type = input("Enter user type (ADMIN / CUSTOMER): ").strip().upper()
        if user_type == "CUSTOMER":
            customer_name = input("Enter customer firstname: ").strip()
            customer_password = input("Enter customer email address: ").strip()
            customer = next(
                (c for c in customers if c["firstname"].strip().lower() == customer_name.strip().lower() and
                 c["emailaddress"].strip().lower() == customer_password.strip().lower()), None)
            if customer:
                print(f"Welcome, {customer_name}!")
                ensure_customer_id(customer)
                customer_menu(customer)
                print(f"Logged in as: {customer['firstname']} {customer['lastname']}, Customer ID: {customer['customerid']}")

            else:
                print("Invalid credentials.")
        elif user_type == "ADMIN":
            print("Admin login is not implemented in this example.")
        else:
            print("Invalid user type.")
        exit_choice = input("Do you want to exit? (YES/NO): ").strip().upper()
        if exit_choice == "YES":
            print("Exiting the system.")
            break

if __name__ == "__main__":
    print("Welcome to E-TEC BME System!")
    login()
