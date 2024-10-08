import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def register_user(email, password, username):
    logging.debug("Entered register_user function.")
    logging.info(f"Attempting to register user with email: {email}")
    
    try:
        logging.debug("Checking if email exists in the database.")
        if email_exists_in_db(email):
            logging.warning(f"Email {email} is already registered.")
            return "Email already registered."
        
        logging.debug("Inserting new user into the database.")
        insert_user_into_db(email, password, username)
        logging.info(f"User {username} successfully registered.")
        return "Registration successful."
    
    except Exception as e:
        logging.error(f"Error during registration process: {e}")
        logging.critical("Critical failure in user registration! Immediate action required.")
        return "Registration failed due to a critical error."

def email_exists_in_db(email):

    logging.debug(f"Checking database for existing email: {email}")
    return False 

def insert_user_into_db(email, password, username):

    logging.debug(f"Inserting user {username} into the database.")
    pass  