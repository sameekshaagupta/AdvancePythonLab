import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def send_message(sender_id, receiver_id, message_content):
    logging.debug("Entered send_message function.")
    logging.info(f"User {sender_id} is attempting to send a message to {receiver_id}")
    
    try:
        if not message_content:
            logging.warning("Empty message content detected.")
            return "Cannot send an empty message."
        
        logging.debug(f"Message content: {message_content}")
        logging.debug("Inserting message into the database.")
        insert_message_into_db(sender_id, receiver_id, message_content)
        
        logging.info(f"Message from {sender_id} to {receiver_id} sent successfully.")
        return "Message sent."
    
    except Exception as e:
        logging.error(f"Failed to send message from {sender_id} to {receiver_id}: {e}")
        logging.critical("Critical error during message sending operation!")
        return "Message sending failed due to a critical error."

def insert_message_into_db(sender_id, receiver_id, message_content):

    logging.debug(f"Inserting message from {sender_id} to {receiver_id} into the database.")
    pass  
