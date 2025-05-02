import webview as webview
import os
import sys
import json
import time
import getpass
from pathlib import Path
from secure_db import UserManager


# Application title
APP_TITLE = "DuckDuckGo AI Chat Desktop"
# URL for DuckDuckGo AI Chat
DDG_AI_CHAT_URL = "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1"

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# HTML templates directory
TEMPLATES_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / "templates"

# Master password for database encryption
# In a real application, this would be securely stored or derived from user input
# For this demo, we'll use a hardcoded password
MASTER_PASSWORD = "your_secure_master_password_here"  # Change this to your own secure password


class DuckDuckGoAIChat:
    def __init__(self):
        self.window = None
        # Initialize the user manager with the master password
        self.user_manager = UserManager(MASTER_PASSWORD)
    
    def get_html_content(self, file_name):
        """Get the content of an HTML file"""
        file_path = TEMPLATES_DIR / file_name
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def create_login_window(self):
        """Create the login window"""
        html_content = self.get_html_content("login.html")
        
        if not html_content:
            # If login.html doesn't exist, create a basic login form
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Login - DuckDuckGo AI Chat</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f5f5f5;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .login-container {
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                        padding: 30px;
                        width: 350px;
                    }
                    h1 {
                        text-align: center;
                        color: #333;
                        margin-bottom: 20px;
                    }
                    .form-group {
                        margin-bottom: 15px;
                    }
                    label {
                        display: block;
                        margin-bottom: 5px;
                        color: #555;
                    }
                    input {
                        width: 100%;
                        padding: 10px;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        box-sizing: border-box;
                    }
                    button {
                        width: 100%;
                        padding: 10px;
                        background-color: #de5833;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 16px;
                        margin-top: 10px;
                    }
                    button:hover {
                        background-color: #c94a2a;
                    }
                    .error-message {
                        color: red;
                        text-align: center;
                        margin-top: 10px;
                        display: none;
                    }
                    .switch-form {
                        text-align: center;
                        margin-top: 20px;
                        color: #555;
                    }
                    .switch-form a {
                        color: #de5833;
                        text-decoration: none;
                    }
                    .switch-form a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <div class="login-container">
                    <h1>DuckDuckGo AI Chat</h1>
                    <div id="login-form">
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <button id="login-button">Login</button>
                        <div id="login-error" class="error-message"></div>
                        <div class="switch-form">
                            Don't have an account? <a href="#" id="switch-to-register">Register</a>
                        </div>
                    </div>
                    <div id="register-form" style="display: none;">
                        <div class="form-group">
                            <label for="reg-username">Username</label>
                            <input type="text" id="reg-username" name="reg-username" required>
                        </div>
                        <div class="form-group">
                            <label for="reg-password">Password</label>
                            <input type="password" id="reg-password" name="reg-password" required>
                        </div>
                        <div class="form-group">
                            <label for="reg-confirm-password">Confirm Password</label>
                            <input type="password" id="reg-confirm-password" name="reg-confirm-password" required>
                        </div>
                        <button id="register-button">Register</button>
                        <div id="register-error" class="error-message"></div>
                        <div class="switch-form">
                            Already have an account? <a href="#" id="switch-to-login">Login</a>
                        </div>
                    </div>
                </div>
                <script>
                    // Switch between login and register forms
                    document.getElementById('switch-to-register').addEventListener('click', function(e) {
                        e.preventDefault();
                        document.getElementById('login-form').style.display = 'none';
                        document.getElementById('register-form').style.display = 'block';
                    });
                    
                    document.getElementById('switch-to-login').addEventListener('click', function(e) {
                        e.preventDefault();
                        document.getElementById('register-form').style.display = 'none';
                        document.getElementById('login-form').style.display = 'block';
                    });
                    
                    // Login form submission
                    document.getElementById('login-button').addEventListener('click', function() {
                        const username = document.getElementById('username').value;
                        const password = document.getElementById('password').value;
                        
                        if (!username || !password) {
                            document.getElementById('login-error').textContent = 'Please fill in all fields';
                            document.getElementById('login-error').style.display = 'block';
                            return;
                        }
                        
                        window.pywebview.api.login(username, password).then(function(response) {
                            if (response.success) {
                                // Login successful, redirect to chat
                                window.pywebview.api.load_chat();
                            } else {
                                // Show error message
                                document.getElementById('login-error').textContent = response.message;
                                document.getElementById('login-error').style.display = 'block';
                            }
                        });
                    });
                    
                    // Register form submission
                    document.getElementById('register-button').addEventListener('click', function() {
                        const username = document.getElementById('reg-username').value;
                        const password = document.getElementById('reg-password').value;
                        const confirmPassword = document.getElementById('reg-confirm-password').value;
                        
                        if (!username || !password || !confirmPassword) {
                            document.getElementById('register-error').textContent = 'Please fill in all fields';
                            document.getElementById('register-error').style.display = 'block';
                            return;
                        }
                        
                        if (password !== confirmPassword) {
                            document.getElementById('register-error').textContent = 'Passwords do not match';
                            document.getElementById('register-error').style.display = 'block';
                            return;
                        }
                        
                        window.pywebview.api.register(username, password).then(function(response) {
                            if (response.success) {
                                // Registration successful, switch to login form
                                document.getElementById('register-form').style.display = 'none';
                                document.getElementById('login-form').style.display = 'block';
                                document.getElementById('login-error').textContent = 'Registration successful. Please login.';
                                document.getElementById('login-error').style.display = 'block';
                                document.getElementById('login-error').style.color = 'green';
                            } else {
                                // Show error message
                                document.getElementById('register-error').textContent = response.message;
                                document.getElementById('register-error').style.display = 'block';
                            }
                        });
                    });
                </script>
            </body>
            </html>
            """
        
        self.window = webview.create_window(
            title=APP_TITLE,
            html=html_content,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            resizable=True,
            min_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
            text_select=True,
            confirm_close=True,
            js_api=self
        )
    
    def create_chat_window(self):
        """Create the chat window"""
        # Try to load custom HTML first
        html_content = self.get_html_content("chat.html")
        
        if html_content:
            self.window.load_html(html_content)
        else:
            # Fall back to DuckDuckGo AI Chat URL
            self.window.load_url(DDG_AI_CHAT_URL)
    
    def register(self, username, password):
        """Register a new user"""
        success, message = self.user_manager.register_user(username, password)
        return {"success": success, "message": message}
    
    def login(self, username, password):
        """Login a user"""
        success, message = self.user_manager.login_user(username, password)
        return {"success": success, "message": message}
    
    def logout(self):
        """Logout the current user"""
        success, message = self.user_manager.logout_user()
        return {"success": success, "message": message}
    
    def load_chat(self):
        """Load the chat window"""
        self.create_chat_window()
        return {"success": True}
    
    def save_chat(self, chat_history):
        """Save the chat history"""
        success, message = self.user_manager.save_chat_history(chat_history)
        return {"success": success, "message": message}
    
    def get_chat_history(self):
        """Get the chat history for the current user"""
        user_data = self.user_manager.get_user_data()
        if user_data:
            return {"success": True, "chat_history": user_data["chat_history"]}
        return {"success": False, "message": "No user logged in"}
    
    def run(self):
        """Run the application"""
        self.create_login_window()
        webview.start(debug=True)


if __name__ == "__main__":
    # Create and run the application
    app = DuckDuckGoAIChat()
    app.run()