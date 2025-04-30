import webview
import os
import sys

# Application title
APP_TITLE = "DuckDuckGo AI Chat Desktop"
# URL for DuckDuckGo AI Chat
DDG_AI_CHAT_URL = "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1"

# Window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800


class DuckDuckGoAIChat:
    def __init__(self):
        self.window = None
    
    def create_window(self):
        """Create the main application window"""
        self.window = webview.create_window(
            title=APP_TITLE,
            url=DDG_AI_CHAT_URL,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            resizable=True,
            min_size=(WINDOW_WIDTH, WINDOW_HEIGHT),
            text_select=True,
        )
        
    
    
    def run(self):
        """Run the application"""
        self.create_window()
        webview.start(debug=False)


if __name__ == "__main__":
    # Create and run the application
    app = DuckDuckGoAIChat()
    app.run()