import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

def send_message(sender_id, receiver_id, message_content):
    logging.info(f"User {sender_id} sending message to {receiver_id}")
    
    try:
        if not message_content:
            logging.warning("Empty message content.")
            return "Cannot send an empty message."
        
        # Simulate message insertion into the database
        insert_message_into_db(sender_id, receiver_id, message_content)
        logging.info(f"Message from {sender_id} to {receiver_id} sent successfully.")
        return "Message sent."

    except Exception as e:
        logging.error(f"Failed to send message from {sender_id} to {receiver_id}: {e}")
        return "Message sending failed due to an error."

def insert_message_into_db(sender_id, receiver_id, message_content):
    # Simulated function for message insertion
    pass