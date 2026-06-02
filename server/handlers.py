import json
import secrets
import logging
from datetime import datetime
from database import Database
from client_manager import ClientManager, send_json
import utils

logger = logging.getLogger(__name__)

# Shared database and client manager instances
db = Database()
client_manager = ClientManager()

def deliver_pending_messages(email, client_socket):
    """
    Fetches and delivers undelivered messages to a newly logged-in user.
    """
    try:
        pending_messages = db.get_undelivered_messages(email)
        for msg in pending_messages:
            # msg is (id, sender_email, content)
            send_json(client_socket, {
                'status': 'message', 
                'from': msg[1], 
                'content': msg[2], 
                'time': str(datetime.now())
            })
        if pending_messages:
            db.mark_message_as_delivered(email)
    except Exception as e:
        logger.exception(f"Error delivering pending messages to {email}: {e}")

def handle_registration(client_socket, payload):
    """
    Handles account registration and verifies registration OTP.
    """
    email = payload['email']
    otp = payload.get('otp')
    password = payload['password']
    name = payload['name']
    
    is_valid, error_msg = utils.validate_email(email)
    if not is_valid:
        send_json(client_socket, {'status': 'error', 'action': 'register', 'message': error_msg})
        return

    if not otp:
        send_json(client_socket, {'status': 'error', 'action': 'register', 'message': 'OTP is required.'})
        return

    if not db.verify_otp(email, otp):
        send_json(client_socket, {'status': 'error', 'action': 'register', 'message': 'OTP mismatched or expired.'})
        return

    db.delete_otp(email)
    success = db.register_user(email, password, name)
    if success:
        send_json(client_socket, {'status': 'ok', 'action': 'register', 'message': 'Registration successful'})
    else:
        send_json(client_socket, {'status': 'error', 'action': 'register', 'message': 'Email already exists'})

def handle_login(client_socket, payload):
    """
    Handles user authentication. On success, adds user connection to ClientManager.
    """
    email = payload['email']
    password = payload['password']
    
    client_details = db.get_user(email)
    if not client_details:
        send_json(client_socket, {'status': 'error', 'action': 'login', 'message': 'User not found'})
        return None
        
    if not db.verify_password(password, client_details[1]):   
        send_json(client_socket, {'status': 'error', 'action': 'login', 'message': 'Wrong password'})
        return None
    
    client_manager.add_client(email, client_socket, client_details[2])
    send_json(client_socket, {
        'status': 'ok', 
        'action': 'login', 
        'message': 'Login successfully', 
        'name': client_details[2], 
        'email': email
    })
    return email

def handle_forgot_password(client_socket, payload):
    """
    Generates a password reset OTP and emails it to the user.
    """
    email = payload['email']
    is_valid, error_msg = utils.validate_email(email)
    if not is_valid:
        send_json(client_socket, {'status': 'error', 'action': 'forgot_password', 'message': error_msg})
        return
        
    otp = f"{secrets.randbelow(1000000):06d}"
    if db.save_otp(email, otp):
        subject = "Password Reset OTP"
        body_template = "Your password reset OTP is {otp}"
        if utils.send_otp_email(email, otp, subject, body_template):
            send_json(client_socket, {'status': 'ok', 'action': 'forgot_password', 'message': 'OTP sent'})
        else:
            logger.warning(f"Email delivery failed. Fallback OTP for {email}: {otp}")
            send_json(client_socket, {
                'status': 'ok', 
                'action': 'forgot_password', 
                'message': 'Email delivery failed. Fallback OTP generated.'
            })
    else:
        send_json(client_socket, {'status': 'error', 'action': 'forgot_password', 'message': 'Failed to generate OTP'})

def handle_verify_otp(client_socket, payload):
    """
    Verifies user-submitted forgot-password OTP.
    """
    email = payload['email']
    otp = payload['otp']
    if db.verify_otp(email, otp):
        db.delete_otp(email)
        send_json(client_socket, {'status': 'ok', 'action': 'verify_otp', 'message': 'OTP matched'})
    else:
        send_json(client_socket, {'status': 'error', 'action': 'verify_otp', 'message': 'OTP mismatched or expired'})

def handle_reset_password(client_socket, payload):
    """
    Updates user password after successful verification.
    """
    email = payload['email']
    password = payload['new_password']
    if db.update_password(email, password):
        send_json(client_socket, {'status': 'ok', 'action': 'reset_password', 'message': 'Password updated successfully'})
    else:
        send_json(client_socket, {'status': 'error', 'action': 'reset_password', 'message': 'Failed to update password'})

