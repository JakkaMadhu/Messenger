import threading
from datetime import datetime, timedelta
import bcrypt
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import MONGODB_URI

class Database:
    """
    Database access object providing operations for users, direct messages, and OTP lifecycle.
    """
    def __init__(self):
        self.lock = threading.Lock()
        # Initialize connection using URI from config.py
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client.get_default_database("db_messenger")
        
        # Collection references
        self.users = self.db["users"]
        self.messages = self.db["messages"]
        self.otp_store = self.db["otp_store"]
        
        self.setup()

    def setup(self):
        """
        Creates indexes required for indexing and automatic OTP expiration.
        """
        # Create a TTL index for OTP expiration (automatically cleans up expired OTPs)
        self.otp_store.create_index("expiry_time", expireAfterSeconds=0)
        
        # Create indexes for optimal messaging query performance
        self.messages.create_index([("sender_mail", 1), ("receiver_mail", 1)])
        self.messages.create_index([("receiver_mail", 1), ("delivery_status", 1)])

    def register_user(self, email, password, name):
        """
        Registers a new user after hashing the password.
        """
        email_normalized = email.lower().strip()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.users.insert_one({
                "_id": email_normalized,
                "hashed_password": hashed_password.decode('utf-8') if isinstance(hashed_password, bytes) else hashed_password,
                "name": name
            })
            return True
        except DuplicateKeyError:
            return False

    def get_user(self, email):
        """
        Queries and returns a user profile by email address.
        """
        email_normalized = email.lower().strip()
        user_doc = self.users.find_one({"_id": email_normalized})
        if user_doc:
            # Matches SQLite return format: (email, hashed_password, name)
            return (user_doc["_id"], user_doc["hashed_password"], user_doc["name"])
        return None

    def verify_password(self, plain_password, hashed_password):
        """
        Verifies if a plain password matches its bcrypt hash.
        """
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    def save_message(self, sender_email, recipient_email, content):
        """
        Saves a direct chat message to the messages collection.
        """
        sender_normalized = sender_email.lower().strip()
        recipient_normalized = recipient_email.lower().strip()
        self.messages.insert_one({
            "sender_mail": sender_normalized,
            "receiver_mail": recipient_normalized,
            "content": content,
            "time_sent": datetime.utcnow(),
            "delivery_status": 0
        })

    def get_undelivered_messages(self, recipient_email):
        """
        Returns all messages pending delivery for a recipient.
        """
        recipient_normalized = recipient_email.lower().strip()
        cursor = self.messages.find({"receiver_mail": recipient_normalized, "delivery_status": 0})
        # Matches SQLite return format: (id, sender_mail, content)
        return [(str(msg["_id"]), msg["sender_mail"], msg["content"]) for msg in cursor]

    def mark_message_as_delivered(self, recipient_email):
        """
        Updates the delivery status of all pending messages for a recipient.
        """
        recipient_normalized = recipient_email.lower().strip()
        self.messages.update_many(
            {"receiver_mail": recipient_normalized, "delivery_status": 0},
            {"$set": {"delivery_status": 1}}
        )

    def save_otp(self, email, otp):
        """
        Stores an OTP verification code with a 10-minute expiry time.
        """
        email_normalized = email.lower().strip()
        expiry_time = datetime.utcnow() + timedelta(minutes=10)
        try:
            self.otp_store.update_one(
                {"_id": email_normalized},
                {"$set": {"otp": otp, "expiry_time": expiry_time}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error saving OTP for {email_normalized}: {e}")
            return False

    def verify_otp(self, email, otp):
        """
        Validates the submitted OTP code. Matches string, integer, or padded formats.
        """
        email_normalized = email.lower().strip()
        try:
            formatted_otp = f"{int(otp):06d}"
        except (ValueError, TypeError):
            formatted_otp = str(otp)
            
        try:
            otp_int = int(otp)
        except (ValueError, TypeError):
            otp_int = None

        query_or = [
            {"otp": otp},
            {"otp": formatted_otp},
            {"otp": str(otp)}
        ]
        if otp_int is not None:
            query_or.append({"otp": otp_int})

        record = self.otp_store.find_one({
            "_id": email_normalized,
            "$or": query_or
        })
        if not record:
            return False
        # Double check in case the TTL deletion thread hasn't run yet
        if record["expiry_time"] < datetime.utcnow():
            return False
        return True

    def delete_otp(self, email):
        """
        Removes an OTP code from the database.
        """
        email_normalized = email.lower().strip()
        self.otp_store.delete_one({"_id": email_normalized})

    def update_password(self, email, new_password):
        """
        Updates a user's password hash.
        """
        email_normalized = email.lower().strip()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        result = self.users.update_one(
            {"_id": email_normalized},
            {"$set": {"hashed_password": hashed_password.decode('utf-8') if isinstance(hashed_password, bytes) else hashed_password}}
        )
        return result.modified_count > 0

    def get_chat_history(self, user1_email, user2_email):
        """
        Queries direct messaging history between two users sorted chronologically.
        """
        u1_normalized = user1_email.lower().strip()
        u2_normalized = user2_email.lower().strip()
        cursor = self.messages.find({
            "$or": [
                {"sender_mail": u1_normalized, "receiver_mail": u2_normalized},
                {"sender_mail": u2_normalized, "receiver_mail": u1_normalized}
            ]
        }).sort("time_sent", 1)
        
        return [{
            "sender": msg["sender_mail"],
            "receiver": msg["receiver_mail"],
            "content": msg["content"],
            # Format time like SQLite ("%Y-%m-%d %H:%M:%S") so client's timezone conversion is triggered correctly
            "time": msg["time_sent"].strftime("%Y-%m-%d %H:%M:%S")
        } for msg in cursor]

    def get_recent_chats(self, email):
        """
        Aggregates recent private chat contacts for a user.
        """
        email_normalized = email.lower().strip()
        cursor = self.messages.find(
            {"$or": [{"sender_mail": email_normalized}, {"receiver_mail": email_normalized}]},
            {"sender_mail": 1, "receiver_mail": 1}
        )
        
        partners = set()
        for msg in cursor:
            partner = msg["receiver_mail"] if msg["sender_mail"] == email_normalized else msg["sender_mail"]
            partners.add(partner)
            
        recent_contacts = []
        for partner in partners:
            user_doc = self.users.find_one({"_id": partner})
            if user_doc:
                recent_contacts.append({"email": partner, "name": user_doc["name"]})
        return recent_contacts
