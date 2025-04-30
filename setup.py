from setuptools import setup, find_packages

setup(
    name="duckduckgo-ai-chat-desktop",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pywebview>=4.0",
    ],
    entry_points={
        'console_scripts': [
            'duckduckgo-ai-chat=app:main',
        ],
    },
    author="User",
    author_email="user@example.com",
    description="Desktop application for DuckDuckGo AI Chat",
    keywords="duckduckgo, ai, chat, desktop",
    python_requires=">=3.7",
)