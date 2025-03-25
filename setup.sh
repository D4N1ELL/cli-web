#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Path to compiled binary
BIN_PATH="$SCRIPT_DIR/dist/go2web"

# Make the binary executable
chmod +x "$BIN_PATH"

# Check if already installed
if [ -f "/usr/local/bin/go2web" ]; then
    echo "go2web is already installed."
else
    # Create symbolic link to make it accessible globally
    sudo ln -s "$BIN_PATH" /usr/local/bin/go2web
    echo "go2web has been installed successfully!"
fi

echo "You can now use 'go2web' from anywhere."
