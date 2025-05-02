import os
import sys
import subprocess
import platform

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building DuckDuckGo AI Chat Desktop Application...")
    
    # Determine the icon file based on the platform
    icon_param = ""
    if platform.system() == "Windows":
        icon_param = "--icon=resources/icon.ico"
    elif platform.system() == "Darwin":  # macOS
        icon_param = "--icon=resources/icon.icns"
    else:  # Linux
        icon_param = "--icon=resources/icon.png"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=DuckDuckGoAIChat",
        "--onefile",
        "--windowed",
        icon_param,
        "--clean",
        "--add-data=resources;resources" if platform.system() == "Windows" else "--add-data=resources:resources",
        "app.py"
    ]
    
    # Remove empty icon parameter if resources don't exist yet
    if not os.path.exists("resources"):
        cmd.remove(icon_param)
    
    # Execute the command
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        print(f"Executable can be found in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nError building executable: {e}")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pywebview
        subprocess.run(["pyinstaller", "--version"], check=True, stdout=subprocess.PIPE)
        return True
    except ImportError:
        print("Error: PyWebView is not installed. Please run: pip install -r requirements.txt")
        return False
    except subprocess.CalledProcessError:
        print("Error: PyInstaller is not installed. Please run: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        return False

def create_resources_folder():
    """Create resources folder if it doesn't exist"""
    if not os.path.exists("resources"):
        os.makedirs("resources")
        print("Created resources folder. You may want to add an icon file there.")

if __name__ == "__main__":
    print("=== DuckDuckGo AI Chat Desktop App Builder ===")
    
    if check_dependencies():
        create_resources_folder()
        build_executable()