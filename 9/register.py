import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def register_user(email,password,username):
    logging.info(f'Attempting to register user with {email}')

    try:
        if email_already_exists_in_db(email):
            logging.warning(f"Email {email} already registered")
            return "Email alreaddy registered."
        insert_user_into_db(email,password,username)
        logging.info(f"User {username} successfully registered.")
        return "Registration successful"
    except Exception as e:
        logging.error(f"Error occured during registration: {e}")
        return "Registration failed due to an error."
    
def email_already_exists_in_db(email):
    # code for checking
    return False
def insert_user_into_db(email,password,username):
    pass