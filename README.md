# DuckDuckGo AI Chat Desktop Application

A desktop application that wraps DuckDuckGo's AI Chat service using PyWebView, providing a native desktop experience for the web-based chat interface.

## Features

- Native desktop application experience for DuckDuckGo AI Chat
- Cross-platform support (Windows, macOS, Linux)
- Customizable window size and appearance
- Easy installation and setup

## Requirements

- Python 3.7 or higher
- PyWebView 4.0 or higher
- PyInstaller 5.0 or higher (for packaging)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Ananymous-chat2LLM-desktopApp.git
   cd Ananymous-chat2LLM-desktopApp
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

To run the application directly from Python:

```
python app.py
```

This will open a window with the DuckDuckGo AI Chat interface.

### Building a Standalone Executable

To build a standalone executable that can be distributed without requiring Python:

```
python build_app.py
```

This will create an executable in the `dist` folder that can be run on your operating system without requiring Python to be installed.

#### Adding a Custom Icon

To customize the application icon:

1. Create a `resources` folder (if it doesn't exist already)
2. Add your icon file to the resources folder:
   - Windows: `icon.ico`
   - macOS: `icon.icns`
   - Linux: `icon.png`

## Customization

You can customize the application by modifying the following parameters in `app.py`:

- `APP_TITLE`: Change the window title
- `WINDOW_WIDTH` and `WINDOW_HEIGHT`: Adjust the default window size
- `CUSTOM_CSS`: Modify the CSS to change the appearance of the chat interface

## Troubleshooting

### Common Issues

- **Application doesn't start**: Make sure all dependencies are installed correctly
- **Blank screen**: Check your internet connection, as the application requires internet access to load the DuckDuckGo AI Chat
- **Packaging errors**: Ensure PyInstaller is installed correctly and try running with the `--clean` flag

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [PyWebView](https://pywebview.flowrl.com/) - For providing the webview framework
- [DuckDuckGo](https://duckduckgo.com/) - For their AI Chat service