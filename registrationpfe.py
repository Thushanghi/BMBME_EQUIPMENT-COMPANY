
import json
import os
import re  # Import the regular expressions module for email validation

FILE_PATH = "customer_database.txt"

# Load customer database from file
def load_customer_database():
    """Load customer database from a file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            try:
                data = file.read().strip()  # Read and strip any unnecessary whitespace
                return json.loads(data) if data else []  # Return an empty list if the file is empty
            except json.JSONDecodeError:
                print("Error: File is not in valid JSON format. Initializing with an empty database.")
                return []
    return []

# Save customer database to file
def save_customer_database(user_database):
    """Save the customer database to a file."""
    with open(FILE_PATH, "w") as file:
        json.dump(user_database, file, indent=4)

# Generate a new unique customer ID
def generate_customer_id(customer_database):
    """Generate a new unique customer ID based on the current records."""
    if customer_database:
        last_customer = customer_database[-1]
        last_id = last_customer["customerid"]
        # Extract numeric part of the customer ID and increment by 1
        new_id = "id" + str(int(last_id[2:]) + 1).zfill(3)
    else:
        new_id = "id001"
    return new_id

# Add email validation function
def is_valid_email(email):
    """Validate email format."""
    # Basic regex pattern for a valid email address
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_pattern, email) is not None

# Validate phone number format (added function)
def is_valid_phone_number(phone_number):
    """Check if the phone number is valid (10 digits long)."""
    return phone_number.isdigit() and len(phone_number) == 10

# Main Program
def main():
    customer_database = load_customer_database()
    print(f"Loaded Customer Database: {customer_database}")
    already_a_member = input("Are you already a member? (YES/NO): ").strip().upper()

    if already_a_member == "YES":
        first_name = input("Enter your username: ").strip()
        email_address = input("Enter your password: ").strip()

        user_found = False  # Initialize flag for user existence
        for customer in customer_database:
            # Check if the username and email match an existing user
            if customer.get("firstname").lower() == first_name.lower() and customer.get("emailaddress").lower() == email_address.lower():
                print("\nWelcome back! Here are your details:")
                print(f"Customer ID: {customer['customerid']}")
                print(f"Name: {customer['firstname']} {customer['lastname']}")
                print(f"Phone Number: {customer['phonenumber']}")
                print(f"Email Address: {customer['emailaddress']}")
                user_found = True
                break

        if not user_found:
            print("\nInvalid username or password. Please try again!")

    elif already_a_member == "NO":
        # Register a new user
        print("\nPlease register first!")
        first_name = input("Enter your first name (this will be your username): ").strip()
        last_name = input("Enter your last name: ").strip()
        phone_number = input("Enter your phone number: ").strip()
        email_address = input("Enter your email address (this will be your password): ").strip()

        # Check for missing fields
        if not first_name or not last_name or not phone_number or not email_address:
            print("\nError: Please fill in all required fields for registration!")
            return  # Exit the registration process if validation fails

        # Validate email address format
        if not is_valid_email(email_address):
            print("\nError: Invalid email address format! Please try again.")
            return  # Exit the registration process if email validation fails

        #Validate phone number format
        if not is_valid_phone_number(phone_number):
            print("\nError: Invalid phone number. Please provide a valid phone number with 10 digits.")
            return  # Exit the registration process if phone number validation fails

        # Check if the username or email address already exists in the database
        username_exists = any(customer.get("firstname").lower() == first_name.lower() for customer in customer_database)
        emailaddress_exists = any( customer.get("emailaddress").lower() == email_address.lower() for customer in customer_database)

        if username_exists:
            print("\nA user with this email address already exists! Please try logging in.")
        elif emailaddress_exists:
            print(f"\nA user with this email address '{email_address}' already exists! Please try logging in.")
        else:
            # Add the new user to the database
            customer_id = generate_customer_id(customer_database)
            new_customer = {
                "customerid": customer_id,
                "firstname": first_name,  # First name as username
                "lastname": last_name,
                "phonenumber": phone_number,
                "emailaddress": email_address  # Email as password
            }
            customer_database.append(new_customer)
            save_customer_database(customer_database)

            print("\nRegistration Successful! Here are your details:")
            print(f"Customer ID: {customer_id}")
            print(f"Name: {first_name} {last_name}")
            print(f"Phone Number: {phone_number}")
            print(f"Email Address: {email_address}")

    else:
        print("\nInvalid input! Please answer YES or NO.")

# Run the program
if __name__ == "__main__":
    main()