def handle_register_send_otp(client_socket, payload):
    """
    Generates and emails an OTP for account registration.
    """
    email = payload['email']
    is_valid, error_msg = utils.validate_email(email)
    if not is_valid:
        send_json(client_socket, {'status': 'error', 'action': 'register_send_otp', 'message': error_msg})
        return
    
    if db.get_user(email):
        send_json(client_socket, {'status': 'error', 'action': 'register_send_otp', 'message': 'Email already exists.'})
        return

    otp = f"{secrets.randbelow(1000000):06d}"
    if db.save_otp(email, otp):
        subject = "Account Registration OTP"
        body_template = "Your account registration OTP is {otp}"
        if utils.send_otp_email(email, otp, subject, body_template):
            send_json(client_socket, {'status': 'ok', 'action': 'register_send_otp', 'message': 'OTP sent successfully.'})
        else:
            logger.warning(f"Email delivery failed. Fallback OTP for {email}: {otp}")
            send_json(client_socket, {
                'status': 'ok', 
                'action': 'register_send_otp', 
                'message': 'Email delivery failed. Fallback OTP generated.'
            })
    else:
        send_json(client_socket, {'status': 'error', 'action': 'register_send_otp', 'message': 'Failed to generate OTP.'})

def handle_find_user(client_socket, payload):
    """
    Searches for a user by email and reports their current online status.
    """
    email = payload['email']
    client_details = db.get_user(email)
    if client_details:
        is_online = client_manager.get_receiver_socket(email) is not None
        send_json(client_socket, {
            'status': 'ok', 
            'action': 'find_user', 
            'email': email, 
            'name': client_details[2], 
            'online': is_online
        })
    else:
        send_json(client_socket, {"status": "error", "action": "find_user", "message": "User not found"})

def route_message(sender_email, payload):
    """
    Routes a direct private message to a specific recipient and saves it.
    """
    recipient_email = payload['to']
    message = payload['content']   
    db.save_message(sender_email, recipient_email, message)
    receiver_socket = client_manager.get_receiver_socket(recipient_email)
    if receiver_socket:
        try:
            send_json(receiver_socket, {
                'status': 'message', 
                'from': sender_email, 
                'content': message, 
                'time': str(datetime.now())
            })
            db.mark_message_as_delivered(recipient_email)
        except Exception as e:
            logger.exception(f"Error routing message to {recipient_email}: {e}")

def handle_broadcast(sender_email, payload):
    """
    Broadcasts a message to all online client connections except the sender.
    """
    content = payload['content']
    sockets_to_send = client_manager.get_sockets_except(sender_email)
    
    broadcast_data = {
        'status': 'broadcast',
        'from': sender_email,
        'content': content,
        'time': str(datetime.now())
    }
    for client_socket in sockets_to_send:
        try:
            send_json(client_socket, broadcast_data)
        except Exception as e:
            logger.exception(f"Error sending broadcast from {sender_email}: {e}")

def handle_client(client_socket):
    """
    Thread loop managing client authentication, request routing, and connection teardown.
    """
    email = None
    reader = None
    try:
        reader = client_socket.makefile('r', encoding='utf-8')
        
        # Authentication loop
        while not email:
            line = reader.readline()
            if not line:
                return
            try:
                payload = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            action = payload.get('action')
            if action == "register":
                handle_registration(client_socket, payload)
            elif action == "register_send_otp":
                handle_register_send_otp(client_socket, payload)
            elif action == "login":
                email = handle_login(client_socket, payload)
            elif action == "forgot_password":
                handle_forgot_password(client_socket, payload)
            elif action == "verify_otp":
                handle_verify_otp(client_socket, payload)
            elif action == "reset_password":
                handle_reset_password(client_socket, payload)
            else:
                send_json(client_socket, {'status': 'error', 'message': "Please login or register first"})

        # Authenticated command loop
        deliver_pending_messages(email, client_socket)
        
        while True:
            line = reader.readline()
            if not line:
                break
            try:
                payload = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            action = payload.get('action')
            if action == 'logout':
                break
            elif action == 'message':
                route_message(email, payload)
            elif action == 'broadcast':
                handle_broadcast(email, payload)
            elif action == 'get_online_users':
                online_list = client_manager.get_online_users()
                send_json(client_socket, {'status': 'online_users', 'users': online_list})
            elif action == 'find_user':
                handle_find_user(client_socket, payload)
            elif action == 'get_chat_history':
                partner = payload.get('partner')
                history = db.get_chat_history(email, partner)
                send_json(client_socket, {'status': 'chat_history', 'partner': partner, 'history': history})
            elif action == 'get_recent_chats':
                chats = db.get_recent_chats(email)
                send_json(client_socket, {'status': 'recent_chats', 'chats': chats})
            else:
                send_json(client_socket, {'status': 'error', 'message': "Unknown action"})

    except Exception as e:
        logger.exception(f"Error managing client connection for {email}: {e}")
    finally:
        if email:
            client_manager.remove_client(email, client_socket)
        else:
            logger.info("Unauthenticated client disconnected.")
        try:
            client_socket.close()
        except:
            pass
