import csv
import requests
import logging

# error handling log
logging.basicConfig(
    filename='error_log.txt',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Variables
API_URL = "https://example.com/api/create_user"
REQUIRED_FIELDS = ['name', 'email', 'role']

def is_valid_user(row):
    """Check if all required fields are present"""
    return all(row.get(field) for field in REQUIRED_FIELDS)

def send_create_user_request(user_data):
    """Send the HTTP request to create the user"""
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code != 201:
            logging.error(f"failed to create user {user_data.get('email','Unknown')}: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        logging.error(f"Request exception for user {user_data.get('email','unknown')}: {str(e)}")

def create_users(file_path):
    """Create users attempt"""
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not is_valid_user(row):
                    logging.error(f"Skipping invalid row: {row}")  # Changed to ERROR level to match configuration
                    continue
                send_create_user_request(row)
    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error while processing file {file_path}: {str(e)}")


# Entry point
if __name__ == "__main__":
    create_users("users.csv")
