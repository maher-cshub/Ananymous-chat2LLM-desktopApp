import json
import os
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecureDatabase:
    def __init__(self, db_path, master_password):
        """
        Initialize the secure database with a master password
        
        Args:
            db_path (str): Path to the database file
            master_password (str): Master password for encryption/decryption
        """
        self.db_path = Path(db_path)
        self.master_password = master_password
        self.key = self._generate_key(master_password)
        self.fernet = Fernet(self.key)
        self.data = {}
        
        # Create directory if it doesn't exist
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Load database if it exists
        if self.db_path.exists():
            self.load()
    
    def _generate_key(self, password):
        """
        Generate a key from the master password
        
        Args:
            password (str): Master password
            
        Returns:
            bytes: Encryption key
        """
        # Use a static salt - in production, this should be stored securely
        salt = b'DuckDuckGoAIChat_Salt_Value_Static'
        
        # Generate a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def load(self):
        """
        Load and decrypt the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.db_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt the data
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.data = json.loads(decrypted_data.decode())
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            self.data = {}
            return False
    
    def save(self):
        """
        Encrypt and save the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Convert data to JSON string
            json_data = json.dumps(self.data)
            
            # Encrypt the data
            encrypted_data = self.fernet.encrypt(json_data.encode())
            
            # Save to file
            with open(self.db_path, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def get(self, key, default=None):
        """
        Get a value from the database
        
        Args:
            key (str): Key to get
            default: Default value if key doesn't exist
            
        Returns:
            The value or default
        """
        return self.data.get(key, default)
    
    def set(self, key, value):
        """
        Set a value in the database
        
        Args:
            key (str): Key to set
            value: Value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.data[key] = value
        return self.save()
    
    def delete(self, key):
        """
        Delete a key from the database
        
        Args:
            key (str): Key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if key in self.data:
            del self.data[key]
            return self.save()
        return False
    
    def get_all(self):
        """
        Get all data from the database
        
        Returns:
            dict: All data
        """
        return self.data
    
    def clear(self):
        """
        Clear all data from the database
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.data = {}
        return self.save()


class UserManager:
    def __init__(self, master_password):
        """
        Initialize the user manager with a master password
        
        Args:
            master_password (str): Master password for encryption/decryption
        """
        # User data directory
        self.user_data_dir = Path(os.path.expanduser("~")) / ".ddg_ai_chat"
        
        # Users database file
        self.users_db_path = self.user_data_dir / "users.db"
        
        # Initialize the secure database
        self.db = SecureDatabase(self.users_db_path, master_password)
        
        # Current user
        self.current_user = None
        
        # Load users
        self.users = self.db.get('users', {})
    
    def hash_password(self, password, salt=None):
        """
        Hash a password with a salt
        
        Args:
            password (str): Password to hash
            salt (bytes, optional): Salt to use. If None, a new salt is generated.
            
        Returns:
            tuple: (password_hash, salt)
        """
        if salt is None:
            salt = os.urandom(32)  # 32 bytes = 256 bits
        
        # Hash the password with the salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            100000  # Number of iterations
        )
        
        return password_hash.hex(), salt.hex()
    
    def verify_password(self, password, stored_hash, stored_salt):
        """
        Verify a password against a stored hash and salt
        
        Args:
            password (str): Password to verify
            stored_hash (str): Stored password hash
            stored_salt (str): Stored salt
            
        Returns:
            bool: True if password matches, False otherwise
        """
        # Convert stored salt from hex to bytes
        salt = bytes.fromhex(stored_salt)
        
        # Hash the password with the stored salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            100000  # Number of iterations
        ).hex()
        
        # Compare the hashes
        return password_hash == stored_hash
    
    def register_user(self, username, password):
        """
        Register a new user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            tuple: (success, message)
        """
        if username in self.users:
            return False, "Username already exists"
        
        # Hash the password with a new salt
        password_hash, salt = self.hash_password(password)
        
        # Create the user
        self.users[username] = {
            "password_hash": password_hash,
            "salt": salt,
            "created_at": os.time(),
            "last_login": os.time(),
            "chat_history": []
        }
        
        # Save the users
        self.db.set('users', self.users)
        
        return True, "User registered successfully"
    
    def login_user(self, username, password):
        """
        Login a user
        
        Args:
            username (str): Username
            password (str): Password
            
        Returns:
            tuple: (success, message)
        """
        if username not in self.users:
            return False, "Username does not exist"
        
        user = self.users[username]
        
        # Verify the password
        if not self.verify_password(password, user["password_hash"], user["salt"]):
            return False, "Incorrect password"
        
        # Update last login time
        self.users[username]["last_login"] = os.time()
        self.db.set('users', self.users)
        
        # Set current user
        self.current_user = username
        
        return True, "Login successful"
    
    def logout_user(self):
        """
        Logout the current user
        
        Returns:
            tuple: (success, message)
        """
        self.current_user = None
        return True, "Logout successful"
    
    def get_user_data(self):
        """
        Get the current user's data
        
        Returns:
            dict: User data or None if no user is logged in
        """
        if not self.current_user:
            return None
        
        return self.users[self.current_user]
    
    def save_chat_history(self, chat_history):
        """
        Save the chat history for the current user
        
        Args:
            chat_history (list): Chat history
            
        Returns:
            tuple: (success, message)
        """
        if not self.current_user:
            return False, "No user logged in"
        
        self.users[self.current_user]["chat_history"] = chat_history
        self.db.set('users', self.users)
        
        return True, "Chat history saved"